from flask_restful import Resource

from datagateway_api.common.backends import create_backend
from datagateway_api.common.config import config
from datagateway_api.common.helpers import (
    get_filters_from_query_string,
    get_session_id_from_auth_header,
)

backend = create_backend(config.get_backend_type())


class InstrumentsFacilityCycles(Resource):
    def get(self, id_):
        """
        ---
        summary: Get an Instrument's FacilityCycles
        description: Given an Instrument id get facility cycles where the instrument has
            investigations that occur within that cycle, subject to the given filters
        tags:
            - FacilityCycles
        parameters:
            - in: path
              required: true
              name: id
              description: The id of the instrument to retrieve the facility cycles of
              schema:
                type: integer
            - WHERE_FILTER
            - ORDER_FILTER
            - LIMIT_FILTER
            - SKIP_FILTER
            - DISTINCT_FILTER
            - INCLUDE_FILTER
        responses:
            200:
                description: Success - returns a list of the instrument's facility
                    cycles that satisfy the filters
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: '#/components/schemas/FACILITYCYCLE'
            400:
                description: Bad request - Something was wrong with the request
            401:
                description: Unauthorized - No session ID found in HTTP Auth. header
            403:
                description: Forbidden - The session ID provided is invalid
            404:
                description: No such record - Unable to find a record in ICAT
        """
        return (
            backend.get_facility_cycles_for_instrument_with_filters(
                get_session_id_from_auth_header(), id_, get_filters_from_query_string(),
            ),
            200,
        )


class InstrumentsFacilityCyclesCount(Resource):
    def get(self, id_):
        """
        ---
        summary: Count an Instrument's FacilityCycles
        description: Return the count of the Facility Cycles that have investigations
            that occur within that cycle on the specified instrument that would be
            retrieved given the filters provided
        tags:
            - FacilityCycles
        parameters:
            - in: path
              required: true
              name: id
              description: The id of the instrument to count the facility cycles of
              schema:
                type: integer
            - WHERE_FILTER
            - DISTINCT_FILTER
        responses:
            200:
                description: Success - The count of the instrument's facility cycles
                    that satisfy the filters
                content:
                    application/json:
                        schema:
                            type: integer
            400:
                description: Bad request - Something was wrong with the request
            401:
                description: Unauthorized - No session ID found in HTTP Auth. header
            403:
                description: Forbidden - The session ID provided is invalid
            404:
                description: No such record - Unable to find a record in ICAT
        """
        return (
            backend.get_facility_cycles_for_instrument_count_with_filters(
                get_session_id_from_auth_header(), id_, get_filters_from_query_string(),
            ),
            200,
        )


class InstrumentsFacilityCyclesInvestigations(Resource):
    def get(self, instrument_id, cycle_id):
        """
        ---
        summary: Get the investigations for a given Facility Cycle & Instrument
        description: Given an Instrument id and Facility Cycle id, get the
            investigations that occur within that cycle on that instrument, subject to
            the given filters
        tags:
            - Investigations
        parameters:
            - in: path
              required: true
              name: instrument_id
              description: The id of the instrument to retrieve the investigations of
              schema:
                type: integer
            - in: path
              required: true
              name: cycle_id
              description: The id of the facility cycle to retrieve the investigations
              schema:
                type: integer
            - WHERE_FILTER
            - ORDER_FILTER
            - LIMIT_FILTER
            - SKIP_FILTER
            - DISTINCT_FILTER
            - INCLUDE_FILTER
        responses:
            200:
                description: Success - returns a list of the investigations for the
                    given instrument and facility cycle that satisfy the filters
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: '#/components/schemas/INVESTIGATION'
            400:
                description: Bad request - Something was wrong with the request
            401:
                description: Unauthorized - No session ID found in HTTP Auth. header
            403:
                description: Forbidden - The session ID provided is invalid
            404:
                description: No such record - Unable to find a record in ICAT
        """
        return (
            backend.get_investigations_for_instrument_in_facility_cycle_with_filters(
                get_session_id_from_auth_header(),
                instrument_id,
                cycle_id,
                get_filters_from_query_string(),
            ),
            200,
        )


class InstrumentsFacilityCyclesInvestigationsCount(Resource):
    def get(self, instrument_id, cycle_id):
        """
        ---
        summary: Count investigations for a given Facility Cycle & Instrument
        description: Given an Instrument id and Facility Cycle id, get the number of
            investigations that occur within that cycle on that instrument, subject to
            the given filters
        tags:
            - Investigations
        parameters:
            - in: path
              required: true
              name: instrument_id
              description: The id of the instrument to retrieve the investigations of
              schema:
                type: integer
            - in: path
              required: true
              name: cycle_id
              description: The id of the facility cycle to retrieve the investigations
              schema:
                type: integer
            - WHERE_FILTER
            - DISTINCT_FILTER
        responses:
            200:
                description: Success - The count of the investigations for the given
                    instrument and facility cycle that satisfy the filters
                content:
                    application/json:
                        schema:
                            type: integer
            400:
                description: Bad request - Something was wrong with the request
            401:
                description: Unauthorized - No session ID found in HTTP Auth. header
            403:
                description: Forbidden - The session ID provided is invalid
            404:
                description: No such record - Unable to find a record in ICAT
        """
        return (
            backend.get_investigation_count_for_instrument_facility_cycle_with_filters(
                get_session_id_from_auth_header(),
                instrument_id,
                cycle_id,
                get_filters_from_query_string(),
            ),
            200,
        )
