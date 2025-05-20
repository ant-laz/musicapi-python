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
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

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

# Dependency to get the database engine
def get_db_engine() -> Engine:
    return engine