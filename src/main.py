from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from pathlib import Path
import cv2
import numpy as np
import shutil
from datetime import datetime


csvPath=Path("./data/logs.csv")
framePath=Path("./data/frames")

app=FastAPI()

@app.get("/")
def root():
    return {"message":"Welcome"}

@app.websocket("/uploadlog") #Client sends log and frame data
async def uploadlog(ws:WebSocket):

    await ws.accept()

    try:
        while True:

            jsonBody=await ws.receive_json() #Waits for json message
            data=await ws.receive_bytes() #waits for binary message

            log:str=jsonBody["log"]
            storeLog(log)

            # img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            imgName=datetime.now().strftime("%m_%d_%Y_%H_%M_%S_%f") + ".jpg"
            # if img!=None:
            #     cv2.imwrite(str(framePath / imgName) ,img)
            (framePath / imgName).write_bytes(data)

            await ws.send_json({"message":"Data received"})

    except WebSocketDisconnect:
        print("Connexion has ended")


def storeLog(log:str):
    with csvPath.open(mode="a") as f:
        f.write("\n" + log)
        f.close()

    
