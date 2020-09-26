# coding: UTF-8
print('スクレイピング結果')
import codecs
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
  CATEGORY_ID3 = 'category_id3'
  SITE_NAME    = 'site_name'
  TITLE        = 'title'
  CONTENT_URL  = 'content_url'
  PIC_URL      = 'pic_url'
  DURATION     = 'duration'
  POST_TIME    = 'post_time'

class CategoryID:
  ID = {'巨乳': 1, '人妻': 2, '痴女': 3, 'ギャル': 4, '素人': 5, '熟女': 6, '美乳': 7}

class SiteName:
  TEST            = 'テスト'
  NUKISUTO        = 'ぬきスト'
  ERO_MOVIE_CAFE  = 'エロ動画カフェ'
  IQOO            = 'iQoo'
  POYOPARA        = 'ぽよパラ'
  ERONUKI         = 'エロヌキ'
  JAVMIXTV          = 'Javmix.TV'

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
  +"`, "+PictureID.CATEGORY_ID3+", `"+PictureID.SITE_NAME+"`, `"+PictureID.TITLE+"`, `"+PictureID.CONTENT_URL\
  +"`, `"+PictureID.PIC_URL+"`, `"+PictureID.DURATION+"`, `"+PictureID.POST_TIME+"`"
  
  sql = "INSERT IGNORE INTO `picture` ("+target+") VALUES (NULL, "+picture[PictureID.CATEGORY_ID1]+", "+picture[PictureID.CATEGORY_ID2]+", "+picture[PictureID.CATEGORY_ID3]+", '"+picture[PictureID.SITE_NAME]+"', '"+picture[PictureID.TITLE]+"', '"+picture[PictureID.CONTENT_URL]+"', '"+picture[PictureID.PIC_URL]+"', '"+picture[PictureID.DURATION]+"', CURRENT_TIMESTAMP);"
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

#カテゴリ取得
def getCategory(categories):
    category1 = 0
    category2 = 0
    category3 = 0
#    print(categories)
    if len(categories) >= 3:
      category1 = searchCategory(categories[0].find('a').text)
      category2 = searchCategory(categories[1].find('a').text)
      category3 = searchCategory(categories[2].find('a').text)
    elif len(categories) == 2:
      category1 = searchCategory(categories[0].find('a').text)
      category2 = searchCategory(categories[1].find('a').text)
    elif len(categories) == 1:
      category1 = searchCategory(categories[0].find('a').text)
    
    category = [category1, category2, category3]
    return category


