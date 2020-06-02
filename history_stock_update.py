import sys
import os
import pymysql
import bs4
import requests
import time
import datetime
import traceback
from stock_info import get_history_data
from DB_table import history_stock

def history_stock_to_DB(exchange_code):
	try_times = 3
	while(try_times > 0):
		(history_stock_info, DB_access) = get_history_data('600436')
		time.sleep(8)
		if DB_access:
			break
		try_times -= 1
	if not DB_access:
		print('DATA ACCQUIRE ERROR')
		sys.exit()


	mysql_config = {
		"host": "localhost",
		"port": 3306,
		"user": "root",
		"password": "li1231",
		"charset": "utf8mb4"
	}

	connection = pymysql.connect(**mysql_config)
	cursor = connection.cursor()
	cursor.execute('USE guba')

	for history_stock in history_stock_info:
		exchange_code = history_stock.exchange_code
		lowest_price = history_stock.lowest_price
		opening_price = history_stock.opening_price
		highest_price = history_stock.highest_price
		closing_price = history_stock.closing_price
		date = history_stock.date
		sql = 'REPLACE INTO history_stock(exchange_code, lowest_price, opening_price, highest_price,\
				closing_price, date) VALUES("{}","{}","{}","{}","{}","{}")'.format(exchange_code, lowest_price,\
				opening_price, highest_price, closing_price, date)

		connection.ping(reconnect=True)
		cursor.execute(sql)
		connection.commit()

