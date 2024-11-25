from fastapi import FastAPI, Request, HTTPException
import pandas as pd
import os.path, sys
import grequests

app = FastAPI()

currentDirectory = os.getcwd()

@app.get("/")
async def read_root():
    return {"Hello": "World"}



@app.get("/book/{id}")
async def get_book(id: str):
    try:
        files = []
        print(files)
        for (dirpath, dirname, filenames) in os.walk(f"{currentDirectory}/{id}"):
            files.extend(filenames)

        df = pd.read_csv(f"{currentDirectory}/{id}/{files[0]}")
        return df.to_dict(orient="list")
    except Exception as e:
        raise HTTPException(status_code=500, details=f"There is some error, {repr(e)}")


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
    try:
        requestBody = await request.json()
        filePath = f"{currentDirectory}/{id}"
        print(filePath)
        df_data_temp = get_book(id)
        df_data = await df_data_temp.json()
        # df_data = grequests.map([df_data_temp])[0]
        print(df_data)
        # if(df_data.status_code == 500):
        #     raise Exception("There is some issue with response")
        
        df = pd.DataFrame(df_data)
        print(df)
        with os.scandir(filePath) as it:
            if any(it):
                print("file is present")
            else:
                raise Exception("File is not present for this id")
        if all(key in requestBody.keys() for key in ("name", "data", "key")):
            df2 = pd.DataFrame(requestBody.get("data"))
            fileName = requestBody.get("name")
            p_key = requestBody.get("key")
            merged_df = df.merge(df2, on=p_key, how="outer", suffixes=("_d1Xcopy", "_d2Ycopy"))
            for column in merged_df.columns:
                if(column.endswith("_d1Xcopy")):
                    x_column_name = f"{column.split('_')[0]}_d1Xcopy"
                    y_column_name = f"{column.split('_')[0]}_d2Ycopy"
                    merged_df[column.split("_")[0]] = merged_df[y_column_name].fillna(merged_df[x_column_name])
                    merged_df.drop([x_column_name, y_column_name], axis=1, inplace=True)

            merged_df.to_csv(f"{filePath}/{fileName}", index=False)
            return {"msg": "merged"}
        else:
            raise Exception("Please make sure 'name' and 'data' keys are present")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if(repr(e).endswith("keys are present")):
            raise HTTPException(status_code=400, detail=f"Save not success, {repr(e)}, {exc_tb.tb_lineno}")
        if(repr(e).startswith("file is not present")):
            raise HTTPException(status_code=404, detail=f"Save not success, {repr(e)}, {exc_tb.tb_lineno}")
        raise HTTPException(status_code=500, detail=f"Save not success, {repr(e)}, {exc_tb.tb_lineno}")

    
    
    