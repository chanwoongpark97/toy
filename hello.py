import requests # requests 라이브러리 설치 필요

r = requests.get('http://spartacodingclub.shop/sparta_api/seoulair')
rjson = r.json()

gus = rjson['RealtimeCityAir']['row']

for gu in gus:
	if gu['IDEX_MVL'] < 35:
		print (gu['MSRSTE_NM'], gu['IDEX_MVL'])

# 설치한 라이브러리
# requests
# bs4
# pymongo
# dnspython
# flask
