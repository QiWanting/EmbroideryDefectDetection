import os
import shutil
train_txt_path = "E:/NewProject/code/data/val.txt"
with open(train_txt_path, 'r', encoding='utf-8') as file:
    for line in file:
        file_name = line[line.find("/",5)+1:].strip()[:-3]+("txt")
        print(file_name)
        image_orgin_path = "E:/NewProject/code/data/labels"
        file_save_path = "E:/NewProject/code/data/labels/val"
        shutil.copy(os.path.join(image_orgin_path,file_name), os.path.join(file_save_path,file_name))