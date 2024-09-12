import unittest
from fastapi.testclient import TestClient
import sys
sys.path.append("E:/NewProject/code/")
from api import app

# 创建 FastAPI 应用的测试客户端
client = TestClient(app)

# 读取图片
neu_test_image_path = r"E:\NewProject\code\data\images\test\inclusion_63.jpg"
dagm_test_image_path = r"dataset\DAGM2007_txt\images\val\000024.jpg"

class TestFastAPI(unittest.TestCase):
    def test_predict_image_neu(self):
        # 测试 NEU 检测类型的预测接口
        with open(neu_test_image_path,"rb") as image:
            response = client.post(
                "/predict_image/NEU",
                files={"file": ("image_name",image)}
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("plotted_image", response.json())

    def test_predict_image_dagm(self):
        # 测试 DAGM 检测类型的预测接口
        with open(dagm_test_image_path,"rb") as image:
            response = client.post(
                "/predict_image/DAGM",
                files={"file": ("image_name",image)}
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn("plotted_image", response.json())

    def test_predict_image_invalid_type(self):
        # 测试无效检测类型的情况
        with open(neu_test_image_path,"rb") as image:
            response = client.post(
                "/predict_image/INVALID_TYPE",
                files={"file": ("image_name",image)}
            )
            self.assertEqual(response.status_code, 400)

    def test_predict_image_no_file(self):
        # 测试没有文件上传的情况
        response = client.post("/predict_image/NEU")
        self.assertEqual(response.status_code, 422)

if __name__ == '__main__':
    unittest.main()
