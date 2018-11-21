import re
import time
from urllib import parse
from selenium import webdriver
import setting
import requests


class GetTicket:
    def __init__(self):
        '''初始化'''
        # 空缺值为车次号、发车时间（自己出发站）、出发站点、到达站点、出发日期、座位类型
        self.urltemp = 'https://tieyo.trade.qunar.com/site/booking/purchase.jsp?train={}&dptHm={}&fromstation={}&tostation={}&starttime={}&seat={}'
        self.name = setting.USER_NAME
        self.user_id = setting.USER_ID
        self.tel_name = setting.TEL_NAME
        self.tel = setting.TEL_NUMBER
        # 车次
        self.train = setting.TRAIN
        # 出发时间
        self.dptHm = parse.quote(setting.dptHm)
        # 出发站
        self.fromstation = parse.quote(setting.FROMSTATION)
        # 到达站
        self.tostation = parse.quote(setting.TOSTATION)
        # 出发日期
        self.starttime = parse.quote(setting.STARTTIME)
        # 座位类型
        self.seat = parse.quote(setting.SEAT)


        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade - insecure - requests': '1',
        }
        self.url = self.urltemp.format(self.train, self.dptHm, self.fromstation, self.tostation, self.starttime,
                                       self.seat)

    def test_have_ticket(self):
        '''测试是否有票'''
        while True:
            time.sleep(3)
            response = requests.get(self.url, headers=self.headers)
            # print(response.status_code)
            # print(response.content.decode())
            res_str = response.content.decode()
            if re.findall(r'newlayout', res_str):
                print('有票')
                return True
            else:
                print('无票')

    def get_ticket(self):
        '''先测试是否有票，后购买'''
        if self.test_have_ticket():

            self.driver = webdriver.Chrome()
            self.driver.get(self.url)
            time.sleep(5)
            print('开始输入')
            self.driver.find_element_by_xpath('//li[@class="col1"]//input').send_keys(self.name)
            self.driver.find_element_by_xpath('//li[@class="col2"]//input').send_keys(self.user_id)
            self.driver.find_element_by_xpath('//div[@class="q_inpbox contact-name placeholderCon"]/input').send_keys(
                self.tel_name)
            self.driver.find_element_by_xpath('//div[@class="q_inpbox contact-phone placeholderCon"]/input').send_keys(
                self.tel)
            time.sleep(3)
            self.driver.find_element_by_xpath('//*[@id="fillOrder_submit"]/div[3]/button').click()
            # 可以集成发送短信提醒或者邮件提醒或者播放提示声音
            time.sleep(60 * 40)
            self.driver.close()

