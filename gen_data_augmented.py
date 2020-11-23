from PIL import  Image
import os, glob
import numpy as np
from sklearn import model_selection

classes = ['monkey', 'boar', 'crow']
num_classes = len(classes)
image_size = 50
num_testdata = 100

x_train = []
x_test = []
y_train = []
y_test = []

for index, class_label in enumerate(classes):
    photos_dir = '/work/' + class_label
    files = glob.glob(photos_dir + '/*.jpg')
    for i, file_name in enumerate(files):
        if i >= 200:
            break
        image = Image.open(file_name)
        image = image.convert('RGB')
        image = image.resize((image_size, image_size))

        data = np.asarray(image)
        if i < num_testdata:
            x_test.append(data)
            y_test.append(index)
        else:
            x_train.append(data)
            y_train.append(index)

            for angle in range(-20, 20, 5):
                #rotation
                image_roll = image.rotate(angle)
                data = np.asarray(image_roll)
                x_train.append(data)
                y_train.append(index)

                #transpose
                img_transpose = image_roll.transpose(Image.FLIP_LEFT_RIGHT)
                data = np.asarray(img_transpose)
                x_train.append(data)
                y_train.append(index)

x_train = np.asarray(x_train)
x_test = np.asarray(x_test)
y_train = np.asarray(y_train)
y_test = np.asarray(y_test)


xy_data = (x_train, x_test, y_train, y_test)
np.save('/work/animal_aug.npy', xy_data)
