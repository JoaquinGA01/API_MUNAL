from fastapi import FastAPI, File, UploadFile
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
from fastapi.responses import JSONResponse
import base64

app = FastAPI(
    title="API_MUNAL",
    version="1.0.0.0",
    docs_url = "/api/docs",
    redoc_url= "/api/docs"
)

# Conectamos a MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["API_MUNAL"]
models = db["Models"]

@app.post("/fbx")
async def upload_fbx(file: UploadFile = File(...),title: str = None, info: str = None):
    # guardar el archivo en la base de datos
    fbx_file = file.file.read()
    fbx_file_id = await models.insert_one({
        "name": file.filename,
        "data": base64.b64encode(fbx_file),
        "title": title,
        "info": info
    })
    
    return JSONResponse({"message": f"Archivo FBX con id {fbx_file_id} subido correctamente"})



# Consultamos el archivo FBX desde FastAPI
@app.get("/fbx/{file_id}")
async def get_fbx(file_id: str):
    # buscar el archivo por ID en la colección
    result = await models.find_one({"_id": ObjectId(file_id)})
    if result:
        file_data = result["title"]
        extra_info = result["info"]
        filee = result["data"]
        # Aquí se puede trabajar con el archivo FBX y la información extra encontrada

        return {"file_data": file_data, "extra_info": extra_info, "file":base64.b64encode(filee)}
    else:
        return {"error": "File not found"}
