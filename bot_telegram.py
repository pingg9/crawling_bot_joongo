import json
import requests
import time
import os

# telegram chatbot
def send_to_telegram(text):

    TELEGRAM_TOKEN = "CHATBOT TOKEN"

    # 봇에게 보낸 메시지 받기
    url = "https://api.telegram.org/bot{}/getUpdates".format(TELEGRAM_TOKEN)
    res = requests.get(url)
    res_json = json.loads(res.text)

    # chat_id, msg 파싱
    chat_id = res_json["result"][-1]["message"]["from"]["id"]
    # msg = res_json["result"][-1]["message"]["text"]
    
    # 봇으로 메시지 전송하기
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
    requests.get(url, params = {"chat_id" : chat_id, "text" : text})

# crawling
def search_item(options):
    newdata = options['newdata']
    send_lists = []
    while True:
        keyword = options['keyword']
        min_price = options['min_price']
        max_price = options['max_price']
        delay = options['delay']

        # JSON 타입으로 API 요청
        url = 'https://search-api.joongna.com/v25/search/product'
        data = {"filter":{"categoryDepth":0,"categorySeq":0,"dateFilterParameter":{"sortEndDate":"","sortStartDate":""},"flawedYn":0,"fullPackageYn":0,"limitedEditionYn":0,"maxPrice":2000000000,"minPrice":0,"productCondition":-1,"tradeType":0},"osType":2,"searchQuantity":40,"searchStartTime":"2020-10-03 22:49:30","searchWord":keyword,"sort":"RECENT_SORT","startIndex":0,"productFilter":"ALL"}    
        res = requests.post(url, json=data)

        # JSON 응답 데이터 파싱
        result = res.json()
        result_items = result['data']['items']
        for nb in reversed(result_items):
            if min_price <= nb['price'] <= max_price:
                date = nb['sortDate'][11:]
                title = nb['title']
                price = nb['price']
                if nb['seq'] == 0:
                    href = nb['articleUrl']
                else:
                    href = 'https://m.joongna.com/product-detail/'+str(nb['seq'])

                # 중복 데이터 check
                send = True
                for s in send_lists:
                    if s["title"] == title:
                        #print("중복 데이터")
                        send = False
                        break

                if send == True:
                    # telegram api 호출
                    if newdata == True:                        
                        text = '{} - {}\n가격: {}\n{}'.format(date, title, price, href)
                        send_to_telegram(text)
                        print(text)

                    send_lists.append({
                    "date": date,
                    "title": title,
                    "price": price
                    })

        newdata = True
        now = time.localtime()
        print("reset time: %02d:%02d:%02d" % (now.tm_hour, now.tm_min, now.tm_sec))
        time.sleep(delay)

if __name__== "__main__":
    # start
    options = {
        "keyword": "노트북",
        "min_price": 100000,
        "max_price": 600000,
        "delay": 20,
        "newdata": True
    }

    search_item(options)

        
