import requests
from bs4 import BeautifulSoup as bs
import re
import urllib.request as urllib2
import lxml
import random

# create random user agent generator
def random_user_agent():
    user_agent_list = [
        #Chrome
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        #Firefox
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
    ]
    return random.choice(user_agent_list)


# create random proxy generator
def random_proxy():
    proxy_list = [
        'http://' + str(random.randint(128,191)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + ':8080',
        'https://' + str(random.randint(128,191)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + ':8080',
        'socks4://' + str(random.randint(128,191)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + ':8080',
        'socks5://' + str(random.randint(128,191)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + ':8080'
    ]
    return random.choice(proxy_list)

# setup proxy in requests
def setup_proxy():
    proxy = random_proxy()
    proxies = {
        'http': proxy,
        'https': proxy
    }
    return proxies


class Scraper:
    def __init__(self, url , user_agent=None, proxy=None):
        proxy = random_proxy()
        proxies = {
            'http': proxy,
        }
        user_agent = random_user_agent()
        self.__headers = {
            'User-Agent': f'{self.user_agent}',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }
        self.__url = url
        self.__req = requests.get(self.__url,headers=self.__headers, proxies=proxies)
        self.__soup = bs(self.__req.text, 'lxml')
        self.__data = []

    def get_flipkart_data(self):
        div = self.__soup.find_all('div', attrs={'class': '_1AtVbE col-12-12'})
        if len(div) == 1:
            print('No results found')
        else:
            for i in div:
                i = i.find('div', attrs={'data-id': re.compile('(.*?)')})
                if i == None:
                    pass
                else:
                    try:
                        title = i.find(
                            'img', attrs={'class': re.compile('(.*?)')}).get('alt')
                        price = i.find('div', attrs={'class': '_30jeq3'}).text
                        href = str(
                            i.find('a', attrs={'href': re.compile('(.*?)')}).get('href'))
                        image_link = i.find(
                            'img', attrs={'class': re.compile('(.*?)')}).get('src')

                        self.__data.append(
                            {'store': 'Flipkart', 'title': title, 'price': price, 'url': 'https://www.flipkart.com' + href, 'image_link': image_link})
                    except:
                        pass
        return self.__data

    def get_amazon_data(self):
        div = self.__soup.find_all(
            'div', attrs={'class': 'template=SEARCH_RESULTS'})
        if len(div) == 0:
            print('No results found')
        else:
            for i in div:
                try:
                    href = i.find(
                        'a', attrs={'class': 'a-link-normal s-no-outline'}).get('href')
                    price = i.find(
                        'span', attrs={'class': 'a-price-whole'}).text
                    title = i.find('span', attrs={
                        'class': re.compile('(.*?) a-color-base a-text-normal')}).text
                    image_link = i.find(
                        'img', attrs={'class': 's-image'}).get('src')
                    self.__data.append(
                        {'store': 'Amazon', 'title': title, 'price': price, 'url': 'https://www.amazon.in' + href, 'image_link': image_link})
                except:
                    pass
        return self.__data

    def get_myntra_data(self):
        # print(self.__req.text)
        div = re.findall(
            r'{"landing(.*)"deliveryPromise":""}', self.__req.text)
        # print(div)
        if len(div) == 0:
            print('No results found')
        else:
            start_url = re.search(r'PageUrl":"(.*?)"',
                                  self.__req.text).group(0)
            start_url = start_url[10:-1]

            product_names = re.findall(
                r'"productName":"(.*?)"', self.__req.text)
            product_price = re.findall(r'"price":(.*?),', self.__req.text)
            product_url_unfiltered = re.findall(
                r'"landingPageUrl":"(.*?)"', self.__req.text)
            product_url_unfiltered.insert(0, start_url)
            product_url = []
            image_unfiltered = re.findall(
                r'"searchImage":"(.*?)"', self.__req.text)
            images = []
            for image in image_unfiltered:
                image = re.sub(r'u002F', '', image)
                image = re.sub(r'\\', '/', image)
                images.append(image)

            for i in product_url_unfiltered:
                i = re.sub(r'u002F', '', i)
                i = re.sub(r'\\', '/', i)
                i = 'https://www.myntra.com/' + i
                product_url.append(i)
            try:
                for title, price, url, image in zip(product_names, product_price, product_url, images):
                    self.__data.append(
                        {'store': 'myntra', 'title': title, 'price': price, 'url': url, 'image_link': image})
            except:
                print('Error No results found')
            # print(self.__data)
        return self.__data

    def get_nykaa_data(self):
        response = urllib2.urlopen(self.__url).read()
        div = re.findall(r'"brandIds"(.*)"type"',str(response))
        if len(div) == 0:
            print('No results found')
        else:
            product_url = re.findall(r'"productURL":"(.*?)"',str(div[0]))
            image_url =re.findall(r'"url":"(.*?)"',str(div[0]))
            product_title = re.findall(r'"title":"(.*?)"',str(div[0]))[0:20]
            product_mrp = re.findall(r'"price":(.*?),',str(div[0]))
            try:
                for title,price ,url,image in zip(product_title,product_mrp,product_url,image_url):
                    self.__data.append(
                        {'store': 'nykaa', 'title': title, 'price': price, 'url': url, 'image_link': image})
            except:
                print('No results found')
        return self.__data

# amazon_url = 'https://www.amazon.in/s?k=cloths&crid=1RQH9INII9MC9&sprefix=cloth%2Caps%2C337&ref=nb_sb_noss_2'

# sc = Scraper(amazon_url).get_amazon_data()
# print(sc)