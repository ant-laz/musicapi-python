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

from typing import Union

from fastapi import FastAPI, Response

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

@musicapi.get("/singers")
def singersfetch():
    return Response("fetching singers")