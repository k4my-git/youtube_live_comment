from bs4 import BeautifulSoup
import json
import requests
import requests_html
from urllib.parse import urlparse, parse_qs
import sys
import csv
import time

vid = input("insert ID >>")
target_url = "https://youtu.be/" + vid
dict_str = ""
next_url = ""
comment_data = []
session = requests_html.HTMLSession()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}

# まず動画ページにrequestsを実行しhtmlソースを手に入れてlive_chat_replayの先頭のurlを入手
resp = session.get(target_url)
resp.html.render(sleep=3)
for iframe in resp.html.find("iframe"):
    if("live_chat_replay" in iframe.attrs["src"]):
        next_url= "".join(["https://www.youtube.com", iframe.attrs["src"]])

try:
    while(1):
        try:
            time.sleep(2)
            html = session.get(next_url, headers=headers)
            soup = BeautifulSoup(html.text,"lxml")

            # 次に飛ぶurlのデータがある部分をfind_allで探してsplitで整形
            for scrp in soup.find_all("script"):
                if "window[\"ytInitialData\"]" in scrp.next:
                    dict_str = scrp.next.split(" = ", 1)[1]

            # 辞書形式と認識すると簡単にデータを取得できるが, 末尾に邪魔なのがあるので消しておく（「空白2つ + \n + ;」を消す）
            dict_str = dict_str.rstrip("  \n;")
            # 辞書形式に変換
            dics = json.loads(dict_str)

            # "https://www.youtube.com/live_chat_replay?continuation=" + continue_url が次のlive_chat_replayのurl
            continue_url = dics["continuationContents"]["liveChatContinuation"]["continuations"][0]["liveChatReplayContinuationData"]["continuation"]
            next_url = "https://www.youtube.com/live_chat_replay?continuation=" + continue_url
            # dics["continuationContents"]["liveChatContinuation"]["actions"]がコメントデータのリスト。
            for samp in dics["continuationContents"]["liveChatContinuation"]["actions"][1:]:
                #comment_data.append(str(samp)+"\n")
                if 'addChatItemAction' not in samp["replayChatItemAction"]["actions"][0]:
                    continue
                if 'liveChatTextMessageRenderer' not in samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]:
                    continue
                str1 = str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["message"]["runs"])
                if 'emoji' in str1:
                    continue
                if "-" in str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]):
                    continue
                str1 = str1.replace('[','').replace('{\'text\': \'','').replace('\'}','').replace(', ','').replace(']','')
                litle_cdata = []
                litle_cdata.append(str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]))
                print(str(samp["replayChatItemAction"]["actions"][0]["addChatItemAction"]["item"]["liveChatTextMessageRenderer"]["timestampText"]["simpleText"]))
                litle_cdata.append(str1)
                comment_data.append(litle_cdata)

        # next_urlが入手できなくなったら終わり
        except Exception:
            break
except KeyboardInterrupt:
    sys.exit()
    

# （動画ID）.txt にコメントデータを書き込む
#url = urlparse(target_url)
#query = parse_qs(url.query)
#url = target_url.replace("https://youtu.be/","")
#title = query["v"][0] + ".txt"
title = vid + ".csv"

with open(title, mode='w', encoding='CP932', errors='replace', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(comment_data)