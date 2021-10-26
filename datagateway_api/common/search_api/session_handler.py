# TODO - can we enforce a singleton pattern on the class?
class SessionHandler:
    def __init__(self):
        self.client = None
        self.session_id = None


def requires_session_id(method):
    """
    TODO
    """
    pass

    """
    @wraps(method)
    def wrapper_requires_session(*args, **kwargs):
        pass

    return wrapper_requires_session
    """
