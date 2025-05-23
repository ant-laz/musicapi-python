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

###############################################################################
# Note on python package & module structure 
# main.py is within the directory app
# because the directory app has a emtpy __init__.py file it is a Python package called "app"
# because of this, main.py is a "Python module" of "Python package" app. It is reffered to via app.main
###############################################################################

from fastapi import FastAPI, Response
from fastapi.params import Depends

from app.db.base import get_db_engine, get_db_metadata, get_info_tbl_with_1_col_pk, get_page_of_data

# Create an instance of the FastAPI class
musicapi = FastAPI()

###############################################################################
# API Health Check
# ---------------------
###############################################################################
@musicapi.get("/")
def healthcheck():
    return Response("server is running")    

###############################################################################
# Basic API with SQL Alchemy ORM & cursor based pagination
# ---------------------
# Uses the Google created spanner dialect for SQLAlchemy
# https://github.com/googleapis/python-spanner-sqlalchemy
###############################################################################
@musicapi.get("/api/v1/singers")
def fetch_all_singers(cursor: int, page_size: int, engine = Depends(get_db_engine), metadata = Depends(get_db_metadata)):
    
    tbl_name: str = "Singers"
    tbl, pk_col, pk_col_name = get_info_tbl_with_1_col_pk(tbl_name, metadata)
    data: dict = get_page_of_data(engine, tbl, pk_col, pk_col_name, cursor, page_size)
    return data

@musicapi.get("/api/v1/albums")
def fetch_all_albums(cursor: int, page_size: int, engine = Depends(get_db_engine), metadata = Depends(get_db_metadata)):

    tbl_name: str = "Albums"
    tbl, pk_col, pk_col_name = get_info_tbl_with_1_col_pk(tbl_name, metadata)
    data: dict = get_page_of_data(engine, tbl, pk_col, pk_col_name, cursor, page_size)
    return data

@musicapi.get("/api/v1/labels")
def fetch_all_labels(cursor: int, page_size: int, engine = Depends(get_db_engine), metadata = Depends(get_db_metadata)):
    tbl_name: str = "Labels"
    tbl, pk_col, pk_col_name = get_info_tbl_with_1_col_pk(tbl_name, metadata)
    data: dict = get_page_of_data(engine, tbl, pk_col, pk_col_name, cursor, page_size)
    return data