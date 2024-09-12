import unittest
import sys
sys.path.append("E:/NewProject/code/")
from unittest.mock import patch, MagicMock
from predict import PredictFactory

# 模拟YOLO类和predict方法
class MockYOLO:
    def __init__(self, model_path):
        pass

    def predict(self, source, half, device):
        return MockResult()

class MockResult:
    def __init__(self):
        pass

    def plot(self):
        return 'image_array'
    
# 测试PredictFactory类
class TestPredictFactory(unittest.TestCase):
    @patch('predict.YOLO', new=MockYOLO)
    def setUp(self):
        self.predict_factory = PredictFactory('test_factory')

    def test_get_first_model(self):
        # 模拟os.listdir返回值
        with patch('os.listdir', return_value=['model1.pt', 'model2.pt']):
            first_model = self.predict_factory.get_first_model()
            self.assertIn('.pt', first_model)

    def test_get_first_model_ng(self):
        # 模拟os.listdir返回值
        with patch('os.listdir', return_value=['model1.onxx', 'model2.onxx']):
            first_model = self.predict_factory.get_first_model()
            self.assertIs(first_model,None)

    def test_load_model(self):
        # 测试load_model方法是否正确调用YOLO
        with patch('predict.YOLO') as mock_yolo:
            self.predict_factory.load_model('path/to/model.pt')
            mock_yolo.assert_called_with('path/to/model.pt')

    def test_predict(self):
        # 测试predict方法返回值
        result = self.predict_factory.predict('path/to/image.jpg')
        self.assertIsInstance(result, type(MockResult()))

    def test_get_plotted_image(self):
        # 测试get_plotted_image方法返回值
        result = self.predict_factory.get_plotted_image(MockResult())
        self.assertEqual(result, 'image_array')

if __name__ == '__main__':
    unittest.main()
