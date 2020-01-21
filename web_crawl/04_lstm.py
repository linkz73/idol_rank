import pandas as pd
from pandas import DataFrame
import pandas.io.sql as pdsql
from pandasql import sqldf
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates

from keras.models import Sequential, Model
from keras.layers import LSTM, Dropout, Dense, Activation, Input
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import configparser
import warnings
import sys
warnings.filterwarnings("ignore")

import pymysql
import datetime

con = pymysql.connect(host = "localhost", user = "root", password ="1234",
                      db = "django_app")
cur = con.cursor()

#predict 테이블 생성
create_predict_sql = """CREATE TABLE django_app.predict (predict_id INT AUTO_INCREMENT PRIMARY KEY, predict_total FLOAT, predict_date INT, idol_id INT) WHERE IF NOT EXISTS django_app.predict"""
cur.execute(create_predict_sql)
con.commit()

make_df_sql = """SELECT idol.idol_name, chart.*
FROM chart INNER JOIN idol
ON chart.idol_id = idol.idol_id"""
cur.execute(make_df_sql)
results = cur.fetchall()
datas = pd.DataFrame(results, columns=['idol_name', 'chart_id', 'chart_music', 'chart_media', 'chart_portal','chart_total', 'chart_date', 'idol_id'])
datas['chart_date'] = datas['chart_date'].apply(lambda x:datetime.datetime.strptime(str(x), "%Y%m"))
#TEST
# print(datas)
# name_df = datas[datas['idol_name'] == '조수미']
# name_df = name_df.set_index('chart_date')

# query_tmp = f"SELECT idol_name, chart_date, chart_music, chart_media, chart_portal, chart_total FROM datas WHERE idol_name =(?)"

# val = [datas['idol_name'].values[i]for i in range(len(datas))]
val = datas[datas['chart_date'] == '2019-11-01']
val = val.nlargest(10, 'chart_total', keep='first')
val = [val['idol_name'].values[i]for i in range(len(val))]
# print(val)

