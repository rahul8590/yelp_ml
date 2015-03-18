import pandas as pd
import numpy as np
import datetime 
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelBinarizer, MinMaxScaler


def get_df(ifile):
  df                = pd.read_csv(ifile)
  df['year']        = df['datetime'].apply(lambda x : int(x.split()[0].split('-')[0]))
  df['month']       = df['datetime'].apply(lambda x : int(x.split()[0].split('-')[1]))
  df['day']         = df['datetime'].apply(lambda x : int(x.split()[0].split('-')[2]))
  df['hh']          = df['datetime'].apply(lambda x : int(x.split()[1].split(':')[0]))
  df['day-of-week'] = df.apply(lambda row : int(datetime.date(int(row['year']), int(row['month']), int(row['day'])).weekday()), axis=1)
  df['time-of-day'] = df.apply(lambda row : int( int(row['day'])/2), axis=1)
  df['week-no']     = df.apply(lambda row : int(datetime.date(int(row['year']), int(row['month']), int(row['day'])).isocalendar()[1]), axis=1)
  df['temp']        = df['temp'].apply(lambda x : int(x+0.5))
  df['atemp']       = df['atemp'].apply(lambda x : int(x+0.5))
  df['windspeed']   = df['windspeed'].apply(lambda x : int(x+0.5))
  df['humidity']    = df['humidity'].apply(lambda x : int(x + 0.5))
  return df



### apply transformation and create numpy datafiles
X_mapper = DataFrameMapper([('year', LabelBinarizer()), ('month', LabelBinarizer()),
      ('temp', MinMaxScaler()), ('atemp', MinMaxScaler()), ('windspeed', MinMaxScaler()), ('humidity', MinMaxScaler()), 
      ('season', LabelBinarizer()), ('weather', LabelBinarizer()), ('holiday', LabelBinarizer()), ('workingday', LabelBinarizer())])
for ifile, ofile, train in [('train.csv', 'train.npy', True), ('test.csv', 'test_distribute.npy', False)]:
  df = get_df(ifile)    
  X  = np.round(X_mapper.fit_transform(df), 2) if train else np.round(X_mapper.transform(df), 2)
  print "# of samples X # of features", X.shape[0], X.shape[1] 
  if train is False:
      df['count'] = df['year'].apply(lambda x : 0)
  Y    = df[['count', 'casual', 'registered']].as_matrix() if train else df[['count', 'datetime']].as_matrix()
  X_uc = df[['day', 'hh', 'day-of-week']].as_matrix()
  XY   = np.hstack((Y, X))
  XY   = np.hstack((XY, X_uc))
  np.save(ofile, XY)

