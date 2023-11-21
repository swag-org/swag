# Swag framework
Swag is a low-level library for writing http servers in python. Currently it is under active development and does not have a stable API, normal documentation or full functionality.
In this library I will try to implement the following principles:
- path-query typed queries, I'm going to support primitives like bool, int, float, str.
- caching for many things.
- customizability.
- 1 dependency - Python language (and its standard library).

but now I just started and so none of this is ready. I will develop the project as much as possible.
### A simple example that you can already use:
```python
from swag.app.app import SwagApp  
from swag.app.config import SwagAppConfig  
from swag.http.response import HTTPResponse  
  
my_config = SwagAppConfig(port=6969, host="0.0.0.0")  
  
app = SwagApp(config=my_config)  
  
  
@app.get("/hello")  
def hello(request, name: str):  
    return HTTPResponse(  
        f"<h1>Looks like we are live {str(request.__dict__)} {request.ip} </h1>",  
        content_type="text/html")  
app.start()
```
The library uses sockets under the hood and is synchronous.
