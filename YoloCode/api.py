from fastapi import FastAPI, File, UploadFile, HTTPException, Path
from fastapi.responses import JSONResponse
import uvicorn
from PIL import Image
import io
import os
import numpy as np
import cv2
import base64
from predict import predict_factory

project_dir=os.path.dirname(os.path.abspath(__file__))
NEU_MODEL_PATH = r"model/NEU_n_751_DCV2.pt"
DAGM_MODEL_PATH = r"model/DAGM_n_991_DCV2.pt"

app = FastAPI()

@app.post("/predict_image/{detection_type}")
async def predict_image(detection_type: str = Path(..., title="检测类型", description="请输入NEU或DAGM作为检测类型"), file: UploadFile = File(...)):
    if detection_type not in ["NEU", "DAGM"]:
        raise HTTPException(status_code=400, detail="检测类型必须是NEU或DAGM")
    if not file:
        raise HTTPException(status_code=400, detail="没有收到图片文件")   
    try:
        image = Image.open(io.BytesIO(await file.read()))

        # 切换模型
        predict_factory.load_model(os.path.join(project_dir,eval(detection_type+"_MODEL_PATH")))
        # 预测
        result = predict_factory.predict(image)

        # 转换图片为base64格式
         # 使用OpenCV将ndarray转换为PNG格式的图片
        _, encoded_image = cv2.imencode('.png', predict_factory.get_plotted_image(result[0]))
        # 将编码后的图片转换为Base64编码的字符串
        image_base64 = base64.b64encode(encoded_image.tobytes()).decode('utf-8')

        # 假设处理后的图片信息和其他信息如下
        processed_image_info = {
            "verbose": result[0].verbose(),
            "speed": result[0].speed,
            "info": result[0].tojson(),
            "plotted_image":image_base64
        }

        # 返回处理后的图片信息和其他信息
        return JSONResponse(content=processed_image_info)
    except Exception as e:
        # 如果在处理图片时发生错误，返回错误信息
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
