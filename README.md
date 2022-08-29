# pornstar_face_recognition

- 作品名稱: 日本女優人臉辨識
- 目的: 幫助偶爾在某些網站看片，如pornhub、jable...等等網站，看到一些女優覺得很漂亮，但又不知道她是誰的時候，就可以使用這程式碼，將女優臉部截圖下來代入模型中判斷，得出女優名字。

## 使用電腦設備

- 處理器: AMD Ryzen 5 2600 Six-Core Processor
- 記憶體: KLEVV DDR4-3200 8G
- 顯示卡: Radeon RX 570 Series

## 主要需求

### python:
- BeautifulSoup
- tensorflow   
- keras
- gradio

## 使用流程

### 第一步
- 使用database\create_av_img.py，使用爬蟲函數(BeautifulSoup)的辦法將[AV女優お好み検索]裡的女優人臉存到database裡，也可以自行修改path。
  - 基本上爬蟲完會是每位女優子資料夾8張基本面孔，以及72張使用資料增強方法的女優圖片。
  - 一個類別資料集最多80張。

### 第二步
- 再來使用main.py，將所有女優圖片做深度學習，但由於我的電腦不太好和資料量偏少(一位女優最多只有80張圖片)的關係，所以我只使用20種類別的女優。
  - 先將資料集做分割，分為80%訓練集，20%測試集
  - 將所有圖片做特徵標準化(feature)和One-Hot編碼(label)，使用監督式學習的方式。
  - 建立模型，由於資料量小和顯示卡沒有那麼好，所以採用遷移學習的方式，使用其中的VGG19模型。
    - VGG19模型中只有最後全連接層是使用自己的Dense(20)，20個類別，其餘部分沒有修改，權重都一樣。
    - 訓練過程中，將訓練資料集再做80%訓練/20$驗證，缺點會少更多資料訓練，但優點方便觀察到底訓練得好不好。
    - 優化函數使用RMSprop，學習率和優化器選擇都是try出來的，發現這樣試是最好的。
  - 模型訓練完會產生.h5檔案，再重新執行即可使用，會產生測試集的準確度，以及20張女優辨識度。
  
### 第三步  
- 最後使用main_net.py
  - 讀取訓練好的.h5檔案(porn_model_20_7.h5)，將模型架設到網頁上面，使用python中函數設置(gradio)。
  
## 實驗結果

- 訓練準確度: 使用遷移學習彌補資料集太少的關係，訓練時可以達到99%，但是驗證時85%，還是有overfitting的跡象。

![訓練準確度]

- 測試準確度: 顯示數字為左loss、右準確度，準確度就相對更低78%。 

![測試準確度] 

- 測試圖plot: 20位女優的辨識程度: 辨識測試集中前面20位女優，有3位女優辨識失敗，效果還是有出來但還是需要改善。

![測試圖plot] 

- 將模型架設到網頁上面: 可以自行輸入女優圖片，最好是臉部和224x224的圖片，效果最好，目前只支援20位女優類別。
  - 網頁中也提供example做為使用，來源都來自google圖片，和資料集(database)內不重複。

![網頁]

## 未來展望
### 需要改善的方面有3點:
- 圖片資料不夠，未來可能搭配opencv的方式，直接對a片網頁中女優封面所有臉型做爬蟲，目的是增加資料量，因為一般來說要做深度學習每種類別需要1000張圖片以上，這是需要改善的一點。
- 特徵上的選取，或許使用解凍遷移模型的方式，將數據代入第一個pool，並提取其中輸出部分做為新的特徵，或許效果能更加優化。
- 網頁上的架設，使用gradio app，老實說算是有點偷懶的方式，未來可能會將model.h5與flask或django做結合，讓整體畫面看起來更優美與實用。

## 參考來源
- amd中架設tensorflow的辦法: [amd tensorflow]
- 幫助我從matlab轉殖到python上使用深度學習的最大功臣: [python 資料科學自學聖經]
  - BeautifulSoup爬蟲技巧、遷移學習等等..基本技巧都來自這裡。
- python中遷移學習函數和教程細節: [python 遷移學習]
  - 優化器和模型函數細節都參考這裡。
- 遷移學習中參數調整: [參數調整]
  - 這也是重要的參考資料，教我許多修改模型和特徵上的細節與技巧。
- 網頁的架設資料: [gradio教學]
  - 學習簡易網頁架設，真的很簡單使用。

<!-- links -->
[AV女優お好み検索]:https://www.okonomi-search.com/
[amd tensorflow]:https://www.youtube.com/watch?v=SDqCE2mwaA4&ab_channel=Btkb
[python 資料科學自學聖經]:https://www.books.com.tw/products/0010923134
[python 遷移學習]:https://keras.io/zh/applications/
[參數調整]:https://www.analyticsvidhya.com/blog/2017/06/transfer-learning-the-art-of-fine-tuning-a-pre-trained-model/
[gradio教學]:https://zhuanlan.zhihu.com/p/556126344

<!-- pictures -->
[訓練準確度]:/train_predict_20_7.jpg
[測試準確度]:/test_predict_20_7.jpg
[測試圖plot]:/test_20_pornstars_7.png
[網頁]:/porn_face_recognition_net.jpg

