import os
from PIL import Image, ImageFilter
import shutil
SIZE = 28, 28
OUTPUT_DIRECTORY = 'BlurredImages'
RESULT_DIRECTORY = 'ResultImages'
def resize_images_and_blur(path):
    if not os.path.exists(path):
        print('Wrong path mate!')
        return
    if not os.path.exists(os.path.join(path, OUTPUT_DIRECTORY)):
        os.mkdir(os.path.join(path, OUTPUT_DIRECTORY))
    for file in os.listdir(path):
        basename=os.path.basename(file)[:3]
        if(os.path.splitext(file)[1].lower() == '.jpg'):
            #if ((int(basename[:2])>=10 and int(basename[:2])<=25 and basename[2]=='1') or (int(basename[:2])>25 and basename[2]=='0')):
                file_path = os.path.join(path, file)
                with Image.open(file_path) as img:
                    img = img.resize(SIZE, Image.ANTIALIAS)
                    img.save(file_path)
                with Image.open(file_path) as img:
                    for i in range(1, 6):
                        img1 = img.filter(ImageFilter.BoxBlur(i))
                        new_name = os.path.splitext(file)[0] + '-' + str(i) + os.path.splitext(file)[1]
                        img1.save(os.path.join(path, OUTPUT_DIRECTORY, new_name))
                new_name = os.path.splitext(file)[0] + '-0' + os.path.splitext(file)[1]
                shutil.move(file_path, os.path.join(path, OUTPUT_DIRECTORY, new_name))
def replicate_images(path):
    if not os.path.exists(path):
        print('Wrong path mate!')
        return
    if not os.path.exists(os.path.join(path, RESULT_DIRECTORY)):
        os.mkdir(os.path.join(path, RESULT_DIRECTORY))
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            print(file_path)
            for i in range(1, 1001):
                new_name = os.path.splitext(file)[0] + '-' + str(i) + os.path.splitext(file)[1]
                shutil.copyfile(file_path, os.path.join(path, RESULT_DIRECTORY, new_name))
            os.remove(file_path)
if __name__ == '__main__':
    resize_images_and_blur('.')
    replicate_images('./' + OUTPUT_DIRECTORY)