"""

FastAPI allows you to declare additional information and validation for
your parameters.

Example


"""

from fastapi import FastAPI, Query


val_app = FastAPI()


@val_app.get("/items")
async def read_items(query_param : str):
	results = {"items" :[{"item_id" : "some_item"}, {"item_id": "some_item2"}]}

	if query_param:
		results.update({"queried_param" : query_param})

	return results

"""
The query parameter query_param is of type str, and by default is None, so it
is optional.

Additional validation

We are going to enforce that even though query_param is optional, whenever it is provided,
it doesn't exceed a length of 50 characters.

"""
@val_app.get("/items2")
async def read_items(query_param : str = Query(None, max_length = 50)):
	results = {"items" :[{"item_id" : "some_item"}, {"item_id": "some_item2"}]}

	if query_param:
		results.update({"queried_param" : query_param})

	return results

"""
As we have to replace the default value None with Query(None), the first
parameter to Query serves the same purpose of defining that default value.

So:

query_param: str = Query(None)

...makes the parameter optional, the same as:

query_param: str = None

But it declares it explicitly as being a query parameter.

And then, we can pass more parameters to Query. In this case, the max_length
parameter that applies to strings:

q: str = Query(None, max_length=50)

This will validate the data, show a clear error when the data is not valid, and
document the parameter in the OpenAPI schema path operation.

Add more validations

You can also add a parameter min_length:


"""

@val_app.get("/items3")
async def read_items(query_param : str = Query(None, min_length = 3, max_length = 50)):
	results = {"items" :[{"item_id" : "some_item"}, {"item_id": "some_item2"}]}

	if query_param:
		results.update({"queried_param" : query_param})

	return results

"""
Add regular expressions

You can define a regular expression that the parameter should match:

"""

@val_app.get("/items4")
async def read_items(query_param : str = Query(None, min_length = 3,
    max_length = 50, regex = "^fixedquery$")):
	results = {"items" :[{"item_id" : "some_item"}, {"item_id": "some_item2"}]}

	if query_param:
		results.update({"queried_param" : query_param})

	return results

"""
Default values

The same way that you can pass None as the first argument to be used as the
default value, you can pass other values.

Let's say that you want to declare the q query parameter to have a min_length
of 3, and to have a default value of :

"""

@val_app.get("/items5")
async def read_items(query_param : str = Query("defaultvalue", min_length = 3)):
	results = {"items" :[{"item_id" : "some_item"}, {"item_id": "some_item2"}]}

	if query_param:
		results.update({"queried_param" : query_param})

	return results

"""
So, when you need to declare a value as required while using Query, you can use
... as the first argument: This will let FastAPI know that this parameter is required.

"""
@val_app.get("/items6")
async def read_items(query_param : str = Query(..., min_length = 3)):
	results = {"items" :[{"item_id" : "some_item"}, {"item_id": "some_item2"}]}

	if query_param:
		results.update({"queried_param" : query_param})

	return results

"""
Query parameter list / multiple values

When you define a query parameter explicitly with Query you can also declare it
to receive a list of values, or said in other way, to receive multiple values.

Then, with a URL like:

http://localhost:8000/items/?query_params=foo&query_params=bar&query_params="?

you would receive the multiple q query parameters' values (Apple & Orange) in a
Python list inside your path operation function, in the function parameter
query_params.

So, the response to that URL would be:

{
  "item_list": [
    "foo",
    "bar"
  ]
}

"""
from typing import List


@val_app.get("/items7")
async def read_items(query_params : List[str] = Query(None)):
	queried_items = {"item_list" : query_params}

	return queried_items

"""
To declare a query parameter with a type of list, like in the example above,
you need to explicitly use Query, otherwise it would be interpreted as a
request body.

"""
"""
Query parameter list / multiple values with defaults

And you can also define a default list of values if none are provided:
"""
fruits = ["Apple", "Orange", "Mangoe", "Pineapple", "Pawpaw", "Avocado"]

@val_app.get("/items8")
async def read_items(query_params : List[str] = Query(fruits)):
	queried_items = {"item_list" : query_params}

	return queried_items

"""
If you go to:

http://localhost:8000/items8/

the default of query_param will be: ["Apple", "Orange", ...] and your response will be:

{
  "item_list": [
    "Apple",
	"Orange",
	"Mangoe",
	"Pineapple",
	"Pawpaw",
	"Avocado"
  ]
}

"""

"""
Declare more metadata

You can add more information about the parameter.

That information will be included in the generated OpenAPI and used by the
documentation user interfaces and external tools.

You can add a title, description

"""

@val_app.get("/items9")
async def read_items(
    query_param : str = Query(
	None,
	min_length = 3,
    title = "Account Details",
	description = "Query account details for the member to search in the database that have a good match"
    )):
	results = {"items" :[{"item_id" : "some_item"}, {"item_id": "some_item2"}]}

	if query_param:
		results.update({"queried_param" : query_param})

	return results


"""

	Generic validations and metadata:

    alias
    title
    description
    deprecated

Validations specific for strings:

    min_length
    max_length
    regex
"""
