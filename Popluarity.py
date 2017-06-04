import pandas as pd
from sklearn import linear_model

class Popularity(object):
  def __init__(self, csv):
    self.dataTrain = pd.read_csv(csv)
    # self.dataTest = pd.read_csv(r'/Users/taichikato/Desktop/InstaPopular/Testdata.csv')
  def popularity(self):
    x_train = self.dataTrain[['NCP', 'NFC']].values.reshape(-1,2)
    y_train = self.dataTrain['P']
    x_test = self.dataTest[['NCP', 'NFC']].values.reshape(-1,2)
    print('x_test \n')
    print(x_test)
    ols = linear_model.LinearRegression()
    model = ols.fit(x_train, y_train)
    print(model.predict(x_test)[0:12])
p = Popularity(r'/Users/taichikato/Desktop/InstaPopular/Dataset.csv')
p.popularity()