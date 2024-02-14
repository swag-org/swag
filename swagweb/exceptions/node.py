from swagweb.exceptions import SwagException


class NodeException(SwagException):
    pass


class NodeNotFoundException(NodeException):
    """
    Raise when the node not found.
    """
