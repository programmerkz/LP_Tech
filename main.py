from datetime import datetime
from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


__db_users = [
    {"id": 0, "user_name": "Alex", "role": "moderator"},
    {"id": 1, "user_name": "John", "role": "super admin"},
    {"id": 2, "user_name": "Bill", "role": "user"},
    {"id": 3, "user_name": "Kate", "role": "admin"}]

__db_operations = [
    {"id": 0, "user_id": 0, "currency": "KZT", "amount": 1_000},
    {"id": 1, "user_id": 0, "currency": "USD", "amount": 22_800},
    {"id": 2, "user_id": 3, "currency": "BTC", "amount": 14_200},
    {"id": 3, "user_id": 2, "currency": "KZT", "amount": 3_700},
    {"id": 4, "user_id": 2, "currency": "BTC", "amount": 1_100},
    {"id": 5, "user_id": 0, "currency": "KZT", "amount": 2_400},
    {"id": 6, "user_id": 1, "currency": "BTC", "amount": 400},
    {"id": 7, "user_id": 0, "currency": "USD", "amount": 1_900},
    ]

db_mock = {"users": __db_users, "operations": __db_operations}



app = FastAPI()


@app.get("/user/{user_id}")
def get_user(user_id: int) -> dict:
    fetch_result = [usr for usr in db_mock["users"] if usr.get("id") == user_id]

    if len(fetch_result) == 0:
        raise HTTPException(status_code=404, detail="User not found")
    
    return fetch_result[0]


@app.post("/user/")
def add_user(user_name: str, user_role: str = "user") -> dict:
    max_id = max(usr.get("id") for usr in db_mock["users"])

    new_user = {"id": max_id + 1, "user_name": user_name, "role": user_role}
    db_mock["users"].append(new_user)

    return new_user


@app.patch("/user/{user_id}")
def set_user_role(user_id: int, user_role: str) -> dict:
    fetch_result = [usr for usr in db_mock["users"] if usr.get("id") == user_id]

    if len(fetch_result) == 0:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    fetch_result[0]["role"] = user_role

    return fetch_result[0]



@app.get("/operation")
def get_operations(currency: str = "KZT") -> list[dict]:
    fetch_result = [oper for oper in db_mock["operations"] if oper["currency"] == currency]

    return fetch_result


class StockOperation(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=10)
    amount: int = Field(ge=0)


@app.post("/operation")
def add_operations(operation_list: List[StockOperation])-> List[int]:
    id = max([oper.get("id") for oper in db_mock["operations"]])
    added_ids = []

    for op in operation_list:
        id += 1
        added_ids.append(id)
        op.id = id
        db_mock["operations"].append(dict(op))
    
    print("DEBUG:")
    print(db_mock["operations"])
    
    return added_ids



class SecurityTypes(Enum):
    DEBT = "DEBT"
    EQUITY = "EQUITY"
    HYBRID = "HYBRID"

class CreditRatings(Enum):
    AAA = "AAA"
    AA = "AA"
    A = "A"
    BBB = "BBB"
    BB = "BB"
    B = "B"
    CCC = "CCC"
    CC = "CC"
    C = "C"
    D = "D"


class Publisher(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(max_length=30)
    full_name: str = Field(max_length=200)

class RatingAgency(BaseModel):
    id: int = Field(ge=0)
    name: str = Field(max_length=100)

class RatingRecord(BaseModel):
    rating_agency: RatingAgency
    credit_rating: CreditRatings
    date: datetime

class Security(BaseModel):
    id: int = Field(ge=0)
    type: SecurityTypes
    publisher: Publisher
    ratings: Optional[List[RatingRecord]]


# s = Security(id=0, type=SecurityTypes.EQUITY, 
#              publisher=Publisher(id=0, name="IBM", full_name="IBM Inc."), 
#              ratings=[RatingRecord(rating_agency=RatingAgency(id=0, name="Barclays"),
#                                    credit_rating=CreditRatings.BB, 
#                                    date=datetime.now())])
db_securities: list[Security] = []

@app.post("/securities", response_model=Security)
def add_security(sequriry: Security):
    ids = list([sec.id for sec in db_securities])
    print("DEBUG", ids)
    max_id = max([-1] + ids)

    sequriry.id = max_id + 1
    db_securities.append(sequriry)

    return sequriry





@app.get("/version")
def app_version():
    return "LP Tech LLC RESTfull API (version 0.1)"