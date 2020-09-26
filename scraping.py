# coding: UTF-8
print('スクレイピング結果')
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

class CategoryID:
  ID = {'巨乳': 1, '人妻': 2, '痴女': 3, 'ギャル': 4}

class SiteName:
  NUKISUTO = 'ぬきスト'
  ERO_MOVIE_CAFE = 'エロ動画カフェ'

###################
# 関数定義部
###################

#pictureテーブルへのデータ登録
# @param: picture 画像用連想配列の配列
# @param: file file操作オブジェクト
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
  
  sql = "INSERT IGNORE INTO `picture` ("+target+") VALUES (NULL, "+picture[PictureID.CATEGORY_ID1]+", "+picture[PictureID.CATEGORY_ID2]+", '"+picture[PictureID.SITE_NAME]+"', '"+picture[PictureID.TITLE]+"', '"+picture[PictureID.CONTENT_URL]+"', '"+picture[PictureID.PIC_URL]+"', '"+picture[PictureID.DURATION]+"', CURRENT_TIMESTAMP);"
#  print(sql)
  file.write(sql)
  cursor.execute(sql)
  #rows = cursor.fetchall()
  #for row in rows:
  #  print(row)
  #print(rows[0][3])

  conn.commit()
  #切断
  conn.close

#カテゴリ検索
def searchCategory(category):
  check = category in CategoryID.ID.keys()
  if check:
    return CategoryID.ID[category]
  else:
    return 0

#スクレイピング - ぬきスト
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingNukisuto(soup, fileobj, site_title):
  articles = soup.find_all('article')
  
  # 連想配列に取得したデータを詰める
  for article in articles:
    categories = article.find_all('ul')
    
    category1 = 0
    category2 = 0
    
    if len(categories) >= 2:
      category1 = searchCategory(categories[0].find('a').text)
      category2 = searchCategory(categories[1].find('a').text)
    elif len(categories) == 1:
      category1 = int(searchCategory(categories[0].find('a').text))
      
    picture = {PictureID.CATEGORY_ID1: str(category1),
               PictureID.CATEGORY_ID2: str(category2),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('img')['alt'],
               PictureID.CONTENT_URL: 'https://www.nukistream.com' + article.find('h3').find('a')['href'],
               PictureID.PIC_URL: 'https:' + article.find('img')['src'],
               PictureID.DURATION: article.find('span').text}
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")


#スクレイピング
#スクレイピング - エロ動画カフェ
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingEroMovieCafe(soup, fileobj, site_title):
  articles = soup.find('div', class_='p-recent__inner flex-horizontal').find_all('div', class_='c-card js-atd__article')
#  print(article[0])

  # 連想配列に取得したデータを詰める
  for article in articles:
    categories = article.find_all('li')
    
    category1 = 0
    category2 = 0
    #print(categories[0].find('a').text)
    if len(categories) >= 1:
      category1 = CategoryID.ID['巨乳']
      category2 = searchCategory(categories[0].find('a').text)
      
    picture = {PictureID.CATEGORY_ID1: str(category1),
               PictureID.CATEGORY_ID2: str(category2),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('a', class_='js-atd__link').text,
               PictureID.CONTENT_URL: article.find('a', class_='js-atd__link')['href'],
               PictureID.PIC_URL: article.find('img', class_='js-atd__img')['src'],
               PictureID.DURATION: '-'}
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")


def scraping(fileobj, site_title, url):
  res = requests.get(url)
  #print(res.text)

  soup = BeautifulSoup(res.text.encode('utf-8'), "html.parser")

  #print(soup)

  picture_array = []

  #print(searchCategory(articles[0].find('ul').find('a').text))
  
  if site_title == SiteName.NUKISUTO:
    scrapingNukisuto(soup, fileobj, site_title)
  elif site_title == SiteName.ERO_MOVIE_CAFE:
    scrapingEroMovieCafe(soup, fileobj, site_title)

##############################
# メイン部
##############################  
dt_now = datetime.datetime.now()
file = dt_now.strftime('%Y%m%d_%H%M')+".sql"
fileobj = open(file, "w", encoding = "utf_8")

scraping(fileobj, SiteName.NUKISUTO, 'https://www.nukistream.com/category.php?id=1')
scraping(fileobj, SiteName.ERO_MOVIE_CAFE, 'http://xvideos-field5.com/archives/category/%e5%b7%a8%e4%b9%b3')

fileobj.close()