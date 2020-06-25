import aiofiles
import csv

from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum



my_app = FastAPI()


class Item(BaseModel):
	name : str
	price : float
	is_on_offer : bool = None

class User_info(BaseModel):
	fname : str
	lname : str
	phone : int
	email : str



#Populate User info from external source
external_source = {
   "fname" : "Ram",
   "lname" : "Shadows",
    "phone" : "0721700575",
   "email" : "ramshadows@gmail.com",

}

user = User_info(**external_source)


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]



@my_app.get("/")
async def read_root():
	return {"Hello" : "World"}


@my_app.get("/items/{item_id}")
async def read_item(item_id : int, q : str = None):
	return {"item_id" : item_id, "q" : q}


@my_app.put("/items/{item_id}")
async def update_items(item_id : int, item : Item):
	return {"item_id" : item_id, "item_name" : item.name}

@my_app.get("/items/")
async def update_items(skip: int = 0, limit: int = 10):
	return fake_items_db[skip : skip + limit]

@my_app.get("/user_info")
async def get_user_info():
	return {"user_info" : user}

@my_app.get("/model/{model_name}")
async def get_model(model_name : ModelName):
	if model_name.value == ModelName.alexnet:
		return {"model_name" : model_name, "message": "Deep Learning FTW!"}
	if model_name.value == "lenet":
		return {"model_name": model_name, "message": "LeCNN all the images"}

	return {"model_name": model_name, "message": "Have some residuals"}


class Portfolio(BaseModel):
	name : str
	share : int
	price : float

#A pydantic model to receive the Request Body parameters
class StockDetails(BaseModel):
	name : str
	description : str = None
	price : float
	tax : float = None

"""
The API will receive a json object / python dict similar to these
{
    "name": "Saf",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5
}
"""
stock_detail = {
  "name": "Saf",
  "description": "An optional description",
  "price": 45.2,
  "tax": 3.5

}

stoc = StockDetails(**stock_detail)
#Request Body
@my_app.post("/stock/")
async def create_stock(stock : StockDetails):
	""" Inside of the function, you can access all the attributes of the model object directly:"""
	stock_dict = stock.dict()
	if stock.tax:
		price_with_tax = stock.price + stock.tax
		stock_dict.update({"price_with_tax" : price_with_tax})
	return stock_dict

#Request Body + Path parameters
@my_app.put("/stock/{stock_id}")
async def create_stock(stock_id : int):
	return{"stock_id" : stock_id, **stoc.dict()}







@my_app.get("/portfolio/")
async def read_portfolio():
	stock_portfolio = []
	with open("Data/portfolio.csv", "rt") as f:
		rows = csv.reader(f)
		headers = next(rows)
		for row in rows:
			stock = Portfolio(name = row[0], share = row[1], price = row[2])
			stock_portfolio.append(stock)



		return {"portfolio" : stock_portfolio}
