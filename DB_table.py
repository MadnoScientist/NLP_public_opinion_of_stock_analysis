class post:
    def __init__(self, exchange_code, post_id, readings_num, comments_num, post_title, post_date_time):
        self.exchange_code = exchange_code
        self.post_id = post_id
        self.readings_num = readings_num
        self.comments_num = comments_num
        self.post_title = post_title
        self.post_date_time = post_date_time
        #self.poster_id = poster_id

    def setExchange_code(self, exchange_code):
        self.exchange_code = exchange_code
    
    def setPost_id(self, post_id):
        self.post_id = post_id

    def setReadings_num(self, readings_num):
        self.readings_num = readings_num
    
    def setComments_num(self, comments_num):
        self.comments_num = comments_num
    
    def setPost_title(self, post_title):
        self.post_title = post_title
    
    def setPost_date_time(self, post_date_time):
        self.post_date_time = post_date_time
    
    def getExchange_code(self):
        return self.exchange_code

    def getPost_id(self):
        return self.post_id
    
    def getReadings_num(self):
        #if self.readings_num =
        return self.readings_num
    
    def getComments_num(self):
        #if self.readings_num =
        return self.comments_num
    
    def getPost_title(self):
        return self.post_title
    
    def getPost_date_time(self):
        return self.post_date_time

class comment:
    def __init__(self, comment_id, exchange_code, post_id, comment_content, like_num, comment_time):
        self.comment_id = comment_id
        self.exchange_code = exchange_code
        self.post_id = post_id
        #self.user_id = user_id
        self.comment_content = comment_content
        self.like_num = like_num
        self.comment_time = comment_time
        #self.binded_comment_id = binded_comment_id

    def setComment_id(self, comment_id):
        self.comment_id = comment_id
    
    def setExchange_code(self, exchange_code):
        self.exchange_code = exchange_code

    def setPost_id(self, post_id):
        self.post_id = post_id

    def setComment_content(self, comment_content):
        self.comment_content = comment_content

    def setLike_num(self, like_num):
        self.kike_num = like_num
    
    def setBinded_comment_id(self, binded_comment_id):
        self.binded_comment_id = binded_comment_id
    
    def setComment_time(self, comment_time):
        self.comment_time = comment_time
    
    def getComment_id(self):
        return self.comment_id
    
    def getExchange_code(self):
        return self.exchange_code

    def getPost_id(self, post_id):
        return self.post_id

    def getComment_content(self):
        return self.comment_content

    def getLike_num(self, like_num):
        return self.like_num
    
    def getComment_time(self, comment_time):
        return self.comment_time
    
    # def getBinded_comment_id(self):
    #     return self.binded_comment_id

class history_stock:
    def __init__(self, exchange_code, lowest_price, opening_price, highest_price, closing_price, volume, date):
        self.exchange_code = exchange_code
        self.lowest_price = lowest_price
        self.opening_price = opening_price
        self.highest_price = highest_price
        self.closing_price = closing_price
        self.volume = volume
        self.date = date

class stock:
    def __init__(self, exchange_code, stock_name, opening_price, closing_price, current_price, \
        today_highest_price, today_lowest_price, bid_price, auction_price, trading_volume, trading_amount_yuan, \
            B1, B2, B3, B4, B5, S1, S2, S3, S4, S5, date, time):
            self.exchange_code = exchange_code
            self.stock_name = stock_name
            self.opening_price = opening_price
            self.closing_price = closing_price
            self.current_price = current_price
            self.today_highest_price = today_highest_price
            self.today_lowest_price = today_lowest_price
            self.bid_price = bid_price
            self.auction_price = auction_price
            self.trading_volume = trading_amount_yuan
            self.trading_amount_yuan = trading_amount_yuan
            self.B1 = B1
            self.B2 = B2
            self.B3 = B3
            self.B4 = B4
            self.B5 = B5
            self.S1 = S1
            self.S2 = S2
            self.S3 = S3
            self.S4 = S4
            self.S5 = S5
            self.date = date
            self.time = time

    def show_object(self):
        print('STOCK_NAME = {}'.format(self.stock_name))
        print('------------------------------------------------------------------------------------------------------------------------------------------------')
        print('opening_price = {}\t closing_price = {}\t current_price = {}.'. \
            format(self.opening_price, self.closing_price, self.current_price))
        print('today_highest_price = {}\t today_lowest_price = {}\t bid_price = {}\t auction_price = {}'. \
            format(self.today_highest_price, self.today_lowest_price, self.bid_price, self. auction_price))
        print('trading_volume = {}\t trading_amount_yuan = {}\t'.format(self.trading_volume, self.trading_amount_yuan))
        print('B1 = {}\t B2 = {}\t B3 = {}\t B4 = {}\t B5 = {}'.format(self.B1, self.B2, self.B3, self.B4, self.B5))
        print('S1 = {}\t S2 = {}\t S3 = {}\t S4 = {}\t S5 = {}'.format(self.S1, self.S2, self.S3, self.S4, self.S5))
        print('Time: {} {}'.format(self.date, self.time))
        print('------------------------------------------------------------------------------------------------------------------------------------------------')
