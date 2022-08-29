import os, cv2, glob, magic
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.utils import to_categorical
from keras.applications.vgg19 import VGG19, preprocess_input
#from keras.applications.inception_v3 import preprocess_input
from keras.models import Model
import japanize_matplotlib
from keras.preprocessing import image
plt.style.use('ggplot') # use ggplot style



##設定女優數字標籤
def dict_label(porn_database_url):
    dict_label = {}
    label_count = 0
    for x in range(len(os.listdir(porn_database_url))):
        porn_star_name = os.listdir(porn_database_url)[x]
        try:
            type_message_error = magic.from_file(porn_database_url + porn_star_name)
        except:
            type_message_error = -1

        if type_message_error == -1:
            dict_label[porn_star_name] = label_count
            label_count+=1
        else:
            continue

    return dict_label

##讀取女優圖片，以及標記女優標籤
def read_and_label_porn_picture(porn_data_database,dict_label):
    porn_star_images=[]
    porn_star_labels=[]
    porn_star_names=[]
    porn_data_database = porn_data_database + '*'
    for folders in glob.glob(porn_data_database):
        try:
            type_message_error = magic.from_file(folders)
        except:
            type_message_error = -1

        if  type_message_error == -1:   
            label = folders.split('\\')[-1]
            print(label,'圖片讀取中...')
            for filename in os.listdir(folders):
                try:
                    img = cv2.imdecode(np.fromfile((os.path.join(folders,filename)), dtype=np.uint8), -1)
                    img = cv2.resize(img,dsize=(224,224))
                    if img is not None:
                        porn_star_images.append(img)
                        porn_star_labels.append(dict_label[label])
                        porn_star_names.append(label.encode().decode())
                except:
                    pass
            
        else:
            continue

    print('已經讀取所有女優圖片!')
    
    return porn_star_images, porn_star_labels, porn_star_names

##將特徵標準化和One-Hot編碼標籤
def normalize_one_hot(train_feature, test_feature, train_label, test_label):
    #特徵標準化
    train_feature = preprocess_input(train_feature)
    test_feature = preprocess_input(test_feature)
    
    #One-Hot標籤
    train_label = to_categorical(train_label)
    test_label = to_categorical(test_label)

    return train_feature, test_feature, train_label, test_label

##將測試女優圖片，進行預測，比較10張測試圖片準確度
def porn_label_predict(test_feature, test_label, test_names, prediction, start_id, num=10):
    fig = plt.figure(figsize=(30, 30))
    if num>25: num=25
    for i in range(0, num):
        ax=plt.subplot(4,5, 1+i)
        ax.imshow(test_feature[start_id])
        if(len(prediction)>0):
            title = 'AI = ' + str(prediction[start_id])
            if prediction[start_id] == test_label[start_id]:
                title += ' (o)'
                title += '\nlabel = ' + str(test_label[start_id])
                title += '\npredict_name = ' + test_names[start_id]
                ax.set_title(title, fontsize=8)
            else:
                title += ' (x)'
                title += '\nlabel = ' + str(test_label[start_id])
                title += '\npredict_name = ' + test_names[start_id]
                ax.set_title(title, fontsize=8, color='red')
        else:
            title = 'label = ' + str(test_label[start_id])
            title += '\npredict_name = ' + test_names[start_id]
        ax.set_xticks([]);ax.set_yticks([])
        start_id+=1
    plt.subplots_adjust(left=0.125,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.35)
    #fig.savefig('test_' + str(num) + '_pornstars.png',dpi=fig.dpi)
    plt.show()
    #plt.savefig('test_' + str(num) + '_pornstars.png')
    #plt.savefig('test_' + str(num) + '_pornstars.jpg')
