import os,keras
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

datagen = ImageDataGenerator(
    featurewise_center=True,
    featurewise_std_normalization=True,
    rotation_range=10,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True)

for file in os.listdir("train_data\\Base-Data\\BlurredImages\\ResultImages\\"):
	print(file)
	name= "train_data\\Base-Data\\BlurredImages\\ResultImages\\"+file
	img = load_img(name)  # this is a PIL image
	x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
	x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, 3, 150, 150)

	# the .flow() command below generates batches of randomly transformed images
	# and saves the results to the `preview/` directory
	i = 0
	for batch in datagen.flow(x, batch_size=1,
                          save_to_dir='train_data\\Base-Data\\BlurredImages\\ResultImages',save_prefix=os.path.basename(file)[:-4], save_format='jpg'):
			i += 1
			if i >=1:
				break  # otherwise the generator would loop indefinitely
	
	
	
