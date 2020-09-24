# coding: UTF-8
print('hello world!')
import requests
import MySQLdb
import sys
import datetime
from bs4 import BeautifulSoup

###################
# 定数定義部
###################
class PictureID:
  ID = 'id'
  CATEGORY_ID1 = 'category_id1'
  CATEGORY_ID2 = 'category_id2'
  SITE_NAME = 'site_name'
  TITLE = 'title'
  CONTENT_URL = 'content_url'
  PIC_URL = 'pic_url'
  DURATION = 'duration'
  POST_TIME = 'post_time'

###################
# 関数定義部
###################
#pictureテーブルへのデータ登録
def insertPicture(picture, file):
  #接続
  conn = MySQLdb.connect(
    user='zufyzqwv_admin',
    password='cXj8WYi4gPSa66t',
    host='localhost',
    db='zufyzqwv_mydb',
    use_unicode=True,
    charset="utf8"
  )
  
  cursor = conn.cursor()
  
  target = "`"+PictureID.ID+"`, `"+PictureID.CATEGORY_ID1+"`, `"+PictureID.CATEGORY_ID2\
  +"`, `"+PictureID.SITE_NAME+"`, `"+PictureID.TITLE+"`, `"+PictureID.CONTENT_URL\
  +"`, `"+PictureID.PIC_URL+"`, `"+PictureID.DURATION+"`, `"+PictureID.POST_TIME+"`"
  
  sql = "INSERT IGNORE INTO `picture` ("+target+") VALUES (NULL, 0, 0, '"+picture[PictureID.SITE_NAME]+"', '"+picture[PictureID.TITLE]+"', '"+picture[PictureID.CONTENT_URL]+"', '"+picture[PictureID.PIC_URL]+"', '"+picture[PictureID.DURATION]+"', CURRENT_TIMESTAMP);"
  file.write(sql)
  cursor.execute(sql)
  #rows = cursor.fetchall()
  #for row in rows:
  #  print(row)
  #print(rows[0][3])

  conn.commit()
  #切断
  conn.close

##############################
# メイン部
##############################  
url = 'https://www.nukistream.com/category.php?id=1'
res = requests.get(url)
#print(res.text)

soup = BeautifulSoup(res.text.encode('utf-8'), "html.parser")

#print(soup)

picture_array = []

articles = soup.find_all('article')
#print(articles)

dt_now = datetime.datetime.now()
file = "抜きスト_"+dt_now.strftime('%Y%m%d%H%M')+".sql"
print(file)
fileobj = open(file, "w", encoding = "utf_8")

# 連想配列に取得したデータを詰める
for article in articles:
  picture = {PictureID.SITE_NAME: 'ぬきすと',
             PictureID.TITLE: article.find('img')['alt'],
             PictureID.CONTENT_URL: 'https://www.nukistream.com' + article.find('h3').find('a')['href'],
             PictureID.PIC_URL: 'https:' + article.find('img')['src'],
             PictureID.DURATION: article.find('span').text}
  insertPicture(picture, fileobj)

print('ぬきスト', str(len(articles))+"件見つかりました")
fileobj.close()