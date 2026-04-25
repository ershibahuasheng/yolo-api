from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import numpy as np
from PIL import Image
import io
import os

app = FastAPI(title="YOLO API")

# 延迟加载模型
model = None

def get_model():
    global model
    if model is None:
        from ultralytics import YOLO
        print("Loading YOLO model...")
        model = YOLO('yolov8n.pt')
        print("Model loaded!")
    return model

@app.get("/")
async def root():
    return {"message": "YOLO API is running", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # 读取图片
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        img = np.array(image)
        
        # 获取模型并预测
        model = get_model()
        results = model(img)
        
        # 提取结果
        detections = []
        for r in results:
            if r.boxes:
                for box in r.boxes:
                    conf = float(box.conf[0])
                    cls = int(box.cls[0])
                    name = model.names[cls]
                    detections.append([name, conf])
        
        return JSONResponse(content=detections)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
