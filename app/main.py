#    Copyright 2025 Google LLC
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import os

from fastapi import FastAPI, Response

from google.cloud import spanner

from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.orm import Session

# Create an instance of the FastAPI class
musicapi = FastAPI()

###############################################################################
# 0. API Health Check
# ---------------------
# create a path (aka endpoint or route) + operation
# path is the base path "/"
# operation is one of the HTTP methods, in this case GET
# the "@" is a python decorator that tells Fast API the "root" method is for GET operations on "/"
# this endpoint is a "health check" to allow developers to assess if deployemnts have been successful
###############################################################################
@musicapi.get("/")
def healthcheck():
    return Response("server is running")

###############################################################################
# 1. Basic API with hard written SQL, no pagination, use python spanner library
###############################################################################
@musicapi.get("/api/v1/singers")
def fetch_all_singers():
    # need to fetch my spanner instance ID
    instanceid = os.environ["SPANNER_INSTANCE_ID"]

    # need to fetch my spanner database ID
    databaseid = os.environ["SPANNER_DATABASE_ID"]

    # Instantiate a client.
    spanner_client = spanner.Client()
    
    # Get a Cloud Spanner instance by ID.
    instance = spanner_client.instance(instanceid)
    
    # Get a Cloud Spanner database by ID.
    database = instance.database(databaseid)

    singer_data = {}
    singer_data["singers"] = []

    # Execute a simple SQL statement.
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT SingerId, FirstName, LastName, BirthDate FROM Singers"
        )

        for row in results:
            id, firstname, lastname, dateofbirth = row
            this_singer = {"id": id, "firstname": firstname, "lastname": lastname, "dateofbirth": dateofbirth}
            singer_data["singers"].append(this_singer)

    return singer_data

###############################################################################
# 2. Basic API with hard written SQL, cursor based pagination & py spanner lib
###############################################################################
@musicapi.get("/api/v2/singers")
def fetch_all_singers_paginated(cursor: int, page_size: int):
    # need to fetch my spanner instance ID
    instanceid = os.environ["SPANNER_INSTANCE_ID"]

    # need to fetch my spanner database ID
    databaseid = os.environ["SPANNER_DATABASE_ID"]

    # Instantiate a client.
    spanner_client = spanner.Client()
    
    # Get a Cloud Spanner instance by ID.
    instance = spanner_client.instance(instanceid)
    
    # Get a Cloud Spanner database by ID.
    database = instance.database(databaseid)

    singer_data = {}
    singer_data["singers"] = []
    singer_data["next_cursor"] = ""

    # Execute a simple SQL statement.
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            f"SELECT SingerId, FirstName, LastName, BirthDate FROM Singers WHERE SingerId >= {cursor} ORDER BY SingerId LIMIT {page_size}"
        )

        for row in results:
            id, firstname, lastname, dateofbirth = row
            this_singer = {"id": id, "firstname": firstname, "lastname": lastname, "dateofbirth": dateofbirth}
            singer_data["singers"].append(this_singer)
            singer_data["next_cursor"] = int(id)+1

    return singer_data

###############################################################################
# 2. Basic API with SQL Alchemy ORM & cursor based pagination
# ---------------------
# Uses the Google created spanner dialect for SQLAlchemy
# https://github.com/googleapis/python-spanner-sqlalchemy
###############################################################################
@musicapi.get("/api/v3/singers")
def fetch_all_singers_paginated_sqlalchemy(cursor: int, page_size: int):

    # fetch environment variables to tell SQLAlchemy where to find our DB
    instanceid = os.environ["SPANNER_INSTANCE_ID"]
    databaseid = os.environ["SPANNER_DATABASE_ID"]
    projectid = os.environ["GOOGLE_CLOUD_PROJECT"]

    # The start of any SQLAlchemy application is an object called the Engine. 
    # This object acts as a central source of connections to a particular database
    # echo=True instructs the Engine to log all of the SQL it emits to a Python logger that will write to sout
    engine = create_engine(
        f"spanner+spanner:///projects/{projectid}/instances/{instanceid}/databases/{databaseid}",
        echo=True
    )
    
    # Database metadata refers to objects that represnt Tables & Columns
    # MetaData is a collection (e.g. py dict) that stores Tables
    # table = Table("Singers", MetaData(bind=engine), autoload=True)
    metadata_obj = MetaData()

    # Once we have a MetaData object, we can declare some Table objects
    # We use a feature of SQLAlchemy called table reflection to reduce code required
    # Table reflection refers to the process of generating Table 
    # and related objects by reading the current state of a database. 
    # This way we avoid hardcoding Table schema which can go out of date !
    singers_table = Table("Singers", metadata_obj, autoload_with=engine)
    
    # create a container to store the information fetched from the db
    # set default value of "next_cursor" to current cursor to handle
    # edge case when we have reached the end of the data in the db
    data = {"records":[], "next_cursor": cursor}

    # Using a session, first create a select statement
    # implement cursor based pagination used the provided cursor & page_size provided in the api call
    # parse the result set into a json object which can be returned
    with Session(engine) as session:
        stmt = select(singers_table).where(singers_table.c.SingerId >= cursor).order_by(singers_table.c.SingerId.asc()).limit(page_size)
        result = session.execute(stmt)
        for row in result:
            data["records"].append(row._asdict())
            data["next_cursor"] = int(row.SingerId)+1

    return data