# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pymysql

begin_time = int(time.time())
# 结束页数
end_page = 214

borrow_url = 'https://www.58klc.com/Borrow/index/p/'
# 无头版本chrome driver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(chrome_options=chrome_options)

# browser = webdriver.Chrome()
# browser.maximize_window()
browser.implicitly_wait(10)

# 打开数据库连接
# 运行时加上数据库配置
db = pymysql.connect("")
# 使用cursor()方法获取操作游标
cursor = db.cursor()

for curr_page in range(0, end_page):
    curr_time = int(time.time())
    print(curr_page + 1)
    curr_url = borrow_url + str(curr_page + 1)
    print(curr_url)
    browser.get(curr_url)
    bs4 = BeautifulSoup(browser.page_source, 'html.parser')
    lists = bs4.find_all('div', {'class': 'list-item'})
    for ele in lists:
        # 项目id
        borrow_href = ele.a['href']
        borrow_nid = borrow_href.split('/')[-1].replace('+','')
        # print(borrow_nid)
        # 项目标题
        borrow_name = ele.find('div', {'class': 'project-title'}).get_text().strip()
        # print(borrow_name)
        # 项目年化收益
        borrow_interest_rate = float(ele.span.string.strip())
        # print(borrow_interest_rate)
        # 项目期限
        borrow_day = int(ele.find('div', {'class': 'project-day'}).span.string[:-1])
        # print(borrow_day)
        # 项目金额
        borrow_amount = float(ele.find(style='float:right;font-size: 14px;margin-right: 20px;').span.string[:-1])
        # print(borrow_amount)

        # 入库
        try:
            # 执行sql语句
            cursor.execute(
                'insert into test_python_pull_borrow(borrow_nid, borrow_name, borrow_interest_rate, borrow_day, borrow_amount, addtime) values ("{}", "{}", "{}", "{}","{}","{}")'.format(
                    borrow_nid,
                    borrow_name, borrow_interest_rate,
                    borrow_day, borrow_amount, curr_time))
            # cursor.execute('insert into test_python_pull_borrow values("%s", "%s", "%d", "%d", "%d")' % \
            #                (borrow_nid, borrow_name, borrow_interest_rate, borrow_day, borrow_amount))
            # 执行sql语句
            db.commit()
        except:
            # 发生错误时回滚
            db.rollback()
            print('入库失败')

# 关闭数据库连接
db.close()
print('全部数据拉取成功')
end_time = int(time.time())
print('开始于' + str(begin_time) +', 结束于' + str(end_time),',一共执行' + str(end_time-begin_time) + '秒')
