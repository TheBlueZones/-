import requests
import time

def get_data(uid: str):
    """爬取微博用户信息"""
    base_url = f"https://m.weibo.cn/api/container/getIndex"
    params = {
        "type": "uid",
        "value": uid,
        "containerid": f"100505{uid}"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Referer": "https://m.weibo.cn/",
        "Accept": "application/json, text/plain, */*",
    }

    try:
        response = requests.get(base_url, params=params, headers=headers)
        time.sleep(3)  # 延时3秒防止被反爬
        return response.json()
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

if __name__ == "__main__":
    user_id = "1749127163"
    user_data = get_data(user_id)
    print(user_data)