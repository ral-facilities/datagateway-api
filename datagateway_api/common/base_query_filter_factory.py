from abc import abstractstaticmethod


class QueryFilterFactory(object):
    @abstractstaticmethod
    def get_query_filter(request_filter):
        """
        Given a filter, return a matching Query filter object

        :param request_filter: The filter to create the QueryFilter for
        :type request_filter: :class:`dict`
        :return: The QueryFilter object created
        """
        pass
