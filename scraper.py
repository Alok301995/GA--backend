import requests
from bs4 import BeautifulSoup as bs
import re
import urllib.request as urllib2


class Scraper:
    def __init__(self, url):
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        }
        self.__url = url
        self.__req = requests.get(
            url, headers=self.__headers)
        self.__soup = bs(self.__req.text, 'html.parser')
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
        print(self.__req.text)
        div = re.findall(
            r'{"landing(.*)"deliveryPromise":""}', self.__req.text)
        print(div)
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
            print(self.__data)
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
