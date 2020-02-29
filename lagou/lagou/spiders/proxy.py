import requests
from fake_useragent import UserAgent
from lxml.etree import HTML
import MySQLdb
import time
conn = MySQLdb.connect(host='192.168.227.130', user='root', passwd='123456', db='spider', charset='utf8')
cursor = conn.cursor()

# url = 'http://www.baidu.com'
# proxy = {'https':'114.226.161.133:9999'}
# re = requests.get(url, proxies=proxy)
# print (re.status_code)
ua = UserAgent()

class GetIp(object):

    def delete_ip(self, ip):
        delete_sql = "DELETE FROM proxy where ip='{0}'".format(ip)
        cursor.execute(delete_sql)
        conn.commit()

    def test_ip(self, ip, port, proxy_type):
        url = 'https://www.baidu.com'
        proxy = {proxy_type.lower(): "{0}://{1}:{2}".format(proxy_type.lower(), ip, port)}
        try:
            response = requests.get(url, proxies=proxy)
            time.sleep(1)
        except Exception as e:
            #print('无效的ip:', ip)
            self.delete_ip(ip)
            return False
        else:
            if response.status_code == 200:
                #print('可用ip:', ip)
                return True
            else:
                #print('无效ip:', ip)
                self.delete_ip(ip)
                return False
    def get_ip(self):
        random_ip = '''
            SELECT proxy_type, ip, port FROM proxy ORDER BY RAND() LIMIT 1
        '''
        result = cursor.execute(random_ip)
        for info in cursor.fetchall():
            proxy_type = info[0]
            ip = info[1]
            port = info[2]
            result = self.test_ip(ip, port, proxy_type)
            if result:
                return "{0}://{1}:{2}".format(proxy_type.lower(), ip, port)
            else:
                self.get_ip()
def insert_sql(ip, port, proxy_type):
    cursor.execute(
        "insert into proxy(ip, port, proxy_type) values('{0}', '{1}', '{2}')".format(ip, port, proxy_type)
    )
    conn.commit()


def get_html():
    headers = {'User-Agent': ua.random}
    url = 'https://www.xicidaili.com/wt/{}'
    for i in range(1, 4):
        full_url = url.format(str(i))
        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            parse_html(response.text)

def parse_html(html):
    response = HTML(html)
    data_list = response.xpath("//table[@id='ip_list']//tr[contains(@class, 'odd')]")
    for data in data_list:
        ip = data.xpath('./td[2]/text()')
        port = data.xpath('./td[3]/text()')
        proxy_type = data.xpath('./td[6]/text()')
        if ip and port and proxy_type:
            insert_sql(ip[0], port[0], proxy_type[0])

def test():
    url = ''
if __name__ == "__main__":
    #get_html()
    a = GetIp()
    for i in range(10):
        print(a.get_ip())