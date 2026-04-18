from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
import io
import os

# ✅ Fix model path (prevents repeated download)
os.environ["U2NET_HOME"] = "/opt/render/project/src/models"

app = FastAPI()

# ✅ Use lightweight model (very important for Render free)
session = new_session("u2netp")

@app.get("/")
def root():
    return {"message": "Server running"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    input_bytes = await file.read()

    # ✅ Use session here
    output_bytes = remove(input_bytes, session=session)

    return StreamingResponse(
        io.BytesIO(output_bytes),
        media_type="image/png"
    )
