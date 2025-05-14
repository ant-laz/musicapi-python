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

# Create an instance of the FastAPI class
musicapi = FastAPI()

# create a path (aka endpoint or route) + operation
# path is the base path "/"
# operation is one of the HTTP methods, in this case GET
# the "@" is a python decorator that tells Fast API the "root" method is for GET operations on "/"
# this endpoint is a "health check" to allow developers to assess if deployemnts have been successful
@musicapi.get("/")
def healthcheck():
    return Response("server is running")

# get all singers
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

# get all singers using cursor based pagination
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

# get a specific singer by ID
@musicapi.get("/api/v1/singers/{singer_id}")
def fetch_singer_by_id(singer_id: int):
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
            f"SELECT SingerId, FirstName, LastName, BirthDate FROM Singers WHERE SingerId = {singer_id}"
        )

        for row in results:
            id, firstname, lastname, dateofbirth = row
            this_singer = {"id": id, "firstname": firstname, "lastname": lastname, "dateofbirth": dateofbirth}
            singer_data["singers"].append(this_singer)

    return singer_data