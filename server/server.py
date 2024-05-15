from fastapi import FastAPI, File, UploadFile, HTTPException, status, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from parser import parserDutchStyleLife, parse_response, get_semantic
from search import get_mask
from motor.motor_asyncio import AsyncIOMotorClient
import tensorflow as tf
from tensorflow import keras

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

IMAGE_SIZE = 512
IMAGE_SEND_SIZE = 256

async def db_connection():
    try:
        client = AsyncIOMotorClient('mongodb://database:27017')
        db = client.dutchStyleLife
        return db.symbol
    except Exception as e:
        raise HTTPException(status_code=500, detail="Connection to Database Error")

@app.get('/')
async def hello():
    return 'Welcome to the DutchStileLife server!'

@app.get('/refresh_db')
async def refresh_db():
    try:
        exelList = parserDutchStyleLife()
        if exelList == 'Parser Error':
            return {"detail": "Parser error occurred"}, status.HTTP_400_BAD_REQUEST
        keys, count = exelList.keys(), 0
        coll = await db_connection()
        await coll.delete_many({})
        for key in keys:
            await coll.insert_one({'_id': count, key: exelList[key]})
            count += 1
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return 'Success'

@app.get('/list_of_segments')
async def list_of_segments(id: str):
    coll = await db_connection()
    response = await parse_response(coll, id)
    return JSONResponse(content=response)

@app.post('/list_of_symbols')
async def list_of_symbols(id: int = Query(...), files: List[UploadFile] = File(...)):
    try:
        coll = await db_connection()
        response = []
        for file in files:
            image_content = await file.read()
            image_tensor = tf.io.decode_png(image_content, channels=3)
            image_tensor.set_shape([None, None, 3])
            image_tensor = tf.image.resize(image_tensor, [IMAGE_SIZE, IMAGE_SIZE])
            if id != -1 and id < len(models):
                image_masks, image_classes = get_mask([models[id]], image_tensor)
            else:
                image_masks, image_classes = get_mask(models, image_tensor)
            image_tensor = tf.image.resize(image_tensor, [IMAGE_SEND_SIZE, IMAGE_SEND_SIZE])
            image_tensor = image_tensor.numpy().tolist()
            image_classes = await get_semantic(coll, id, image_classes)
            response.append({"image": image_tensor, "image_masks": image_masks, "list_of_symbols": image_classes})
        return JSONResponse(content=response)
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})

model_table = keras.models.load_model('./models/model_table')
model_flower = keras.models.load_model('./models/model_flower')
model_skeleton = keras.models.load_model('./models/model_skeleton')
models = [model_table, model_flower, model_skeleton]