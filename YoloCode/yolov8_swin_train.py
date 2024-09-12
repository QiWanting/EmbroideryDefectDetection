from ultralytics import YOLO

# Load a model
# model = YOLO('yolov8s.yaml')  # build a new model from YAML
model = YOLO('E:/NewProject/code/ultralytics/cfg/models/v8/yolov8_three_swinTrans.yaml')  # load a pretrained model (recommended for training)
# model = YOLO('yolov8s.yaml').load('yolov8s.pt')  # build from YAML and transfer weights

# Train the model
if __name__ == '__main__':
    model.train(data='./data/defect.yaml', pretrained='./model/yolov8x.pt', epochs=400, imgsz=640, batch=16,device='0')
