from skimage import img_as_float
from skimage import io, color, morphology
import matplotlib.pyplot as plt
import matplotlib,os
from PIL import Image


for file in os.listdir("train_data\\Base-Data\\"):
	image = img_as_float(color.rgb2gray(io.imread("train_data\\Base-Data\\"+file)))
	image_binary = image < 0.5
	out_skeletonize = morphology.skeletonize(image_binary)
	out_thin = morphology.thin(image_binary)
	matplotlib.image.imsave("train_data\\Base-Data\\"+file[:-4]+'-p.jpg', out_thin,cmap='gray')
	os.remove("train_data\\Base-Data\\"+file)
