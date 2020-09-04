import json
import requests
import time
import os

# kakao api
def send_to_kakao(text):
    KAKAO_TOKEN = "ACCESS TOKEN"
    header = {"Authorization": "Bearer " + KAKAO_TOKEN}
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        }
    }
    data = {"template_object": json.dumps(post)}

    return requests.post(url, headers=header, data=data)

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
        for nb in result_items:
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

                # kakao 메시지 발송
                if send == True and newdata == True:
                    text = '{} - {}\n가격: {}\n{}'.format(date, title, price, href)
                    r = send_to_kakao(text)
                    print(text)
                    print(r.text)

                # 중복 데이터 check
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
        "delay": 60,
        "newdata": False
    }

    search_item(options)
        
