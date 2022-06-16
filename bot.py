#Stock bot
#@author Robert Federline
#@date 6/15/22
#unspagettied as of 6/10/22

import math
from requests.exceptions import ConnectionError
import datetime
import requests
from bs4 import BeautifulSoup
import os
#import shutil

os.system("") #makes sure that the ANSI escape sequences work correcly


#ANSI escape sequences for color
COLOR = {
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

class bot:

    #initializer for bot
    def __init__(self,stock_amount,stock_held,tic,balance,date):
        self.stock_amount = stock_amount
        self.balance = balance
        self.stock_held = stock_held
        self.last_stock_held = stock_held
        self.tic = tic
        
        #creates files   
        self.title = str(self.tic)+"_"+date+".txt"
        self.titlep = str(self.tic)+"_prices_"+date+".txt"
        self.data_title = str(self.tic)+"_"+date+"_data.txt"
        try:
            file = open(self.title, "x")
            price_file = open(self.titlep, "x")
            data_file = open(self.data_title, "x")
        except FileExistsError:
            print("[  RESTART  ]")
            file = open(self.title, "a")
            price_file = open(self.titlep, "a")
            data_file = open(self.data_title, "a")
            file.write("[  RESTART  ]")
            price_file.write("[  RESTART  ]")
            data_file.write("[  RESTART  ]")

        file.close()
        price_file.close()
        data_file.close()

    def day_change(self,date):

        #for moving datafiles
        #os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
        #os.replace("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
        #shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

        #changes files and clears prices list
        self.data_title = str(self.tic)+"_"+date+"_data.txt"
        data_file = open(self.data_title, "x")
        self.title = str(self.tic)+"_"+date+".txt"
        file = open(self.title, "x")
        self.titlep = str(self.tic)+"_prices_"+date+".txt"
        price_file = open(self.titlep, "x")
        data_file.close()
        file.close()
        price_file.close()
        self.prices.clear()

    #buy method
    def buy(self,price):
        ct = datetime.datetime.now()
        stock = math.floor(self.balance/price)
        self.balance=self.balance-stock*price
        self.stock_held=self.stock_held+stock

        #cancels if there isnt enough money to complete transaction
        if (self.balance<0.00):
            self.balance = self.balance + stock*price
            self.stock_held = self.stock_held - stock
            if (self.balance>0.00): #may be depreciated
                stock = int(self.balance/price)
                self.balance=self.balance-stock*price
                self.stock_held=self.stock_held+stock
            print(ct,COLOR["RED"],"| ",self.tic," | Transaction Failed, Insufficent Funds",COLOR["ENDC"])
            file = open(self.title, "a")
            file.write(str(ct)+"| Failed buy"+"\n")
            file.close()
        else:
            if (stock==0):
                print(ct,COLOR["RED"],"| ",self.tic," | Transaction Failed, Insufficent Funds",COLOR["ENDC"])
                file = open(self.title, "a")
                file.write(str(ct)+"| Failed buy"+"\n")
                file.close()
            else:
                print(ct,COLOR["RED"],"| Buy ",self.tic," Price:",price," Amount:",stock," Total:",(stock*price),COLOR["ENDC"])
                text = str(ct)+"| Buy "+self.tic+" Price:"+str(price)+" Amount:"+str(stock)+" Total:"+str(stock*price)
                file = open(self.title, "a")
                file.write(text+"\n")
                file.close()
                self.last_buy_price=price

    #sell method
    def sell(self,price):
        ct = datetime.datetime.now()
        self.balance = self.balance + self.stock_held * price
        prev_stock_held = self.stock_held
        self.stock_held = self.stock_held - self.stock_held

        #cancels if there isnt enough stock to complete transaction
        if (self.stock_held<0):
            self.balance = self.balance - self.stock_held * price
            self.stock_held = self.stock_held + self.stock_held
            print(ct,COLOR["RED"],"| ",self.tic," | Transaction Failed, Insufficent Stock",COLOR["ENDC"])
            text = (str(ct)+"| Failed Sell")
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
        else:
            print(ct,COLOR["GREEN"],"| Sell ",self.tic," Price:",price," Amount:",prev_stock_held," Total:",(prev_stock_held*price),COLOR["ENDC"])
            text = str(ct)+"| Sell "+str(self.tic)+" Price:"+str(price)+" Amount:"+str(prev_stock_held)+" Total:"+str(prev_stock_held*price)
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()

    #starts the bot, gets inital price
    def start(self):

        #sets headers and url
        self.headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
        self.url = "https://www.wsj.com/market-data/quotes/"+self.tic.upper()+"/financials"

        try:

            #getting the response from wsj
            response = requests.get(self.url,headers=self.headers)
            ct = datetime.datetime.now()
            print(ct,COLOR["BLUE"],"|",self.tic,"| Response Delay:",response.elapsed," Response Size: ",(len(response.content)/1000),"KB",COLOR["ENDC"])
            soup = BeautifulSoup(response.text,"lxml")
            results = soup.find(id = "quote_val")
            self.prices = [float(results.text)]

        #catches exception of a connection error so that it doesnt terminate program
        except ConnectionError:
            ct = datetime.datetime.now()
            text = str(ct)+"| Connection Timeout"
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
            return str(ct)+COLOR["RED"]+"| Connection Timeout"+COLOR["ENDC"]
        except requests.exceptions.RequestException:
            ct = datetime.datetime.now()
            text = str(ct)+"| Connection Timeout"
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
            return str(ct)+COLOR["RED"]+"| Connection Timeout"+COLOR["ENDC"]
        except AttributeError:
            ct = datetime.datetime.now()
            text = str(ct)+"| Attribute Error"
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
            return str(ct)+COLOR["RED"]+"| Attribute Error"+COLOR["ENDC"]

    #used for updating the bot, checking price and buying or selling if the market situation is right
    def check_price(self,time_elapsed,mode):

        try:

            #getting the response from wsj
            response = requests.get(self.url,headers=self.headers)
            ct = datetime.datetime.now()
            print(ct,COLOR["BLUE"],"|",self.tic,"| Response Delay:",response.elapsed," Response Size: ",(len(response.content)/1000),"KB",COLOR["ENDC"])
            soup = BeautifulSoup(response.text,"lxml")

            #finds the price
            results = soup.find(id = "quote_val")
            price = float(results.text)
            self.previous_price = price

            #writes price to price file
            price_file = open(self.titlep, "a")
            price_file.write(str(datetime.datetime.now())+"|"+str(price)+"\n")
            price_file.close() 

            #setting up the list the will be used to determine if there is a peak or a low
            if (len(self.prices)<5):
                self.prices.append(price)
            else:
                self.prices[0] = self.prices[1]
                self.prices[1] = self.prices[2]
                self.prices[2] = self.prices[3]
                self.prices[3] = self.prices[4]
                self.prices[4] = price               

            #mode 1, sells and buys on the second continuation of the trend
            if (mode==1):
                #limiter to sell if the stock is after a peak
                if time_elapsed>(4):
                    if (self.prices[2]>self.prices[0] and self.prices[2]>self.prices[1]):
                        if (self.prices[2]>self.prices[3] and self.prices[2]>self.prices[4]):
                            if (self.stock_held>0):
                                if (price>self.last_buy_price):
                                    self.sell(price)
                                    self.last_sell_price=price

                #limiter to buy if the stock is after a low
                if time_elapsed>(4):
                    if (self.prices[2]<self.prices[0] and self.prices[2]<self.prices[1]):
                        if (self.prices[2]<self.prices[3] and self.prices[2]<self.prices[4]):
                            if self.balance>0.00:
                                self.buy(price)

            #mode 2, sells and buys on the first change in direction
            if (mode==2):
                #limiter to sell if the stock is after a peak
                if time_elapsed>(4):
                    if (self.prices[3]>self.prices[0] and self.prices[3]>self.prices[1]):
                        if (self.prices[3]>self.prices[2] and self.prices[3]>self.prices[4]):
                            if (self.stock_held>0):
                                if (price>self.last_buy_price):
                                    self.sell(price)
                                    self.last_sell_price=price

                #limiter to buy if the stock is after a low
                if time_elapsed>(4):
                    if (self.prices[3]<self.prices[0] and self.prices[3]<self.prices[1]):
                        if (self.prices[3]<self.prices[2] and self.prices[3]<self.prices[4]):
                            if self.balance>0.00:
                                self.buy(price)

            #mode 3, compares to the previous price
            if (mode==3):
                #limiter to sell if the price is greater than the last price
                if (self.previous_price<price):
                    if (self.stock_held>0):
                        if (price>self.last_buy_price):
                            self.sell(price)
                            self.last_sell_price=price

                #limiter to buy if the price is less than the last price
                if (self.previous_price>price):
                    if self.balance>0.00:
                        self.buy(price)
            
            if ((self.stock_held*price)+self.balance<400):
                self.sell(price)
                self.last_sell_price=price
            
            if (self.stock_held>self.last_stock_held):
                transaction_state = "Buy"
            if (self.stock_held<self.last_stock_held):
                transaction_state = "Sell"
            else:
                transaction_state = "None"

            self.last_stock_held = self.stock_held
            self.previous_price = price
            #returns update string and prints update to file
            ct = datetime.datetime.now()
            text = str(ct)+"  | "+str(self.tic)+" | min "+str(time_elapsed)+"\tprice:"+str(price)+"\tbalance:"+str(self.balance)+"\tStock Held:"+str(self.stock_held)+"\tMoney in Stocks:"+str(self.stock_held*price)+"\tTotal Balance:"+str((self.stock_held*price)+self.balance)

            data = str(ct)+" Price:"+str(price)+" Tot Balance:"+str((self.stock_held*price)+self.balance)+" "+transaction_state
            data_file = open(self.data_title, "a")
            data_file.write(data)

            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
            return text
        
        #catches exception of a connection error so that it doesnt terminate program
        except ConnectionError:
            ct = datetime.datetime.now()
            text = str(ct)+"| Connection Timeout"
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
            data_file = open(self.data_title, "a")
            data_file.write(text)
            data_file.close()
            return str(ct)+COLOR["RED"]+"| Connection Timeout"+COLOR["ENDC"]
        except requests.exceptions.RequestException:
            ct = datetime.datetime.now()
            text = str(ct)+"| Connection Timeout"
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
            data_file = open(self.data_title, "a")
            data_file.write(text)
            data_file.close()
            return str(ct)+COLOR["RED"]+"| Connection Timeout"+COLOR["ENDC"]
        except AttributeError:
            ct = datetime.datetime.now()
            text = str(ct)+"| Attribute Error"
            file = open(self.title, "a")
            file.write(text+"\n")
            file.close()
            data_file = open(self.data_title, "a")
            data_file.write(text)
            data_file.close()
            return str(ct)+COLOR["RED"]+"| Attribute Error"+COLOR["ENDC"]
