
import OpenBlender
from io import StringIO
import json
import web_scrapping
from auto_webscrapping import Auto_CoinTelegraph
from auto_webscrapping import Auto_CryptoNews

import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/Dehesa97/Web-Scrapping/8c403cdc9562c4b7dd53b8604e48d54de2cef9a8/data.csv')
df.head()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



df = df.reindex(index=df.index[::-1])
X = df[[ "open", "close", "volume", "market_cap", "positive", "negative","nasdaq change", "change"]]
y = df[["change"]]
y.index = y.index + 1
y2 = pd.DataFrame([0], columns = ['change'])
y = pd.concat([y2, y])
y.drop(index = y.index[-1], inplace = True)

from sklearn.preprocessing import StandardScaler, MinMaxScaler
min = MinMaxScaler()
standard = StandardScaler()

Xstan = standard.fit_transform(X)
ymm = min.fit_transform(y)

Xtrain = Xstan[1:550, :]
Xtest = Xstan[550:, :]

ytrain = ymm[1:550, :]
ytest = ymm[550:, :]

import torch
import torch.nn as nn
from torch.autograd import Variable

XTrainTensors = Variable(torch.Tensor(Xtrain))
XTestTensors = Variable(torch.Tensor(Xtest))
XTrainTensors = torch.reshape(XTrainTensors,   (XTrainTensors.shape[0], 1, XTrainTensors.shape[1]))
XTestTensors = torch.reshape(XTestTensors,  (XTestTensors.shape[0], 1, XTestTensors.shape[1]))

yTrainTensors = Variable(torch.Tensor(ytrain))
yTestTensors = Variable(torch.Tensor(ytest))

class Prediction(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length):
        super(Prediction, self).__init__()
        self.num_classes = num_classes
        self.num_layers = num_layers
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.seq_length = seq_length

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                          num_layers=num_layers, batch_first=True)
        self.fc_1 =  nn.Linear(hidden_size, 100)
        self.fc = nn.Linear(100, num_classes)

        self.relu = nn.ReLU()

    def forward(self,x):
        h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #hidden state
        c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #internal state

        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input, hidden, and internal state
        hn = hn.view(-1, self.hidden_size) #reshaping the data for Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out) #first Dense
        out = self.relu(out) #relu
        out = self.fc(out) #Final Output
        return out

num_epochs = 3000
learning_rate = 0.001
input_size = 8
hidden_size = 5
num_layers = 1
num_classes = 1

prediction = Prediction(num_classes, input_size, hidden_size, num_layers, 15)

criterion = torch.nn.MSELoss()    # mean-squared error
optimizer = torch.optim.Adam(prediction.parameters(), lr=learning_rate)

loss_plt = []

for epoch in range(num_epochs):
  outputs = prediction.forward(XTrainTensors) #forward pass
  optimizer.zero_grad() #caluclate the gradient, manually setting to 0

  # obtain the loss function
  loss = criterion(outputs, yTrainTensors)

  loss.backward() #calculates the loss of the loss function
  loss_plt.append(loss.item())
  optimizer.step() #improve from loss, i.e backprop
  if epoch % 1000 == 0:
    print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))

plt.plot(loss_plt)

df_X_ss = standard.transform(X) #old transformers
df_y_mm = min.transform(y) #old transformers

df_X_ss = Variable(torch.Tensor(df_X_ss)) #converting to Tensors
df_y_mm = Variable(torch.Tensor(df_y_mm))
#reshaping the dataset
df_X_ss = torch.reshape(df_X_ss, (df_X_ss.shape[0], 1, df_X_ss.shape[1]))


train_predict = prediction(df_X_ss)#forward pass
data_predict = train_predict.data.numpy() #numpy conversion
dataY_plot = df_y_mm.data.numpy()

data_predict = min.inverse_transform(data_predict) #reverse transformation
dataY_plot = min.inverse_transform(dataY_plot)
plt.figure(figsize=(10,6)) #plotting
 #size of the training set

