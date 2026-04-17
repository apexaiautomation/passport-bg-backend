from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://apex-passport-photo.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Server running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    try:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Please upload an image file.")

        input_bytes = await file.read()
        if not input_bytes:
            raise HTTPException(status_code=400, detail="Empty file uploaded.")

        from rembg import remove
        output_bytes = remove(input_bytes)

        return StreamingResponse(
            io.BytesIO(output_bytes),
            media_type="image/png"
        )

    except HTTPException:
        raise
    except Exception as e:
        print("REMOVE_BG_ERROR:", str(e))
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
