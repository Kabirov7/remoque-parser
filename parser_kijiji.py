import mysql.connector
import requests
from bs4 import BeautifulSoup
import config as const


class Parser():
    def __init__(self):
        self.URL = ''
        self.HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
           'accept': '*/*'}
        self.DB = mysql.connector.connect(host=const.HOST, user=const.USER, password=const.MYSQL_PASSWORD, database=const.DATABASE_NAME, auth_plugin='mysql_native_password')
        self.MY_CURSOR = self.DB.cursor()
        self.name_table = ''
        self.pages_count = ''
        self.host = ''

    def change_const(self):
        self.URL = ''
        self.name_table = ''
        self.pages_count = ''
        return  self.URL, self.name_table


    def get_html(self, url, params=None):
        self.r = requests.get(url, headers=self.HEADERS, params=params)
        return self.r

    def get_content(self, html):
        pass

    def save_sql(self, items):
        self.MY_CURSOR.execute(f'CREATE TABLE if not exists {self.name_table}(ID int PRIMARY KEY AUTO_INCREMENT, title text, id_add bigint, price text, description text, link text, new_ boolean default true)')
        self.MY_CURSOR.execute(f"update {self.name_table} set new_=true")

        for self.i in items:
            self.MY_CURSOR.execute(f'select * from {self.name_table} where id_add="{self.i["id_add"]}"')
            self.theme = self.MY_CURSOR.fetchone()
            if self.theme == None:
                self.sqlFormula = f'INSERT INTO {self.name_table}(title, id_add, price, description, link) VALUES (%s,%s,%s,%s,%s)'
                self.remoque = ([self.i['title'], self.i['id_add'], self.i['price'], self.i['description'], self.i['link']])
                self.MY_CURSOR.execute(self.sqlFormula, self.remoque)
            else:
                self.MY_CURSOR.execute(f'update {self.name_table} set new_=false where id_add="{self.i["id_add"]}" or id_add is null')
            self.DB.commit()

    def main(self):
        self.change_const()
        self.html = self.get_html(self.URL)
        if self.html.status_code == 200:
            self.change_const()
            self.remoques = []
            for self.page in range(self.pages_count+1):
                self.html = self.get_html(self.URL, params={"page": self.page})
                self.remoques.extend(self.get_content(self.html.text))
        self.save_sql(self.remoques)

class remorque(Parser):
    def change_const(self):
        self.URL = 'https://www.kijiji.ca/b-vehicules-recreatifs-tentes-roulottes/quebec/remorque/k0c172l9001?price=250__350&price-type=fixed'
        self.name_table = 'remorque'
        self.pages_count = 2
        self.host = 'https://www.kijiji.ca/'

        return self.URL, self.name_table, self.pages_count, self.host

    def get_content(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.items = self.soup.find_all('div', class_='clearfix')


        self.content = []
        for self.i in self.items:
            self.content.append({
                'title': self.i.find_next('div', class_='title').get_text().replace('\n', '').replace('                           ','').replace('                       ',''),
                'id_add': self.i.find_previous('div').get('data-listing-id'),
                'price': self.i.find_next('div', class_='price').get_text().replace('\n', '').replace(' ','')[:3],
                'description': self.i.find_next('div', class_='description').get_text().replace('\n', '').replace('                            ','').replace('                        ','').replace('            ','').replace('$',''),
                'link': self.host + self.i.find_next('a', class_='title').get('href'),
            })
        print(self.content)
        return self.content

