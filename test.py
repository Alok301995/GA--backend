from telnetlib import XASCII
import requests, json
from bs4 import BeautifulSoup
import re
import concurrent.futures

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

def extract_image_url(data):
    response = requests.get('https://www.flipkart.com'+data)
    div = re.findall(r'{"@context":"http://schema.org","@type":"Product"(.*?)}}' ,response.text)
    image = re.findall(r'"image":"(.*?)"' , div[0])
    return image[0]

def get_flipkart_data():
    s = requests.Session()
    res = s.get("https://www.flipkart.com/search?q=bra&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY&page=2", headers=headers, verify=False)
    data = re.findall(r'"type":"AnswerBoxValue","data":(.*?)],"footer"' , res.text);
    if(len(data) ==0):
        print("No data found")
    else:
        # title = re.findall(r'"title":"(.*?)"' , data[0]);
        url = re.findall(r'"url":"(.*?)"' , data[0]);
        # price = re.findall(r'"values":\["(.*?)"]' , data[0]);
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
            result= executor.map(extract_image_url, url)
        print(list(result))
get_flipkart_data()






    



# with concurrent.futures.ThreadPoolExecutor() as executor:
#     executor.map(extract_image_url, url)





    




