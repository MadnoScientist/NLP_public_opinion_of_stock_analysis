# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy
import urllib.request
import os

class Spider:
    def __init__(self):
        self.exCodes = []
        self.url_list = []
        self.stock_name = []

        # Base url of gb.com
        url_temp = "http://gb.eastmoney.com/list,{}"
    
        # 各股股吧首页网址 -> self.url_list
        urls = []
        filepath = os.path.abspath("") + "\\exCode_list.txt"
        with open(filepath, encoding = "UTF-8") as f:
            for line in f.readlines():
                exchange_code = line.split(" ")[1]
                exchange_code = exchange_code[1:-2]
                self.exCodes.append(exchange_code)
                self.stock_name.append(line)
                # without .html
                urls.append(url_temp.format(exchange_code))  
        f.close()
        self.url_list = urls

    # Get posts from each stock
    def get_all_htmls(self):
        # idx.358 -- 片仔癀
        # Get all urls of each stock from page 1 to page 50
        # urls[index][pages] where index is refer to stock sequences
        urls = []
        index = 0
        for stock_url in self.url_list:
            urls.append([])
            for page in range(1,51):
                urls[index].append((stock_url + "_{}.html").format(page))
            index = index + 1
      
        # Save the html of every page
        for i in range(16,index):
            for page in range(0, 50):
                html = self.getHtml(urls[i][page])
                savePath = os.path.abspath("") + "/html" + \
                    "/{}/{}".format(self.exCodes[i], page)
                self.saveHtml(savePath, html)

    def getHtml(self, url):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request, timeout = 8)
        html = response.read()
        return html

    def saveHtml(self, file_name, file_content):
        with open(file_name + '.html','wb') as f:
            f.write(file_content)
        
        


    # def start_requests(self):
    #     urls = []
    #     for page in range(1,50) :
    #         ## data source: 股吧-片仔癀
    #         ## Keyword = 片仔癀, 股
    #         url = "http://gb.eastmoney.com/list,600436_%d.html" (page)
    #         urls.append(url)

    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    # def parse_url(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    # def get_one_page(self, url):

        
