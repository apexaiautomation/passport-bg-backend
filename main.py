from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove, new_session
from PIL import Image
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# lighter rembg model
session = new_session("u2netp")

@app.get("/")
def root():
    return {"message": "Server running"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()

    # open uploaded image
    img = Image.open(io.BytesIO(input_bytes)).convert("RGBA")

    # resize large images to reduce memory usage
    max_size = 1000
    img.thumbnail((max_size, max_size))

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    resized_bytes = buffer.getvalue()

    # background removal with lighter model
    output_bytes = remove(resized_bytes, session=session)

    return StreamingResponse(
        io.BytesIO(output_bytes),
        media_type="image/png"
    )
    # updated for lighter model
