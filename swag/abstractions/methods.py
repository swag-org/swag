from typing import Union, Type


HTTPGetMethod = Type["GET"]
HTTPPostMethod = Type["POST"]
HTTPPutMethod = Type["PUT"]
HTTPDeleteMethod = Type["DELETE"]
HTTPPatchMethod = Type["PATCH"]
HTTPOptionsMethod = Type["OPTIONS"]
HTTPHeadMethod = Type["HEAD"]


HTTPMethod = Union[
    HTTPPostMethod,  HTTPGetMethod,
    HTTPPutMethod, HTTPDeleteMethod,
    HTTPPatchMethod, HTTPOptionsMethod,
    HTTPHeadMethod]