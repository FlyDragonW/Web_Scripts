import requests
nid = 1234
url = f'https://example.com/ischool/widget/site_news/news_query_json_content.php?nid={nid}&dir=0&uid=WID_0_2_0f075596d6cfd282f38872677912f105e9857086'
times = 1000000

for i in range(times):
    print(f'{i+1}/{times}')
    response = requests.get(url)
