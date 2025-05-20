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
# This file app/db/base.py is inside a sub-package, app/db/, so, it's a submodule: app.db.base.
###############################################################################

import os
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.engine import Engine
from sqlalchemy.schema import Table, Column
from sqlalchemy.orm import Session

# fetch environment variables to tell SQLAlchemy where to find our DB
instanceid = os.environ["SPANNER_INSTANCE_ID"]
databaseid = os.environ["SPANNER_DATABASE_ID"]
projectid = os.environ["GOOGLE_CLOUD_PROJECT"]

# The start of any SQLAlchemy application is an object called the Engine. 
# This object acts as a central source of connections to a particular database
# echo=True instructs the Engine to log all of the SQL it emits to a Python logger that will write to sout
engine: Engine = create_engine(
    f"spanner+spanner:///projects/{projectid}/instances/{instanceid}/databases/{databaseid}",
    echo=True
)

# Database metadata refers to objects that represnt Tables & Columns
# MetaData is a collection (e.g. py dict) that stores Tables
# table = Table("Singers", MetaData(bind=engine), autoload=True)
metadata_obj: MetaData = MetaData()

# Once we have a MetaData object, we can declare some Table objects
# We use a feature of SQLAlchemy called table reflection to reduce code required
# Table reflection refers to the process of generating Table 
# and related objects by reading the current state of a database. 
# This way we avoid hardcoding Table schema which can go out of date !
# The following code fetches metadata about all tables in our databse
# ref : 
# https://docs.sqlalchemy.org/en/20/core/reflection.html#reflecting-all-tables-at-once
metadata_obj.reflect(bind=engine)

# Dependency to get the database engine
def get_db_engine() -> Engine:
    return engine

def get_db_metadata() -> MetaData: 
    return metadata_obj

def get_info_tbl_with_1_col_pk(table_name: str, metadata: MetaData):
    my_table: Table = metadata_obj.tables[table_name]
    my_table_pk_column: Column = my_table.primary_key.columns[0]
    my_table_pk_column_name: str = my_table_pk_column.name 
    return (my_table, my_table_pk_column, my_table_pk_column_name)

def get_page_of_data(engine: Engine, tbl: Table, pk_col: Column, pk_col_name: str, cursor: int, page_size: int):
    # create a container to store the information fetched from the db
    # # set default value of "next_cursor" to current cursor to handle
    # # edge case when we have reached the end of the data in the db
    data = {"records":[], "next_cursor": cursor}
    
    # Using a session, first create a select statement
    # # implement cursor based pagination used the provided cursor & page_size provided in the api call
    # # parse the result set into a json object which can be returned
    with Session(engine) as session:
        stmt = (select(tbl)
                .where(pk_col >= cursor)
                .order_by(pk_col.asc())
                .limit(page_size))
        result = session.execute(stmt)
        for row in result:
            this_row: dict = row._asdict()
            data["records"].append(this_row)
            data["next_cursor"] = int(this_row[pk_col_name])+1
    
    return data