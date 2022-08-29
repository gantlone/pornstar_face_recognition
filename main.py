import os, cv2, glob, magic
import tensorflow as tf
import numpy as np
from function import dict_label, read_and_label_porn_picture, normalize_one_hot, porn_label_predict
from sklearn.model_selection import train_test_split
from keras.applications.vgg19 import VGG19
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.optimizers import RMSprop


porn_data_database = 'F:\\porn\\database\\'

##設定女優數字標籤
porn_star_number_label = dict_label(porn_data_database)

##讀取女優圖片，以及標記女優標籤
porn_star_images, porn_star_labels, porn_star_names = read_and_label_porn_picture(porn_data_database,porn_star_number_label)

##女優圖片資料預處理，train:80%、test:20%
##name部分為女優名稱，預測時方便看是誰
random_state = 17
train_feature, test_feature, train_label, test_label, train_names, test_names = \
train_test_split(porn_star_images, porn_star_labels, porn_star_names, random_state=random_state, test_size=0.2)
train_feature = np.array(train_feature)
test_feature = np.array(test_feature)
train_label = np.array(train_label)
test_label = np.array(test_label)
train_names = np.array(train_names)
test_names = np.array(test_names)

##將特徵標準化和One-Hot編碼標籤
train_feature_n, test_feature_n, train_label_one, test_label_one = \
normalize_one_hot(train_feature, test_feature, train_label, test_label)

##建立模型
model_path = os.listdir('F:\\porn\\') 
model_select = [s for s in model_path if "porn_model_20_7.h5" in s] 

if model_select==[]: #如果沒有檔案夾中.h5，執行這行
    #利用訓練女優圖片，建立模型，並保存成.h5格式
    #將遷移學習中所有VGG19中權重與全聯階層相連
    porn_model = VGG19(include_top=False, weights='imagenet', input_shape=(224,224,3), pooling='max')
    porn_model.trainable = False
    model = Sequential()
    model.add(porn_model)
    model.add(Dense(20, activation='softmax'))
    opt = RMSprop(lr=0.001, rho=0.9, epsilon=1e-08, decay=0.0)
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    history = model.fit(train_feature_n, train_label_one, validation_split=0.1, batch_size=16, epochs=70, verbose=2)
    model.save('porn_model_20_7.h5')

else: #如果有檔案夾中.h5，執行這行
    #如果已經建好模型，將測試女優圖片準確度
    #print出測試loss和測試準確度
    #plt輸出20張測試女優圖片預測分析
    model = load_model('porn_model_20_7.h5')
    test_porn_predict = model.predict(test_feature_n)
    test_porn_predict = np.argmax(test_porn_predict, axis=1)
    print(model.evaluate(test_feature_n, test_label_one))
    porn_label_predict(test_feature, test_label, test_names, test_porn_predict, 0, 20)




