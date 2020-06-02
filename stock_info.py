import requests
import sys
import re
import json
import DB_table
import apscheduler
import traceback
import datetime
import time
import os




# Sina API
def get_stock_info(*args):
	url_stock_info_temp = 'https://hq.sinajs.cn/list={}'
	exchange_code_list = ','.join(args)
	url = url_stock_info_temp.format(exchange_code_list)
	stock_info_list = requests.get(url).text
	stock_info_list = re.findall(r'=(.*);', stock_info_list)
	stock_list = []
	for i,stock_info in enumerate(stock_info_list):
		s = stock_info.split(',')
		exchange_code = args[i][2:]
		stock_name = s[0]
		opening_price = s[1]
		closing_price = s[2]
		current_price = s[3]
		today_highest_price = s[4]
		today_lowest_price = s[5]
		bid_price = s[6]
		auction_price = s[7]
		trading_volume = s[8]
		trading_amount_yuan = s[9]
		B1 = [s[10],s[11]]
		B2 = [s[12],s[13]]
		B3 = [s[14],s[15]]
		B4 = [s[16],s[17]]
		B5 = [s[18],s[19]]
		S1 = [s[20],s[21]]
		S2 = [s[22],s[23]]
		S3 = [s[24],s[25]] 
		S4 = [s[26],s[27]]
		S5 = [s[28],s[29]]
		date = s[30]
		time = s[31]
		stock_list.append(DB_table.stock(exchange_code, stock_name, opening_price, closing_price, current_price, \
			today_highest_price, today_lowest_price, bid_price, auction_price, trading_volume, \
				trading_amount_yuan, B1, B2, B3, B4, B5, S1, S2, S3, S4, S5, date, time))
	# for elem in stock_list:
	# 	elem.show_object()
	return stock_list

# @param 
#	mode = min/daily/weekly/monthly
#	code = sh******/sz******
def get_stock_graph(mode, code):
	exchange_code = code[2:]
	now_time = datetime.datetime.now()
	now_time = now_time.strftime("%Y-%m-%d_%H-%M-%S")
	filepath = os.path.abspath('') + '\\stock_graph\\{}\\{}_{}.jpg'.format(exchange_code, now_time, mode)
	url_graph_temp = 'http://image.sinajs.cn/newchart/{}/n/{}.gif'
	url = url_graph_temp.format(mode, code)
	print(url)
	graph = requests.get(url)
	with open(filepath, 'wb') as f:
		f.write(graph.content)
 
# TongHuaShun API
def get_history_data(exchange_code):
	url_temp = 'http://d.10jqka.com.cn/v6/line/hs_{}/01/all.js'
	url = url_temp.format(exchange_code)
	header = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36\
			(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
		"Referer": "http://stockpage.10jqka.com.cn/HQ_v4.html"
	}
	DB_access = False
	try:
		html = requests.get(url, headers=header).text
	except:
		print('http requests error')
	try:
		history_data = re.search(r'.*?\((.*)\)',html).group(1)
		history_data_json = json.loads(history_data)

		history_year_data = history_data_json['sortYear']
		history_dates_data = history_data_json['dates'].split(',')
		history_price_data = history_data_json['price'].split(',')
		history_daily_volume = history_data_json['volumn'].split(',')

		history_dates = []
		sum_days = 0
		for year, days in history_year_data:
			for i in range(days):
				date = '{}-{}-{}'.format(year, history_dates_data[i + sum_days][0:2],\
					history_dates_data[i + sum_days][2:])
				history_dates.append(date)	
			sum_days = sum_days + days

		history_daily_lowest = []
		history_daily_opening = []
		history_daily_highest = []
		history_daily_closing = []
		for idx in range(int(len(history_price_data) / 4)):
			base_price = int(history_price_data[idx * 4])
			history_daily_lowest.append(base_price)
			history_daily_opening.append(base_price + int(history_price_data[idx * 4 + 1]))
			history_daily_highest.append(base_price + int(history_price_data[idx * 4 + 2]))
			history_daily_closing.append(base_price + int(history_price_data[idx * 4 + 3]))
		
		history_stock_info = []
		for idx in range(len(history_dates)):
			lowest_price = float(history_daily_lowest[idx])/100
			opening_price = float(history_daily_opening[idx])/100
			highest_price = float(history_daily_highest[idx])/100
			closing_price = float(history_daily_closing[idx])/100
			volume = history_daily_volume[idx] # 股数
			date = history_dates[idx]
			history_stock_info.append(DB_table.history_stock(exchange_code, lowest_price, opening_price,\
				highest_price, closing_price, volume, date))
		
		DB_access = True
	except Exception as e:
		print(e)
		traceback.print_exc()
		print('scheme not find ---> DB is not able to access')
	
	if DB_access:
		# exchange_code = history_stock_info[0].exchange_code
		# lowest_price = history_stock_info[0].lowest_price
		# opening_price = history_stock_info[0].opening_price
		# highest_price = history_stock_info[0].highest_price
		# closing_price = history_stock_info[0].closing_price
		# volume = history_stock_info[0].volume
		# date = history_stock_info[0].date
		# print('exchange_code = {}\tlowest_price = {}\topening_price = {}\thighest_price = {}\tclosing_price = {}\tvolume = {}\tdate = {}'.format(exchange_code, lowest_price, opening_price,\
		# 		highest_price, closing_price, volume, date))
		return (history_stock_info, DB_access)
	
	else:
		return ([],DB_access)

		
		