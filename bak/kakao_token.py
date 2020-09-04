import requests

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "REST API KEY",
    "redirect_uri" : "https://localhost.com",
    "code"         : "AUTH TOKEN"
    
}
response = requests.post(url, data=data)

tokens = response.json()

print(tokens)