#スクレイピング - ぬきスト
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingNukisuto(soup, fileobj, site_title):
  articles = soup.find_all('article')
  
  # 連想配列に取得したデータを詰める
  for article in articles:
    categories = article.find_all('li')

    category = getCategory(categories)

    picture = {PictureID.CATEGORY_ID1: str(category[0]),
               PictureID.CATEGORY_ID2: str(category[1]),
               PictureID.CATEGORY_ID3: str(category[2]),
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

    category = getCategory(categories)

    picture = {PictureID.CATEGORY_ID1: str(category[0]),
               PictureID.CATEGORY_ID2: str(category[1]),
               PictureID.CATEGORY_ID3: str(category[2]),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('a', class_='js-atd__link').text,
               PictureID.CONTENT_URL: article.find('a', class_='js-atd__link')['href'],
               PictureID.PIC_URL: article.find('img', class_='js-atd__img')['src'],
               PictureID.DURATION: '-'}
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")


#スクレイピング
#スクレイピング - iQoo
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingIqoo(soup, fileobj, site_title):
  articles = soup.find_all('article')

  # 連想配列に取得したデータを詰める
  for article in articles:
    categories = article.find_all('li')

    category = getCategory(categories)

    picture = {PictureID.CATEGORY_ID1: str(category[0]),
               PictureID.CATEGORY_ID2: str(category[1]),
               PictureID.CATEGORY_ID3: str(category[2]),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('img')['alt'],
               PictureID.CONTENT_URL: 'https://iqoo.me' + article.find('a')['href'],
               PictureID.PIC_URL: article.find('img')['src'],
               PictureID.DURATION: article.find('span', class_='duration').text}
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")


#スクレイピング
#スクレイピング - ぽよパラ
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingPoyopara(soup, fileobj, site_title):
  articles = soup.find_all('article')

  # 連想配列に取得したデータを詰める
  for article in articles:
    categories = article.find_all('li')

    category = getCategory(categories)

    picture = {PictureID.CATEGORY_ID1: str(category[0]),
               PictureID.CATEGORY_ID2: str(category[1]),
               PictureID.CATEGORY_ID3: str(category[2]),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('img')['alt'],
               PictureID.CONTENT_URL: 'https://iqoo.me' + article.find('a')['href'],
               PictureID.PIC_URL: article.find('img')['src'],
               PictureID.DURATION: article.find('span', class_='duration').text}
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")


#スクレイピング
#スクレイピング - エロヌキ
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingEronuki(soup, fileobj, site_title):
  articles = soup.find_all('article')

  # 連想配列に取得したデータを詰める
  for article in articles:
    categories = article.find_all('li')

    category = getCategory(categories)

    picture = {PictureID.CATEGORY_ID1: str(category[0]),
               PictureID.CATEGORY_ID2: str(category[1]),
               PictureID.CATEGORY_ID3: str(category[2]),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('h2', class_='movie_main_title').text,
               PictureID.CONTENT_URL: article.find('a')['href'],
               PictureID.PIC_URL: article.find('img')['data-original'],
               PictureID.DURATION: article.find('div', class_='movie-dur').text}
#    print(picture)
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")


#スクレイピング
#スクレイピング - Javmix.TV
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingJavmixtv(soup, fileobj, site_title):
  articles = soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-6')

  # 連想配列に取得したデータを詰める
  for article in articles:
    picture = {PictureID.CATEGORY_ID1: str(0),
               PictureID.CATEGORY_ID2: str(0),
               PictureID.CATEGORY_ID3: str(0),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('img')['alt'],
               PictureID.CONTENT_URL: article.find('a')['href'],
               PictureID.PIC_URL: article.find('img')['src'],
               PictureID.DURATION: article.find('span', class_='rating-bar bgcolor2 time_dur').text}
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")


#スクレイピング
#スクレイピング - テスト
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingTest(soup, fileobj, site_title):
  articles = soup.find_all('div', class_='col-md-3 col-sm-6 col-xs-6')
  print(articles[0])
  # 連想配列に取得したデータを詰める
  for article in articles:
#    categories = article.find_all('li')
#
#    category = getCategory(categories)

    picture = {PictureID.CATEGORY_ID1: str(0),
               PictureID.CATEGORY_ID2: str(0),
               PictureID.CATEGORY_ID3: str(0),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('img')['alt'],
               PictureID.CONTENT_URL: article.find('a')['href'],
               PictureID.PIC_URL: article.find('img')['src'],
               PictureID.DURATION: article.find('span', class_='rating-bar bgcolor2 time_dur').text}
    print(picture)
#    insertPicture(picture, fileobj)
#
#  print(site_title, str(len(articles))+"件見つかりました")


def scraping(fileobj, site_title, url):
  res = requests.get(url)
  #print(res.text)

  soup = BeautifulSoup(res.text.encode('utf-8'), "html.parser")

  #print(soup)

  picture_array = []

  #print(searchCategory(articles[0].find('ul').find('a').text))
  
  if site_title == SiteName.NUKISUTO:
    scrapingNukisuto(soup, fileobj, site_title)
  elif site_title == SiteName.TEST:
    scrapingTest(soup, fileobj, site_title)
  elif site_title == SiteName.ERO_MOVIE_CAFE:
    scrapingEroMovieCafe(soup, fileobj, site_title)
  elif site_title == SiteName.IQOO:
    scrapingIqoo(soup, fileobj, site_title)
  elif site_title == SiteName.POYOPARA:
    scrapingPoyopara(soup, fileobj, site_title)
  elif site_title == SiteName.ERONUKI:
    scrapingEronuki(soup, fileobj, site_title)
  elif site_title == SiteName.JAVMIXTV:
    scrapingJavmixtv(soup, fileobj, site_title)

##############################
# メイン部
##############################  
dt_now = datetime.datetime.now()
file = dt_now.strftime('%Y%m%d_%H%M')+".sql"
fileobj = open(file, "w", encoding = "utf-8")

#scraping(fileobj, SiteName.TEST, 'https://javmix.tv/video/')
scraping(fileobj, SiteName.NUKISUTO, 'https://www.nukistream.com/')
scraping(fileobj, SiteName.ERO_MOVIE_CAFE, 'http://xvideos-field5.com/')
scraping(fileobj, SiteName.IQOO, 'https://iqoo.me/')
scraping(fileobj, SiteName.POYOPARA, 'https://poyopara.com/')
scraping(fileobj, SiteName.ERONUKI, 'https://ero-nuki.net/')
scraping(fileobj, SiteName.JAVMIXTV, 'https://javmix.tv/video/')

fileobj.close()