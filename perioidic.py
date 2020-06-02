import os
import sys
import pymysql
import threading
from stock_info import get_stock_graph
from stock_info import get_stock_info
from apscheduler.schedulers.blocking import BlockingScheduler

def get_stock_data():
	mysql_config = {
			"host": "localhost",
			"port": 3306,
			"user": "root",
			"password": "li1231",
			"charset": "utf8mb4"
	}
	connection = pymysql.connect(**mysql_config)
	cursor = connection.cursor()
	cursor.execute('USE realtime_stock')

	def periodically_info_to_DB(*args, connection, cursor):
		stock_info_list = get_stock_graph(args)
		for stock_info in stock_info_list:
			sql = 'INSERT INTO realtime_stock(exchange_code, current_price, date_time, trading_volume, trading_amount_yuan)\
				 VALUES("{}","{}","{}","{}","{}")'. \
					 format(stock_info.exchange_code, stock_info.current_price, stock_info.trading_volume, stock_info.trading_amount_yuan)
	sched = BlockingScheduler()
	sched.add_job(get_stock_info('sh600000'), trigger='cron', day='mon-fri', hour='9-12, 13-15', seconds='*/3')



