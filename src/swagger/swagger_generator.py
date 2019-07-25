class SwaggerGenerator(object):

    def __init__(self):
        self.endpoints = []

    def resource_wrapper(self):
        """
        Wrapper for Resource classes that appends the class name to the endpoints list
        """

        def decorate(cls):
            self.endpoints.append(cls.__name__)
            return cls

        return decorate
