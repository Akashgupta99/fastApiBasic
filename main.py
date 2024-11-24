from fastapi import FastAPI, Request, HTTPException
import pandas as pd
import os.path, sys
import requests

app = FastAPI()

currentDirectory = os.getcwd()

@app.get("/")
async def read_root():
    return {"Hello": "World"}



@app.get("/book/{id}")
async def get_book(id: str):
    files = []
    for (_, _, filenames) in os.walk(f"{currentDirectory}/{id}"):
        files.extend(filenames)

    df = pd.read_csv(f"{currentDirectory}/{id}/{files[0]}")
    return df.to_dict(orient="list")


@app.post("/book/{id}")
async def place_book(id: str, request: Request):
    try:
        requestBody = await request.json()
        if all(key in requestBody.keys() for key in ("name", "data")):
            filePath = f"{currentDirectory}/{id}"
            df = pd.DataFrame(requestBody.get("data"))
            fileName = requestBody.get("name")
            if not os.path.exists(filePath):
                os.mkdir(filePath)
            else:
                with os.scandir(filePath) as it:
                    if any(it):
                        return {"answer": "File is present for this id"}
                    else:
                        print("empty")

            df.to_csv(f"{filePath}/{fileName}", index=False)

            return {"msg": "done"}
        else:
            raise Exception("Please make sure 'name' and 'data' keys are present")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        raise HTTPException(status_code=500, detail=f"Save not success, {repr(e)}, {exc_tb.tb_lineno}")
    

@app.put("/book/{id}")
async def update_book(id: str, request: Request):
    requestBody = await request.json()
    filePath = f"{currentDirectory}/{id}"
    df_data = requests.get(f"http://localhost:8000/book/{id}")
    df = pd.DataFrame(df_data)
    return {"done": "done"}
    
    
    