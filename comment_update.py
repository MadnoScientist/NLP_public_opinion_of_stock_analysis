import sys
import os
import pymysql
import bs4
import requests
import re
import json
import random
import time
import datetime
import traceback
from DB_table import comment

start_time = datetime.datetime.now()
mysql_config = {
	"host": "localhost",
	"port": 3306,
	"user": "root",
	"password": "li1231",
	"charset": "utf8mb4"
}

headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36\
	(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


# Connect DB and create DB cursor
connection = pymysql.connect(**mysql_config)
cursor_post = connection.cursor()
cursor_comment = connection.cursor()

cursor_post.execute('USE guba')
cursor_comment.execute('USE guba')
url_temp = "http://gb.eastmoney.com/news,{},{}_{}.html"

# Exception handling
errorUrl_list = []

# Exchange_code = 600000 --> 浦发银行
cursor_post.execute("SELECT exchange_code, post_id, comments_num FROM post WHERE exchange_code = '600000'")
data = cursor_post.fetchall()
total_time = 0

structed_comments = []
post_pages_count = 1


for exchange_code, post_id, comments_num in data:
	if('万' in comments_num):
		comments_num = comments_num.replace('万','')
		comments_num = float(comments_num) * 10000 
	end_page = int(1 + int(comments_num) / 30)
	comment_id = 1
	first_post_flag = True

	print('http://gb.eastmoney.com/news,{},{}.html\t comment_num = {}\t page_num = {} '. \
		format(exchange_code, post_id, comments_num, end_page))
	print('--------------------------------------------------------------------------------------------------------------------------------------------')
	
	for page in range(1, end_page + 1):
		url = url_temp.format(exchange_code, post_id, page)
		try:
			response = requests.get(url, headers=headers, timeout=12)
			html = response.text
			post_article = re.search(r'var post_article = (.*);',html).group(1)
			reply_list = re.search(r'var reply_list=(.*);',html).group(1)
			if (post_article is None) or (reply_list is None):
				errorUrl_list.append((exchange_code, post_id, end_page))
				print('Error_URL_Num = {}'.format(len(errorUrl_list)))
				break
			else:
				if(first_post_flag):
					post_article_json = json.loads(post_article)
					first_comment_content = bs4.BeautifulSoup(post_article_json \
						['post']['post_content'],features="html.parser").get_text()
					first_like_num = post_article_json['post']['post_like_count']
					first_comment_time = post_article_json['post']['post_publish_time']
					sql = 'REPLACE INTO comment(comment_id, exchange_code,\
							post_id, comment_content, like_num, comment_time) VALUES("{}","{}","{}","{}","{}","{}")'.\
							format(0, exchange_code, post_id, first_comment_content, first_like_num, first_comment_time)
					
					connection.ping(reconnect=True)
					cursor_comment.execute(sql)
					connection.commit()
					first_post_flag = False
				
				reply_list_json = json.loads(reply_list)
				sleep_time = random.randint(8,12)
				total_time += sleep_time
				time.sleep(sleep_time)
				for idx in range(30):
						try:
							comment_content = reply_list_json['re'][idx]['reply_text']
							like_num = reply_list_json['re'][idx]['reply_like_count']
							comment_time = reply_list_json['re'][idx]['reply_publish_time']
							sql = 'REPLACE INTO comment(comment_id, exchange_code,\
							post_id, comment_content, like_num, comment_time) VALUES("{}","{}","{}","{}","{}", "{}")'.\
								format(comment_id, exchange_code, post_id, comment_content, like_num, comment_time)
						except:
							sql = ''
						try:
							connection.ping(reconnect=True)
							cursor_comment.execute(sql)
							connection.commit()
							comment_id += 1
						except:
							continue
				run_time = (datetime.datetime.now() - start_time).seconds
				print('{}: exchange_code = {}\t post_id = {}\t page = {}\t sleep_time = {}s\t pause_time = {}s\t run_time = {}s'.\
					format(post_pages_count, exchange_code, post_id, page, sleep_time, total_time, run_time))
				post_pages_count += 1		
		except Exception as e:
			print("Exception: http requests failed")
			errorUrl_list.append((exchange_code, post_id, end_page))
			print('Error_URL_Num = {}'.format(len(errorUrl_list)))
			traceback.print_exc()		
	print('--------------------------------------------------------------------------------------------------------------------------------------------\n')
		
try_times = 5
while(try_times >= 0):
	for errorUrl in errorUrl_list:
		errorUrl_list.remove(errorUrl)
		for page in range(1, errorUrl[2] + 1):
			url = url_temp.format(errorUrl[0], errorUrl[1], page)
			try:
				response = requests.get(url, headers=headers, timeout=12)
				html = response.text
				post_article = re.search(r'var post_article = (.*);',html).group(1)
				reply_list = re.search(r'var reply_list=(.*);',html).group(1)
				if (post_article is None) or (reply_list is None):
					errorUrl_list.append((errorUrl[0], errorUrl[1], errorUrl[2]))
					print('Error_URL_Num = {}'.format(len(errorUrl_list)))
					break
				else:
					if(first_post_flag):
						post_article_json = json.loads(post_article)
						first_comment_content = bs4.BeautifulSoup(post_article_json \
							['post']['post_content'],features="html.parser").get_text()
						first_like_num = post_article_json['post']['post_like_count']
						first_comment_time = post_article_json['post']['post_publish_time']
						sql = 'REPLACE INTO comment(comment_id, exchange_code,\
								post_id, comment_content, like_num, comment_time) VALUES("{}","{}","{}","{}","{}","{}")'.\
								format(0, exchange_code, post_id, first_comment_content, first_like_num, first_comment_time)
						
						connection.ping(reconnect=True)
						cursor_comment.execute(sql)
						connection.commit()
						first_post_flag = False
					
					reply_list_json = json.loads(reply_list)
					sleep_time = random.randint(8,12)
					total_time += sleep_time
					time.sleep(sleep_time)
					for idx in range(30):
							try:
								comment_content = reply_list_json['re'][idx]['reply_text']
								like_num = reply_list_json['re'][idx]['reply_like_count']
								comment_time = reply_list_json['re'][idx]['reply_publish_time']
								sql = 'REPLACE INTO comment(comment_id, exchange_code,\
								post_id, comment_content, like_num, comment_time) VALUES("{}","{}","{}","{}","{}", "{}")'.\
									format(comment_id, exchange_code, post_id, comment_content, like_num, comment_time)
							except:
								sql = ''
							try:
								connection.ping(reconnect=True)
								cursor_comment.execute(sql)
								connection.commit()
								comment_id += 1
							except:
								continue
					run_time = (datetime.datetime.now() - start_time).seconds
					print('{}: exchange_code = {}\t post_id = {}\t page = {}\t sleep_time = {}s\t pause_time = {}s\t run_time = {}s'.\
						format(post_pages_count, exchange_code, post_id, page, sleep_time, total_time, run_time))
					post_pages_count += 1		
			except Exception as e:
				print("Exception: http requests failed")
				errorUrl_list.append((errorUrl[0], errorUrl[1], errorUrl[2]))
				print('Error_URL_Num = {}'.format(len(errorUrl_list)))
				traceback.print_exc()
	try_times -= 1

		

cursor_comment.close()
cursor_post.close()
print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^DONE^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')

			
			
			
			
			



		
		