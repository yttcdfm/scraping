# coding: UTF-8
print('スクレイピング結果')
import os
import codecs
import requests
import MySQLdb
import sys
import datetime
from bs4 import BeautifulSoup
import datetime

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

class EventID:
  ID        = 'id'
  NAME      = 'name'
  LOCATION  = 'location'
  DATE      = 'date'
  DETAIL    = 'detail'
  POST_TIME = 'post_time'

class UnitID:
  ID          = 'id'
  SITE_NAME   = 'site_name'
  TITLE       = 'title'
  CONTENT_URL = 'content_url'
  PIC_URL     = 'pic_url'
  POST_TIME   = 'post_time'

class CategoryID:
  ID = {'巨乳': 1, '人妻': 2, '痴女': 3, 'ギャル': 4, '素人': 5, '熟女': 6, '美乳': 7, 'フェラ': 8, 'パイパン': 9, 'スレンダー': 10}

class SiteName:
  TEST            = 'テスト'
  NUKISUTO        = 'ぬきスト'
  ERO_MOVIE_CAFE  = 'エロ動画カフェ'
  IQOO            = 'iQoo'
  POYOPARA        = 'ぽよパラ'
  ERONUKI         = 'エロヌキ'
  JAVMIXTV        = 'Javmix.TV'
  EROMON          = 'エロ動画もん'
  AV_EVENT        = 'いベルト！'
  FANZA           = 'FANZA 動画'

###################
# 関数定義部
###################
#DBへの接続
def connectDB():
  #接続
  conn = MySQLdb.connect(
    user='zufyzqwv_admin',
    password='cXj8WYi4gPSa66t',
    host='localhost',
    db='zufyzqwv_mydb',
    use_unicode=True,
    charset="utf8"
  )
  return conn;

#pictureテーブルへのデータ登録
# @param: picture 画像用連想配列の配列
# @param: file file操作オブジェクト
def insertPicture(picture, file):
  #接続
  conn = connectDB()  
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

#class EventID:
#  ID = 'id'
#  NAME = 'name'
#  LOCATION = 'location'
#  DATE = 'date'
#  DETAIL = 'detail'
#  POST_TIME = 'post_time'

#eventテーブルへのデータ登録
# @param: event イベント用連想配列の配列
# @param: file file操作オブジェクト
def insertEvent(event, file):
  #接続
  conn = connectDB()  
  cursor = conn.cursor()
  
  target = "`"+EventID.ID+"`, `"+EventID.NAME+"`, `"+EventID.LOCATION\
  +"`, "+EventID.DATE+", `"+EventID.DETAIL+"`, `"+EventID.POST_TIME+"`"

  sql = "INSERT IGNORE INTO `event` ("+target+") VALUES (NULL, '"+event[EventID.NAME]+"', '"+event[EventID.LOCATION]+"', '"+event[EventID.DATE]+"', '"+event[EventID.DETAIL]+"', CURRENT_TIMESTAMP);"
  file.write(sql)
  cursor.execute(sql)
  #rows = cursor.fetchall()
  #for row in rows:
  #  print(row)
  #print(rows[0][3])

  conn.commit()
  #切断
  conn.close

#class UnitID:
#  ID          = 'id'
#  SITE_NAME   = 'site_name'
#  TITLE       = 'title'
#  CONTENT_URL = 'content_url'
#  PIC_URL     = 'pic_url'
#  POST_TIME   = 'post_time'

#unitテーブルへのデータ登録
# @param: unit 単体作品の画像用連想配列の配列
# @param: file file操作オブジェクト
def insertUnit(unit, file):
  #接続
  conn = connectDB()  
  cursor = conn.cursor()
  
  target = "`"+UnitID.ID+"`, `"+UnitID.SITE_NAME+"`, `"+UnitID.TITLE\
  +"`, "+UnitID.CONTENT_URL+", `"+UnitID.PIC_URL+"`, `"+UnitID.POST_TIME+"`"
  
  sql = "INSERT IGNORE INTO `unit` ("+target+") VALUES (NULL, '"+unit[UnitID.SITE_NAME]+"', '"+unit[UnitID.TITLE]+"', '"+unit[UnitID.CONTENT_URL]+"', '"+unit[UnitID.PIC_URL]+"', CURRENT_TIMESTAMP);"
  file.write(sql)
  cursor.execute(sql)
  
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
#  print(categories)
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


#カテゴリ取得
def getCategory_multi(categories):
  category1 = 0
  category2 = 0
  category3 = 0
