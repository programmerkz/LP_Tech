from fastapi import FastAPI


app = FastAPI()


@app.get("/version")
def app_version():
    return "LP Tech LLC RESTfull API (version 0.1)"