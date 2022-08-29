import pandas as pd
import numpy as np
import requests
import os
import Augmentor
from bs4 import BeautifulSoup
import urllib.request

##女優網頁
html = requests.get('https://www.okonomi-search.com/')
html.encoding = 'UTF-8'
soup = BeautifulSoup(html.text, 'html.parser')
style_class = soup.find_all('li',class_='top-keyword')
url = 'https://www.okonomi-search.com/tag/'
for c in range(len(style_class)):
  url_class = url + style_class[c].text
  html = requests.get(url_class)
  html.encoding = 'UTF-8'
  soup = BeautifulSoup(html.text, 'html.parser')
  jpg_len = range(len(soup.find_all(class_='faces')))
  database = 'F:\porn\database'
  for x in jpg_len:
    ##女優名稱
    name = soup.find_all('li',class_='img_box')[x].find('h4')
    porn_star = name.text
    porn_star = porn_star.strip()
    ##建立女優資料夾
    porn_star_list = os.listdir(r'F:\porn\database')
    try:##尋找女優資料夾，找不到顯示-1
      ndx = porn_star_list.index(porn_star)
    except:
      ndx = -1
    if ndx == -1:##如果找不到資料夾，則新增資料夾
      os.mkdir(porn_star)
    else:
      continue

    ##建立女優圖片
    jpg = soup.find_all(class_='faces')[x].find_all(class_='faceImg lozad')
    if jpg == []:##如果女優沒有圖片，刪除資料夾並執行下個迴圈
      os.rmdir(porn_star)
      continue
    else:
      jpg_count = 0
      for j in jpg:
        porn_star_img_url = j.get('data-src')
        porn_star_img_name = database + '\\' + porn_star + '\\' +porn_star + '_' +str(jpg_count) +'.jpg'
        urllib.request.urlretrieve(porn_star_img_url, porn_star_img_name)
        jpg_count+=1
      
      ##將圖片做各種變換，增加圖片數量
      porn_star_database = database + '\\' + porn_star
      new_jpg = Augmentor.Pipeline(porn_star_database,porn_star_database)
      for b in range(1,10):
        if b == 1:
          new_jpg.rotate90(probability=1)
          new_jpg.process()

        if b == 2:
          new_jpg.flip_left_right(probability=1)
          new_jpg.process()

        if b == 3:
          new_jpg.rotate90(probability=1)
          new_jpg.process()

        if b == 4:
          new_jpg.rotate90(probability=1)
          new_jpg.process()

        if b == 5:
          new_jpg.rotate90(probability=1)
          new_jpg.process()

        if b == 6:
          new_jpg.skew(probability=1,magnitude=0.2)
          new_jpg.process()

        if b == 7:
          new_jpg.rotate90(probability=1)
          new_jpg.process()

        if b == 8:
          new_jpg.flip_left_right(probability=1)
          new_jpg.process()

        if b == 9:
          new_jpg.rotate90(probability=1)
          new_jpg.process()

        if b == 10:
          new_jpg.rotate90(probability=1)
          new_jpg.process()

  