#  print(categories)
  if len(categories) >= 3:
    category1 = searchCategory(categories[0].text)
    category2 = searchCategory(categories[1].text)
    category3 = searchCategory(categories[2].text)
  elif len(categories) == 2:
    category1 = searchCategory(categories[0].text)
    category2 = searchCategory(categories[1].text)
  elif len(categories) == 1:
    category1 = searchCategory(categories[0].text)
    
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
#スクレイピング - エロ動画もん
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingEromon(soup, fileobj, site_title):
  articles = soup.find_all('div', class_='col-6 col-sm-6 col-md-4 col-lg-3 mb-1 p-1')

  # 連想配列に取得したデータを詰める
  for article in articles:
    categories = article.find('p', class_='tags').find_all('a')
    category = getCategory_multi(categories)

    picture = {PictureID.CATEGORY_ID1: str(category[0]),
               PictureID.CATEGORY_ID2: str(category[1]),
               PictureID.CATEGORY_ID3: str(category[2]),
               PictureID.SITE_NAME: site_title,
               PictureID.TITLE: article.find('h3').text.replace("\n", "").replace("\t", "").replace(" ", ""),
               PictureID.CONTENT_URL: article.find('a')['href'],
               PictureID.PIC_URL: article.find('img')['src'],
               PictureID.DURATION: article.find('div', class_='time p-1 mb-1').text}
    insertPicture(picture, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")

#スクレイピング
#スクレイピング - イベルト！
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingAvevent(soup, fileobj, site_title):
  articles = soup.find_all('li', class_='c-event-list_item')

  # 連想配列に取得したデータを詰める
  for article in articles:
    date_tmp = article.find_all('li', class_='c-event-item_detail-desc')[1].text.replace("\n", "").split("/")
    date_value = datetime.date(int(date_tmp[0]), int(date_tmp[1]), int(date_tmp[2]))
    
    event =   {EventID.NAME: article.find('p', class_='c-event-item_title').text.replace("\u3000", " "),
               EventID.LOCATION: article.find('li', class_='c-event-item_detail-desc').text.replace("\n", ""),
               EventID.DATE: str(date_value),
               EventID.DETAIL: "https://www.av-event.jp"+article.find('a', class_='c-event-item_title-link')['href']}
    insertEvent(event, fileobj)
    
  print(site_title, str(len(articles))+"件見つかりました")

def scrapingFANZA(soup, fileobj, site_title):
  articles = soup.find('div', class_='d-item').find_all('li')

  # 連想配列に取得したデータを詰める
  for article in articles:

    res2 = requests.get(article.find('a')['href'])
    soup2 = BeautifulSoup(res2.text.encode('utf-8'), "html.parser")
    pic_url = soup2.find('img', class_='tdmm')['src']

    unit =    {UnitID.SITE_NAME: SiteName.FANZA,
               UnitID.TITLE: article.find('img')['alt'],
               UnitID.CONTENT_URL: article.find('a')['href'],
               UnitID.PIC_URL: pic_url}

    insertUnit(unit, fileobj)

  print(site_title, str(len(articles))+"件見つかりました")

#スクレイピング
#スクレイピング - テスト
#@param: soup Beautiful Soupの操作用オブジェクト
#@param: fileobj ファイル操作用オブジェクト
#@site_title: サイトタイトル
def scrapingTest(soup, fileobj, site_title):
  articles = soup.find('div', class_='d-item').find_all('li')
  print(articles[0])
#  # 連想配列に取得したデータを詰める
#  for article in articles:
#
#    res2 = requests.get(article.find('a')['href'])
#    soup2 = BeautifulSoup(res2.text.encode('utf-8'), "html.parser")
#    pic_url = soup2.find('img', class_='tdmm')['src']
#
#    unit =    {UnitID.SITE_NAME: SiteName.FANZA,
#               UnitID.TITLE: article.find('img')['alt'],
#               UnitID.CONTENT_URL: article.find('a')['href'],
#               UnitID.PIC_URL: pic_url}
#    print(unit)
#    insertUnit(unit, fileobj)
#
#  print(site_title, str(len(articles))+"件見つかりました")


def scraping(fileobj, site_title, url):
  res = requests.get(url)
#  print(res.text)

  soup = BeautifulSoup(res.text.encode('utf-8'), "html.parser")

  #print(soup)

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
  elif site_title == SiteName.EROMON:
    scrapingEromon(soup, fileobj, site_title)
  elif site_title == SiteName.AV_EVENT:
    scrapingAvevent(soup, fileobj, site_title)
  elif site_title == SiteName.FANZA:
    scrapingFANZA(soup, fileobj, site_title)


##############################
# メイン部
##############################  
dt_now = datetime.datetime.now()
file = dt_now.strftime('%Y%m%d_%H%M')+".sql"
fileobj = codecs.open(file, "w", encoding="utf_8")

#scraping(fileobj, SiteName.TEST, 'https://www.dmm.co.jp/digital/videoa/-/list/search/=/?searchstr=%E7%94%B0%E4%B8%AD%E3%81%AD%E3%81%AD%20%E5%8D%98%E4%BD%93%E4%BD%9C%E5%93%81')
scraping(fileobj, SiteName.NUKISUTO, 'https://www.nukistream.com/')
scraping(fileobj, SiteName.ERO_MOVIE_CAFE, 'http://xvideos-field5.com/')
scraping(fileobj, SiteName.IQOO, 'https://iqoo.me/')
scraping(fileobj, SiteName.POYOPARA, 'https://poyopara.com/')
scraping(fileobj, SiteName.ERONUKI, 'https://ero-nuki.net/')
scraping(fileobj, SiteName.JAVMIXTV, 'https://javmix.tv/video/')
scraping(fileobj, SiteName.EROMON, 'https://eromon.net/')
scraping(fileobj, SiteName.AV_EVENT, 'https://www.av-event.jp/search/?q=%E7%94%B0%E4%B8%AD%E3%81%AD%E3%81%AD')
scraping(fileobj, SiteName.FANZA, 'https://www.dmm.co.jp/digital/videoa/-/list/search/=/?searchstr=%E7%94%B0%E4%B8%AD%E3%81%AD%E3%81%AD%20%E5%8D%98%E4%BD%93%E4%BD%9C%E5%93%81')

fileobj.close()

os.remove(file)