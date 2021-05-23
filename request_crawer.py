# 導入 模組(module) 
import requests 
# 把 到 ptt 八卦版 網址存到URL 變數中
URL = "https://www.ptt.cc/bbs/Gossiping/index.html"
# 設定Header與Cookie
my_headers = {'cookie': 'over18=1;'}
# 發送get 請求 到 ptt 八卦版
response = requests.get(URL, headers = my_headers)
# 印出回傳網頁程式碼
print(response.text)