remove_val = list(set(val))
list = []
# name_dic = {}
for name in remove_val:
    index_dr = pd.date_range('20180101', periods=23, freq='MS')
    df = pd.DataFrame(index=index_dr, columns=['set'])
    # name_df = {'name' : datas[datas['idol_name'] == name]}
    name_df = datas[datas['idol_name'] == name]
    name_df = name_df.set_index('chart_date')
    # name_dic[name] = name_df
    # print(type(name_dic.values()))

    # name_df['chart_date'] = name_df['chart_date'].apply(lambda x:x[:10])
    # last_day = df_tmp.values[0][0][0:10]
    # pivot_df = df.pivot(df, index=['chart_date'], columns=['idol_name', 'chart_music', 'chart_media', 'chart_portal','chart_total'],
    #                     values =['idol_name', 'chart_music', 'chart_media', 'chart_portal','chart_total'])
    # name_df = name_df.set_index("chart_date")
    # print(name_df)


    # print(datas['chart_date'])
    # 시작일자 = '201801' #'SELECT MIN(칼럼) FROM 테이블"
    # 종료일자 = '201911' #"SELECT MAX(컬럼) FROM 테이블"
    # for name_df in name_dic.values():
    #     index_dr = pd.date_range('20180101', periods=23, freq='MS')
    #     df = pd.DataFrame(index = index_dr, columns= ['set'])
    # print(name_df)
    result_df = df.join(name_df, how='left', lsuffix='_left')
    result_df.drop(['set', 'chart_id', 'idol_name'], axis=1, inplace=True)
    idol_id = name_df['idol_id'][0].tolist()

    fill_data = {"chart_music": name_df['chart_music'].mean(),"chart_media" : name_df['chart_media'].mean(),
                 "chart_portal": name_df['chart_portal'].mean(), "chart_total": name_df['chart_total'].mean(), "idol_id" : idol_id}
    result_df = result_df.fillna(fill_data).round(2)


    # result_df = pd.concat([df,name_df], axis=1, join='inner', join_axes=False)
    # result_df = pd.merge(df, name_df)
    # print(result_df)
    # df = pd.DataFrame()
    # # query_tmp = f"SELECT date,music,social,naver,total FROM df WHERE date > '{시작일자}' AND date < '{종료일자}' AND name='방탄소년단'"



    from keras.utils import np_utils

    # 1. 데이터 전처리
    X1 = result_df['chart_music'].values
    X2 = result_df['chart_media'].values
    X3 = result_df['chart_portal'].values
    y = result_df['chart_total'].values
    print(y.shape)  # (60000,)

    size = 3
    def split_x(seq, size):
        aaa = []
        for i in range(len(seq) - size + 1):
            subset = seq[i:(i+size)]
            aaa.append([item for item in subset])
        return np.array(aaa)


    X1 = split_x(X1, size)
    X1 = X1[:-1,:]
    X2 = split_x(X2, size)
    X2 = X2[:-1,:]
    X3 = split_x(X3, size)
    X3 = X3[:-1,:]
    # y 값은 x를 lstm 모델에 맞도록 앞에서 사이즈만큼 잘라주어야 함.
    y = y[size:,]

    from sklearn.preprocessing import MinMaxScaler, StandardScaler
    scaler = MinMaxScaler()
    # scaler = StandardScaler()
    # scaler.fit(x)  # fit 을 하면서 가중치가 생성됨.
    # x = scaler.transform(x)
    X1 = scaler.fit_transform(X1)
    X2 = scaler.fit_transform(X2)
    X3 = scaler.fit_transform(X3)

    X1 = np.reshape(X1, (X1.shape[0], X1.shape[1], 1))
    X2 = np.reshape(X2, (X2.shape[0], X2.shape[1], 1))
    X3 = np.reshape(X3, (X3.shape[0], X3.shape[1], 1))
    # y = np.reshape(y, (y.shape[0], y.shape[1], 1))

    # print(X2)
    # print(X3)
    # print(y)
    # print(y.shape)

    from sklearn.model_selection import train_test_split
    X1_train, X1_test, X2_train, X2_test = train_test_split(X1, X2, random_state=3, test_size=0.4)
    X1_val, X1_test, X2_val, X2_test = train_test_split(X1_test, X2_test, random_state=3, test_size=0.5)
    X3_train, X3_test = train_test_split(X3, random_state=3, test_size=0.4)
    X3_val, X3_test = train_test_split(X3_test, random_state=3, test_size=0.5)
    y_train, y_test = train_test_split(y, random_state=3, test_size=0.4)
    y_val, y_test = train_test_split(y_test, random_state=3, test_size=0.5)

    # print("X1_train shape", X1_train.shape)  # (*,3,1)
    # print("X2_train shape", X2_train.shape)  # (*,3,1)
    # print("X3_train shape", X2_train.shape)  # (*,3,1)
    # print("X1_test shape", X1_test.shape)  # (*,3,1)
    # print("X2_test shape", X2_test.shape)  # (*,3,1)
    # print("X3_test shape", X3_test.shape)  # (*,3,1)
    # print("X1_val shape", X1_val.shape)  # (*,3,1)
    # print("X2_val shape", X2_val.shape)  # (*,3,1)
    # print("X3_val shape", X3_val.shape)  # (*,3,1)
    # print("y_train shape", y_train.shape)  # (4,)
    # print("y_test shape", y_test.shape)  # (2,)
    # print("y_val shape", y_val.shape)  # (1,)

    input1 = Input(shape=(3,1))
    layers = LSTM(100, return_sequences=True, activation='relu')(input1)
    layers = LSTM(64, activation='relu')(layers)
    middle1 = Dropout(0.5)(layers)

    input2 = Input(shape=(3,1))
    layers2 = LSTM(100, return_sequences=True, activation='relu')(input2)
    layers2 = LSTM(64, activation='relu')(layers2)
    middle2 = Dropout(0.5)(layers2)

    input3 = Input(shape=(3,1))
    layers3 = LSTM(100, return_sequences=True, activation='relu')(input3)
    layers3 = LSTM(64, activation='relu')(layers3)
    middle3 = Dropout(0.5)(layers3)

    from keras.layers.merge import concatenate
    merge1 = concatenate([middle1, middle2, middle3])  # output 만 묶어 주면 됨.
    output = Dense(30, activation='relu')(merge1)
    output = Dense(10, activation='relu')(merge1)
    output1 = Dense(1, activation='relu')(output)

    model = Model(inputs = [input1, input2, input3], outputs = output1)
    # model.summary()

    from keras.callbacks import EarlyStopping

    model.compile(loss='mse', optimizer='adam', metrics=['mse'])
    # model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    early_stopping_callback = EarlyStopping(monitor='val_acc', patience=10)

    start_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    model.fit([X1_train,X2_train,X3_train], y_train,
        validation_data=([X1_val,X2_val,X3_val], y_val),
        batch_size=1,
        verbose=2,
        epochs=1000,
        callbacks=[
            # TensorBoard(log_dir='logs/%s' % (start_time)),
            early_stopping_callback,
            # ModelCheckpoint('./lstm_test/models/%s_eth.h5' % (start_time), monitor='val_acc', verbose=1, save_best_only=True, mode='auto'),
            # ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, verbose=1, mode='auto')
    ])


    # 예측 결과를 그래프로 표현
    X1_chart, X2_chart, X3_chart = X1[:][-1:], X2[:][-1:], X3[:][-1:]
    pred = model.predict([X1_chart,X2_chart,X3_chart])
    # print("\n Test Accuracy: %.4f" % (model.evaluate([X1_test,X2_test,X3_test], y_test)[0]))
    pred = pred.flatten().tolist()
    pred = round(pred[0], 2)
    # print(pred)
    # print(type(pred))
    result = pred, 201912, idol_id
    list.append(result)
    del [df, result_df]
# fig = plt.figure(facecolor='white', figsize=(20, 10))
# ax = fig.add_subplot(111)
# ax.plot(y_test, label='True')
# ax.plot(pred, label='Prediction')
# ax.legend()
# plt.show()




insert_predict_sql = """INSERT INTO django_app.predict(predict_total, predict_date, idol_id)
VALUES (%s, %s, %s)"""

value = list
cur.executemany(insert_predict_sql, value)
con.commit()

foreign_key = """ALTER TABLE predict ADD FOREIGN KEY (idol_id) REFERENCES idol (idol_id);"""
cur.execute(foreign_key)
con.commit()

con.close()
