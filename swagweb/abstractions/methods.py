from typing import Union, Literal


HTTPGetMethod = Literal["GET"]
HTTPPostMethod = Literal["POST"]
HTTPPutMethod = Literal["PUT"]
HTTPDeleteMethod = Literal["DELETE"]
HTTPPatchMethod = Literal["PATCH"]
HTTPOptionsMethod = Literal["OPTIONS"]
HTTPHeadMethod = Literal["HEAD"]


HTTPMethod = Union[
    HTTPPostMethod,
    HTTPGetMethod,
    HTTPPutMethod,
    HTTPDeleteMethod,
    HTTPPatchMethod,
    HTTPOptionsMethod,
    HTTPHeadMethod,
]