plt.plot(dataY_plot, label='Real Change', color='red') #actual plot
plt.plot(data_predict, label='Predicted Change', color='green') #predicted plot
plt.title('Prediction')
plt.legend()


df2 = pd.DataFrame(data_predict, columns = ['prediction'])
df3 = pd.DataFrame(dataY_plot, columns = ['real change'])
dfCols = pd.concat([df2, y], axis = 1)
def calc_new_col(dfCols):
   if ((dfCols['prediction'] <= 0) & (dfCols['change'] <= 0)) | ((dfCols['prediction'] >= 0) & (dfCols['change'] >= 0)) :
        return 1
   else:
        return 0

dfCols["rightwrong"] = dfCols.apply(calc_new_col, axis=1)

testing = dfCols.loc[550:]
right = testing.loc[dfCols['rightwrong'] == 1]
print("testing accuracy:", (len(right)/len(testing)) * 100)









#get Cryptoprices from Openblender


action = 'API_getObservationsFromDataset'

# ANCHOR: 'BTC to USD'


parameters = {
    	'token':'623b09189516290d209a3c816Pri1VXVFj0nkKyb0QioflJ0kGFU5y',
	'id_user':'623b09189516290d209a3c81',
	'id_dataset':'5d4c3b789516290b02fe3e24',
	'date_filter':{"start_date":"2022-04-22","end_date":"2022-04-23"}
}


df5 = pd.read_json(StringIO(json.dumps(OpenBlender.call(action, parameters)['sample'])), convert_dates=False, convert_axes=False).sort_values('timestamp', ascending=False)
df5.reset_index(drop=True, inplace=True)
df5['date'] = [OpenBlender.unixToDate(ts, timezone = 'GMT') for ts in df5.timestamp]

#blend with nasdaq change
blend_source = {
    "id_dataset": "5d4c9b629516290b01c94904",
    "feature": "change",
}

df5['change'] = 100 * (np.log(df5['close']) - np.log(df5['open']))

df_blend = OpenBlender.timeBlend( token = '623b09189516290d209a3c816Pri1VXVFj0nkKyb0QioflJ0kGFU5y',
                                  anchor_ts = df5.timestamp,
                                  blend_source = blend_source,
                                  blend_type = 'closest_observation',
                                  interval_size = 60 * 60 * 24,
                                  direction = 'time_prior',
                                  interval_output = 'list',
                                  missing_values = 'raw')
df5 = pd.concat([df5, df_blend.loc[:, df_blend.columns != 'timestamp']], axis = 1)

#rename columns
df5 = df5.rename(columns = {"BITCOIN_NE.text_COUNT_last1days": "no. articles", "BITCOIN_NE.text_last1days":"list of articles", "NQ100_PRICE.change_pre": "nasdaq change"})

#remove duplicates
df5 = df5.drop_duplicates(subset=['date'], keep='first')

web_scrapingInstance = Auto_CoinTelegraph()
web_scrapingInstance2 = Auto_CryptoNews()

df5['positive'] = web_scrapingInstance[0] + web_scrapingInstance2[0]
df5['negative'] = web_scrapingInstance[1] + web_scrapingInstance2[1]

dataToModel = df5[[ "open", "close", "volume", "market_cap", "positive", "negative","nasdaq change", "change"]]
dataToModel.head()

df_X_s = standard.transform(dataToModel) #old transformers

df_X_s = Variable(torch.Tensor(df_X_s)) #converting to Tensors
#reshaping the dataset
df_X_s = torch.reshape(df_X_s, (df_X_s.shape[0], 1, df_X_s.shape[1]))

train_predict = prediction(df_X_s)#forward pass
data_predict = train_predict.data.numpy() #numpy conversion

data_predict = min.inverse_transform(data_predict) #reverse transformation


#print(type(data_predict))
print('Prediction: ',data_predict)

plt.show()
