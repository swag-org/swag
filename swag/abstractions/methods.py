from typing import Union, Type


HTTPGetMethod = Type["GET"]
HTTPPostMethod = Type["POST"]
HTTPPutMethod = Type["PUT"]
HTTPDeleteMethod = Type["DELETE"]
HTTPMethod = Union[HTTPPostMethod,  HTTPGetMethod, HTTPPutMethod, HTTPDeleteMethod]

AllHTTPMethods = ["GET", "POST", "PUT", "DELETE"]