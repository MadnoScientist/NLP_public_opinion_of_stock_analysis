import os
import pymysql
import sys
import csv
import html.parser
import re
import urllib.request
from DB_table import post
from bs4 import BeautifulSoup


def post_update():
	exCode_list = []
	filepath = os.path.abspath("") + "\\exCode_list.txt"
	with open(filepath, encoding = "UTF-8") as f:
		for line in f.readlines():
			exchange_code = line.split(" ")[1]
			exchange_code = exchange_code[1:-2]
			exCode_list.append(exchange_code)  
	f.close()

	structed_Posts = []
	for code in exCode_list[0:9]:
		for page in range(50):
			filePath = os.path.abspath("") + "\\html\\{}\\{}.html".format(code, page)
			f = open(filePath, encoding = "UTF-8")
			soup = BeautifulSoup(f, features = "html.parser")
		
			post_list = soup.find_all(name='div', attrs={'class': 'articleh normal_post'})
			for item in post_list:
				readings_num = item.find(name='span', attrs={'class': 'l1 a1'}).text
				comments_num = item.find(name='span', attrs={'class': 'l2 a2'}).text
				post_title = item.find(name='span', attrs={'class': 'l3 a3'}).string
				#poster_info = item.find(name='span', attrs={'class': 'l4 a4'}).a.get('href')
				post_date_time = item.find(name='span', attrs={'class': 'l5 a5'}).string
				Url = item.find(name='span', attrs={'class': 'l3 a3'}).a.get('href')

			# cjztb = 冲击涨停 & cfhpl = 财富评论 & cjpl = 财经评论 & fangtan = 访谈 & 未被删帖(贴名存在)
				if((not "cjztb" in Url) and (not "cfhpl" in Url) and \
					(not "cjpl" in Url) and (not "fangtan" in Url) and \
					(not "qa_list" in Url) and (not post_title == "None") and \
					(not "ask" in Url)):
					try:
						Url = Url.split(".")[0]
						exchange_code = Url.split(",")[1]
						post_id = Url.split(",")[2]
						structed_Posts.append(post(exchange_code, post_id, readings_num, \
							comments_num, post_title, post_date_time))
					except:
						print("ERROR, URL = {}, exchange_code = {}, page = {}".format(Url, code, page))
	mysql_config = {
		"host": "localhost",
		"port": 3306,
		"user": "root",
		"password": "li1231",
		"charset": "utf8mb4"
		}

	connection = pymysql.connect(**mysql_config)

	cursor_post = connection.cursor()
	cursor_comment = connection.cursor()
	cursor_post.execute('USE guba')
	cursor_comment.execute('USE guba')

	for post_Info in structed_Posts:

		exchange_code = post_Info.getExchange_code()
		post_id = post_Info.getPost_id()
		readings_num = post_Info.getReadings_num()
		comments_num = post_Info.getComments_num()
		post_title = post_Info.getPost_title()
		post_date_time = post_Info.getPost_date_time()

		sql = 'INSERT IGNORE INTO post(exchange_code, post_id, \
			readings_num, comments_num, \
			post_title, post_date_time) VALUES ("{}","{}","{}","{}","{}","{}");'.\
			format(exchange_code, post_id, readings_num, comments_num, post_title, post_date_time) 

		try:
			cursor_post.execute(sql)
			connection.commit()
		except:
			print("Exception: Exchange_code:{}\tPost_ID:{}\tReadings_num:{}\tComments_num:{}\tPost_title:{}\tPost_date_time:{}". \
				format(exchange_code, post_id, readings_num, comments_num, post_title, post_date_time))

