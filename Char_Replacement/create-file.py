import os,json
import cv2
# import thinning_algorithm
import numpy as np


f=open("rn_input.json-bun","wt")

dict={"size":5,"letters":[]}
def load_image(imagename):
    img = cv2.imread(imagename, 0)
    img = np.asarray(img, dtype="float32")
    img = img.reshape(784)
    return img

def write_in_file(dict,image_path):
    image = load_image(image_path)
    image = image.astype('float32')
    image /= 255
    dict["letters"].append(image.tolist())
    print(image.tolist())

image1_path="D:\\[IA]\\sapt13\\OCR-manuscripts\\train_data\\Base-Data\\BlurredImages\\ResultImages\\0001-0-1.jpg"
image2_path="D:\\[IA]\\sapt13\\OCR-manuscripts\\train_data\\Base-Data\\BlurredImages\\ResultImages\\0101-0-1.jpg"
image3_path="D:\\[IA]\\sapt13\\OCR-manuscripts\\train_data\\Base-Data\\BlurredImages\\ResultImages\\0111-0-1.jpg"
image4_path="D:\\[IA]\\sapt13\\OCR-manuscripts\\train_data\\Base-Data\\BlurredImages\\ResultImages\\0112-0-662.jpg"
image5_path="D:\\[IA]\\sapt13\\OCR-manuscripts\\train_data\\Base-Data\\BlurredImages\\ResultImages\\0961-0-1.jpg"
write_in_file(dict,image1_path)
write_in_file(dict,image2_path)
write_in_file(dict,image3_path)
write_in_file(dict,image4_path)
write_in_file(dict,image5_path)
json.dump(dict,f,indent=2)
f.close()