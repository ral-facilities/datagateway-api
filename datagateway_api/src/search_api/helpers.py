from functools import wraps
import json
import logging
import traceback

from pydantic import ValidationError
import requests

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.exceptions import (
    BadRequestError,
    MissingRecordError,
    ScoringAPIError,
    SearchAPIError,
)
from datagateway_api.src.common.filter_order_handler import FilterOrderHandler
from datagateway_api.src.search_api.filters import (
    SearchAPIIncludeFilter,
    SearchAPIWhereFilter,
)
from datagateway_api.src.search_api.filters import (
    SearchAPIQueryFilter,
)
import datagateway_api.src.search_api.models as models
from datagateway_api.src.search_api.query import SearchAPIQuery
from datagateway_api.src.search_api.session_handler import (
    client_manager,
    SessionHandler,
)

log = logging.getLogger()


def search_api_error_handling(method):
    """
    Decorator (similar to `queries_records`) to handle exceptions and present in a way
    required for the search API. The decorator should be applied to search API endpoint
    resources

    :param method: The method for the endpoint
    :raises: Any exception caught by the execution of `method`
    """

    @wraps(method)
    def wrapper_error_handling(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ValidationError as e:
            log.exception(msg=e.args)
            assign_status_code(e, 500)
            raise SearchAPIError(create_error_message(e))
        except ConnectionError as e:
            log.exception(msg=e.args)
            assign_status_code(e, 500)
            raise ScoringAPIError(create_error_message(e))
        except (ValueError, TypeError, AttributeError, KeyError) as e:
            log.exception(msg=e.args)
            assign_status_code(e, 400)
            raise BadRequestError(create_error_message(e))
        except Exception as e:
            log.exception(msg=e.args)
            # Defensively assign a 500 if the exception doesn't already have a status
            # code
            assign_status_code(e, 500)
            raise type(e)(create_error_message(e))

    def assign_status_code(e, status_code):
        try:
            # If no status code exists (for non-API defined exceptions), assign a status
            # code
            e.status_code
        except AttributeError:
            e.status_code = status_code

    def create_error_message(e):
        return {
            "error": {
                "statusCode": e.status_code,
                "name": e.__class__.__name__,
                "message": str(e),
            },
        }

    return wrapper_error_handling


def get_score(entities, query, group, limit):
    """
    Gets the score on the given entities based in the query parameter and limit
    """

    try:
        myobj = {
            "query": query,
            "group": Config.config.search_api.scoring_group,
            "limit": limit,
            #"itemIds": list(map(lambda entity: entity["pid"], entities)),
        }

        print(Config.config.search_api.scoring_server)
        response = requests.post(
            Config.config.search_api.scoring_server, json=myobj, timeout=5
        )
        print((response.text))
        if response.status_code < 400:
            scores = response.json()["scores"]
            print(str(len(scores)) + " scores retrieved from scoring app")
            print(str(len(entities)) + " entities retrieved from ICAT")
            for entity in entities:
                items = list(
                    filter(
                        lambda score: str(score["itemId"]) == str(entity["pid"]),
                        scores,
                    ),
                )

                if len(items) == 1:

                    print(
                        "FOUND",
                        entity["startDate"],
                        entity["title"],
                        entity["pid"],
                        entity["doi"],
                        entity["summary"],
                        items[0]["score"],
                    )
                    entity["score"] = items[0]["score"]

                else:
                    # print("not FOUND %s", entity)
                    print(
                        "NOT FOUND",
                        entity["startDate"],
                        entity["title"],
                        entity["pid"],
                        entity["doi"],
                    )
                    entity["score"] = -1
                # filter(
                #    lambda x: x["itemId"] == entity["pid"], response.json()
                # )["score"]
            return entities
        else:
            raise ScoringAPIError(
                Exception(f"Score API returned {response.status_code}"),
            )
    except ConnectionError as e:
        log.error("ConnectionError to %s ", url)
        raise e
    except Exception as e:
        traceback.print_exc()
        log.error("Error on scoring")
        raise e


@client_manager
def get_search(entity_name, filters, str_conditions=None):
    """
    Search for data on the given entity, using filters from the request to restrict the
    query

    :param entity_name: Name of the entity requested to query against
    :type entity_name: :class:`str`
    :param filters: The list of Search API filters to be applied to the request/query
    :type filters: List of specific implementation :class:`QueryFilter`
    :param str_conditions: Where clause to be applied to the JPQL query
    :type str_conditions: :class:`str`
    :return: List of records (in JSON serialisable format) of the given entity for the
        query constructed from that and the request's filters
    """

    log.info("Searching for %s using request's filters", entity_name)
    log.debug("Entity Name: %s, Filters: %s", entity_name, filters)

    entity_relations = []
    for filter_ in filters:
        if isinstance(filter_, SearchAPIIncludeFilter):
            entity_relations.extend(filter_.included_filters)

    query = SearchAPIQuery(entity_name, str_conditions=str_conditions)
    log.debug("Query: %s", query)
    filter_handler = FilterOrderHandler()
    filter_handler.add_filters(filters)
    filter_handler.add_icat_relations_for_panosc_non_related_fields(entity_name)
    filter_handler.add_icat_relations_for_non_related_fields_of_panosc_related_entities(
        entity_name,
    )
    filter_handler.merge_python_icat_limit_skip_filters()
    filter_handler.apply_filters(query)

    log.debug("JPQL Query to be sent/executed in ICAT: %s", query.icat_query.query)
    icat_query_data = query.icat_query.execute_query(SessionHandler.client, True)

    panosc_data = []
    for icat_data in icat_query_data:
        panosc_model = getattr(models, entity_name)
        panosc_record = panosc_model.from_icat(icat_data, entity_relations).json(
            by_alias=True,
        )
        panosc_data.append(json.loads(panosc_record))

    return panosc_data


@client_manager
def get_with_pid(entity_name, pid, filters):
    """
    Get a particular record of data from the specified entity

    These will only be called with entity names of Dataset, Document and Instrument.
    Each of these entities have a PID attribute, so we can assume the identifier will be
    persistent (or `pid`) rather than an ordinary identifier (`id`)

    :param entity_name: Name of the entity requested to query against
    :type entity_name: :class:`str`
    :param pid: Persistent identifier of the data to find
    :type pid: :class:`str`
    :param filters: The list of Search API filters to be applied to the request/query
    :type filters: List of specific implementation :class:`QueryFilter`
    :return: The (in JSON serialisable format) record of the specified PID
    :raises MissingRecordError: If no results can be found for the query
    """

    log.info("Getting %s from ID %s", entity_name, pid)
    log.debug("Entity Name: %s, Filters: %s", entity_name, filters)

    filters.append(SearchAPIWhereFilter("pid", pid, "eq"))

    panosc_data = get_search(entity_name, filters)
    if not panosc_data:
        raise MissingRecordError("No result found")
    else:
        return panosc_data[0]


@client_manager
def get_count(entity_name, filters):
    """
    Get the number of results of a given entity, with filters provided in the request to
    restrict the search

    :param entity_name: Name of the entity requested to query against
    :type entity_name: :class:`str`
    :param filters: The list of Search API filters to be applied to the request/query
    :type filters: List of specific implementation :class:`QueryFilter`
    :return: Dict containing the number of records returned from the query
    """

    log.info("Getting number of results for %s, using request's filters", entity_name)
    log.debug("Entity Name: %s, Filters: %s", entity_name, filters)

    query = SearchAPIQuery(entity_name, aggregate="COUNT")

    filter_handler = FilterOrderHandler()
    filter_handler.add_filters(filters)
    filter_handler.merge_python_icat_limit_skip_filters()
    filter_handler.apply_filters(query)

    log.debug("Python ICAT Query: %s", query.icat_query.query)

    log.debug("JPQL Query to be sent/executed in ICAT: %s", query.icat_query.query)
    icat_query_data = query.icat_query.execute_query(SessionHandler.client, True)

    return {"count": icat_query_data[0]}


@client_manager
def get_files(entity_name, pid, filters):
    """
    Using the PID of a dataset, find all of its associated files and return them

    :param entity_name: Name of the entity requested to query against
    :type entity_name: :class:`str`
    :param pid: Persistent identifier of the dataset
    :type pid: :class:`str`
    :param filters: The list of Search API filters to be applied to the request/query
    :type filters: List of specific implementation :class:`QueryFilter`
    :return: List of file records for the dataset given by PID
    """

    log.info("Getting files of dataset (PID: %s), using request's filters", pid)
    log.debug
    (
        "Entity Name: %s, Filters: %s",
        entity_name,
        filters,
    )

    filters.append(SearchAPIWhereFilter("dataset.pid", pid, "eq"))
    return get_search(entity_name, filters)


@client_manager
def get_files_count(entity_name, filters, pid):
    """
    Using the PID of a dataset, find the number of associated files

    :param entity_name: Name of the entity requested to query against
    :type entity_name: :class:`str`
    :param pid: Persistent identifier of the data to find
    :type pid: :class:`str`
    :param filters: The list of Search API filters to be applied to the request/query
    :type filters: List of specific implementation :class:`QueryFilter`
    :return: Dict containing the number of files for the dataset given by PID
    """

    log.info(
        "Getting number of files for dataset (PID: %s), using request's filters",
        pid,
    )
    log.debug(
        "Entity Name: %s, Filters: %s",
        entity_name,
        filters,
    )

    filters.append(SearchAPIWhereFilter("dataset.pid", pid, "eq"))
    return get_count(entity_name, filters)


def get_search_api_query_filter_list(filters):
    """
    Returns the list of SearchAPIQueryFilter that are in the filters array
    """
    return list(filter(lambda x: isinstance(x, SearchAPIQueryFilter), filters))


@client_manager
def is_query_parameter_enabled(filters):
    """
    Checks if query parameter is enabled based if the SearchAPIQueryFilter
    is in the query and the scoring is enabled
    """
    print(Config.config.search_api.password)
    return len(get_search_api_query_filter_list(filters)) == 1
