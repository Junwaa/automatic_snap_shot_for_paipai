import time
import requests
import re
import sys

# 1. Paste the product ID
# 2. Enter the expected price When the time is 2 seconds remaining and the price is lower than the expected price
# 3 Enter a cookie
ID = sys.argv[1]  # product ID
my_price = int(sys.argv[2])  # expected price
y = 3  # increase rate
s = 2  # waiting for refresh time


c=''
# Set the above c


HEADERS = {
    'Referer': 'https://paipai.jd.com/auction-detail/113158389',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
    'Cookie': ''
}
HEADERS['Cookie'] = c
url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'


# Get current price & remaining time
def get_pricetime():
    r_url = 'https://used-api.jd.com/auction/detail?auctionId=' + ID + '&callback=__jp1'
    r = requests.get(r_url, headers=HEADERS)
    p_url = 'https://used-api.jd.com/auctionRecord/getCurrentAndOfferNum?auctionId=' + \
        ID + '&callback=__jp17'
    p = requests.get(p_url, headers=HEADERS)
    cur_price = re.findall(r"currentPrice\":(.+?),", p.text)
    c_time = re.findall(r"currentTime\":\"(.+?)\"", r.text)
    e_time = re.findall(r"endTime\":(.+?),", r.text)
    cur_price = ''.join(cur_price)
    c_time = ''.join(c_time)
    e_time = ''.join(e_time)
    c_time = (float(e_time) - float(c_time)) / 1000  # 计算剩余时间并换算成秒
    name = re.findall(r"model\":\"(.+?)\",", r.text)
    coloer = re.findall(r"quality\":\"(.+?)\",", r.text)
    print(name + coloer, end='')
    return cur_price, str(c_time)


def buy(price):
    buy_url = 'https://used-api.jd.com/auctionRecord/offerPrice'
    data = {
        'trackId': '3b154f3a78a78f8b6c2eea5a3cee5674',
        'eid': 'UTT4AVFUIZFVD6KGHHJRAGEEGFJ4MWFSOPDUEF7KBEHDA5ODK3GKDKP5PCVTWIAQ32N2ZT2AR5YBAH3T27354OAI3Q',

    }
    data['price'] = str(int(price))
    data['auctionId'] = str(ID)
    # print(data)
    resp = requests.post(buy_url, headers=HEADERS, data=data)
    print(resp.json())


try:
    while True:
        p = get_pricetime()
        print('ID:' + ID + ',the current price is:' +
              p[0] + 'the remaining time' + p[1] + ',expected price:' + str(my_price))
        x = p[0]
        x = float(x)
        tt = p[1]
        tt = float(tt)
        if x > my_price:
            sys.exit()

        if tt > 50:
        	# s = tt - 50
            s = 40
        elif 15 < tt <= 50:
        	s = 2
        elif tt <= 15:
            s = 1
        if x <= my_price and tt <= 2:
            print('Start to increase the price: the markup amount is' + str(x + y))
            buy(x + y)
        if my_price < x <= my_price + y and tt <= 2:
            print('Start to increase the price: the markup amount is' + str(my_price + y))
            buy(my_price + y)
        if x <= my_price and tt < 8 and s != 0.1:
            s = 0.1
            print('Start to accelerate' + str(s))
        time.sleep(s)  # waiting for refresh time
        if tt < -1:
            print('End of program')
            break
except KeyboardInterrupt:
    print('Stopped')
