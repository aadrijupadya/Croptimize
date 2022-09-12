import numpy as np
import pickle
import xgboost
import sklearn
import PIL
from PIL import Image
from numpy import *
# import tensorflow as tf
# from tensorflow import keras
month_dict = {868: 'January',
              603: 'February',
              1079: 'March',
              57: 'April',
              1102: 'May',
              895: 'June',
              893: 'July',
              87: 'August',
              1578: 'September',
              1275: 'October',
              1261: 'November',
              491: 'December'}
filename1 = 'weather_prediction.sav'
filename2 = 'weather_county_mappings.pickle'
filename3 = 'plant_disease_model.sav'
weather_model = pickle.load(open(filename1, 'rb'))
county_dict2 = pickle.load(open(filename2, 'rb'))
# loaded_model = pickle.load(open(filename3, 'rb'))
county_dict = pickle.load(open('crop_county.sav', 'rb'))
crop_items = pickle.load(open('crop_items.sav', 'rb'))

a = np.array([[1917, 57]])


def weather_predict():
    print(weather_model.predict(a))
    print(county_dict2)


# def get_predictions(path):
#     img = tf.keras.utils.load_img(
#         path,
#         grayscale=False,
#         color_mode="rgb",
#         target_size=(250, 250),
#         interpolation="nearest"
#     )
#     input_arr = tf.keras.preprocessing.image.img_to_array(img)
#     input_arr = np.array([input_arr])

#     predictions = loaded_model.predict(input_arr)
#     predictions_list = list(predictions[0])
#     prediction = predictions_list.index(max(predictions_list))
#     return prediction


print(crop_items)

# get_predictions(
#     '/Users/aadrijupadya/Downloads/archive-3/test/test/TomatoYellowCurlVirus1.JPG')
