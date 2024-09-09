import argparse
import os
import re
import sys
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
import time

timeout = 5
socket.setdefaulttimeout(timeout)

class Crawler:
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0', 'Cookie': ''}
    __per_page = 30
    __anti_scrape_trigger_count = 0
    __max_anti_scrape_triggers = 5
    __restart_trigger_file = "restart_trigger.txt"

    def __init__(self, t=0.1, word='', total_page=1, start_page=1, per_page=30, delay=0.05):
        self.time_sleep = t
        self.word = word
        self.total_page = total_page
        self.start_page = start_page
        self.per_page = per_page
        self.delay = delay

    @staticmethod
    def get_suffix(name):
        m = re.search(r'\.[^\.]*$', name)
        return m.group(0) if m.group(0) and len(m.group(0)) <= 5 else '.jpeg'

    @staticmethod
    def handle_baidu_cookie(original_cookie, cookies):
        if not cookies:
            return original_cookie
        result = original_cookie
        for cookie in cookies:
            result += cookie.split(';')[0] + ';'
        return result.rstrip(';')

    def save_image(self, rsp_data, word):
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        self.__counter = len(os.listdir('./' + word)) + 1
        for image_info in rsp_data['data']:
            try:
                if 'replaceUrl' not in image_info or len(image_info['replaceUrl']) < 1:
                    continue
                obj_url = image_info['replaceUrl'][0]['ObjUrl']
                thumb_url = image_info['thumbURL']
                url = 'https://image.baidu.com/search/down?tn=download&ipn=dwnl&word=download&ie=utf8&fr=result&url=%s&thumburl=%s' % (urllib.parse.quote(obj_url), urllib.parse.quote(thumb_url))
                time.sleep(self.time_sleep)
                suffix = self.get_suffix(obj_url)
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')]
                urllib.request.install_opener(opener)
                filepath = './%s/%s' % (word, str(self.__counter) + str(suffix))
                urllib.request.urlretrieve(url, filepath)
                if os.path.getsize(filepath) < 5:
                    print("下载到了空文件，跳过!")
                    os.unlink(filepath)
                    continue
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print("图片+1,已有" + str(self.__counter) + "张图片")
                self.__counter += 1
        return

    def get_images(self, word):
        search = urllib.parse.quote(word)
        pn = self.__start_amount
        while pn < self.__amount:
            url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%s&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=&hd=&latest=&copyright=&word=%s&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn=%s&rn=%d&gsm=1e&1594447993172=' % (search, search, str(pn), self.__per_page)
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                self.headers['Cookie'] = self.handle_baidu_cookie(self.headers['Cookie'], page.info().get_all('Set-Cookie'))
                rsp = page.read()
                page.close()
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                rsp_data = json.loads(rsp, strict=False)
                if 'data' not in rsp_data:
                    self.__anti_scrape_trigger_count += 1
                    if self.__anti_scrape_trigger_count >= self.__max_anti_scrape_triggers:
                        print("触发反爬机制过多次，准备重启程序...")
                        self.trigger_restart()
                        return
                    print("触发了反爬机制，自动重试！")
                else:
                    self.__anti_scrape_trigger_count = 0
                    self.save_image(rsp_data, word)
                    print("下载下一页")
                    pn += self.__per_page
        print("下载任务结束")
        return

    def trigger_restart(self):
        with open(self.__restart_trigger_file, "w") as f:
            f.write("Trigger Restart")
        sys.exit()

    def start(self, word, total_page=1, start_page=1, per_page=30):
        self.__per_page = per_page
        self.__start_amount = (start_page - 1) * self.__per_page
        self.__amount = total_page * self.__per_page + self.__start_amount
        self.word = word
        self.total_page = total_page
        self.start_page = start_page
        self.per_page = per_page
        self.get_images(word)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--word", type=str, help="抓取关键词", required=True)
        parser.add_argument("-tp", "--total_page", type=int, help="需要抓取的总页数", required=True)
        parser.add_argument("-sp", "--start_page", type=int, help="起始页数", required=True)
        parser.add_argument("-pp", "--per_page", type=int, help="每页大小", choices=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100], default=30, nargs='?')
        parser.add_argument("-d", "--delay", type=float, help="抓取延时（间隔）", default=0.05)
        args = parser.parse_args()

        crawler = Crawler(args.delay, args.word, args.total_page, args.start_page, args.per_page)
        crawler.start(args.word, args.total_page, args.start_page, args.per_page)
    else:
        crawler = Crawler(0.05)
        crawler.start('背部穴位', 5, 1, 30)
