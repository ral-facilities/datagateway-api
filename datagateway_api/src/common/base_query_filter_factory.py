from abc import abstractstaticmethod


class QueryFilterFactory(object):
    @abstractstaticmethod
    def get_query_filter(request_filter, entity_name=None):  # noqa: B902, N805
        """
        Given a filter, return a matching Query filter object

        :param request_filter: The filter to create the QueryFilter for
        :type request_filter: :class:`dict`
        :param entity_name: Entity name of the endpoint, optional (only used for search
            API, not DataGateway API)
        :type entity_name: :class:`str`
        :return: The QueryFilter object created
        """
        pass
