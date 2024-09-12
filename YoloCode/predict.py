import os
from ultralytics import YOLO
project_dir=os.path.dirname(os.path.abspath(__file__))
default_model_path = os.path.join(project_dir,"model")
default_save_path = os.path.join(project_dir,"temp")
model_types = (".pt")
class PredictFactory():
    model = None
    def __init__(self, name):
        self.name = name
        self.load_model(self.get_first_model())

    def get_first_model(self):
        """
        获取目录下的第一个模型

        Returns:
            string: the first model path.

        """
        for file_name in os.listdir(default_model_path):
            if(os.path.splitext(file_name)[-1] in model_types):
                return os.path.join(default_model_path,file_name)
        return
    
    def load_model(self,model_path):
        """
        加载模型

        Args:
            model_path: load model path

        """
        self.model = YOLO(model_path)

    def predict(self,image_path):
        """
        预测一个图像

        Args:
            image_path: image path.

        Returns:
            result: predict result.

        """
        return self.model.predict(source=image_path,half=True,device=0)
    
    def get_plotted_image(self,result):
        """
        从预测结果中返回绘制的图像

        Args:
            result: predict result.

        Returns:
            im_array: image np array.

        """
        im_array = result.plot()
        return im_array

predict_factory = PredictFactory("predict_factory")