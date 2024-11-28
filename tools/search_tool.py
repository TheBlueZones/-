import requests
import re
from typing import List
from urllib.parse import quote


def get_UID(flower: str) -> List[str]:
    search_query = quote(f"{flower}")
    url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)",
        "Accept": "application/json, text/plain, */*",
        "X-Requested-With": "XMLHttpRequest",
        "MWeibo-Pwa": "1",
        "Referer": "https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        uids = []
        if 'data' in data and 'cards' in data['data']:
            for card in data['data']['cards']:
                if 'mblog' in card and 'user' in card['mblog']:
                    uid = card['mblog']['user']['id']
                    uids.append(str(uid))

        return uids[:3] if uids else []

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []