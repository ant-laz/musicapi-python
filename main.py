from fastapi import FastAPI

# Create an instance of the FastAPI class
app = FastAPI()

# create a path (aka endpoint or route) + operation
# path is the base path "/"
# operation is one of the HTTP methods, in this case GET
# the "@" is a python decorator that tells Fast API the "root" method is for GET operations on "/"
@app.get("/")
def root():
    return {"message": "Hello World"}