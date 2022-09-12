import numpy as np
import pickle
import xgboost
import sklearn
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
weather_model = pickle.load(open(filename1, 'rb'))
county_dict2 = pickle.load(open(filename2, 'rb'))
a = np.array([[1917, 57]])
print(weather_model.predict(a))
print(county_dict2)
