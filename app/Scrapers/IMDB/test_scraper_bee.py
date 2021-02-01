import requests

def send_request():
    response = requests.get(
        url="https://www.imdb.com/title/tt0077687/?ref_=fn_al_tt_1",
        params={
            "api_key": "KR42SXJZ1FQO7IJFFC1WGCPB116Y0079AKINLNE9FW2GBQ9ASZX0AOH6KM62F8G106J55COEGK2RR158",
            "url": "https://www.imdb.com/title/tt0077687/?ref_=fn_al_tt_1",
        },

    )
    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.content)
send_request()