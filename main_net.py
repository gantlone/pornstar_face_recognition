from tensorflow.keras.models import load_model
from random import *
import gradio as gr 
import os

##將學習好的model.h5讀取
model = load_model('porn_model_20_7.h5')
porn_data_database = 'F:\\porn\\database\\'

##設定女優標籤
porn_star_number_label = os.listdir(porn_data_database)
n = len(porn_star_number_label)
bek = []
for i in range(n):
    if '.py' in porn_star_number_label[i]:
        bek.append(i)

porn_star_number_label = [porn_star_number_label[i] for i in range(n) if (i not in bek)]

##定義模型與預測
def porn_detect(img):
    img = img.reshape(1, 224, 224, 3)
    prediction = model.predict(img).tolist()[0]
    class_names = porn_star_number_label
    return {class_names[i]: prediction[i] for i in range(20)}

input = gr.inputs.Image(shape=(224, 224), source='upload')
output = gr.outputs.Label(num_top_classes=3, label='預測結果')

##在網頁上顯示字串
porn_list = str()
for k in range(len(porn_star_number_label)):
    count = str(k+1) + '. ' + porn_star_number_label[k]
    porn_list = porn_list + count + ' '
article = '目前支援的女優類別為: ' + porn_list

##舉例的圖片，與database所用的女優圖片不同
os.chdir('F:\porn\database_test')
test_list = os.listdir('F:\porn\database_test')
shuffle(test_list)

##網頁上gradio函數應用，input_image、output_predict
grobj = gr.Interface(fn=porn_detect,
                    inputs=input,
                    outputs=output, 
                    article=article,
                    examples=[test_list[0], test_list[1]],
                    title='日本女優人臉辨識')

##跑程式
if __name__ == "__main__":
    print('connect')
    grobj.launch(inbrowser=True, inline=False, share=True)