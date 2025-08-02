import os
from datetime import datetime
import httpx
import dotenv
import schedule
import time
import random

dotenv.load_dotenv()

BASE_URL = os.getenv("BASE_URL")
TRAQ_USERNAME = os.getenv("TRAQ_USERNAME")
TRAQ_PASSWORD = os.getenv("TRAQ_PASSWORD")

# 必要な情報を環境変数から取得
BASE_URL = os.getenv("BASE_URL")               # 例: https://q.trap.jp/api/v3
TRAQ_USERNAME = os.getenv("TRAQ_USERNAME")     # traQのユーザー名
TRAQ_PASSWORD = os.getenv("TRAQ_PASSWORD")     # traQのパスワード

def get_icon_path():
    """アイコン画像のパスを返す。例: assets/01.png"""
    files = os.listdir("assets")
    md_files = [i for i in files if i.endswith('.png') == True]
    next_icon = md_files[random.randrange(len(md_files))]
    return f"assets/{next_icon}"

def get_r_session_cookie():
    login_url = f"{BASE_URL}/login"
    login_data = {
        "name": TRAQ_USERNAME,
        "password": TRAQ_PASSWORD
    }
    response = httpx.post(login_url, json=login_data)
    # ステータスコード204でもOK
    if response.status_code in [200, 204, 302]:
        # Set-Cookieヘッダーからr_sessionの値を抽出
        set_cookie = response.headers.get("set-cookie")
        if set_cookie:
            # r_session=xxxxxx; ... の形式からxxxxxxだけ抜き出す
            import re
            m = re.search(r"r_session=([^;]+)", set_cookie)
            if m:
                return m.group(1)
            else:
                print("Set-Cookieヘッダーにr_sessionが見つかりません")
                return None
        else:
            print("Set-Cookieヘッダーがありません")
            return None
    else:
        print(f"ログイン失敗: {response.status_code} {response.text}")
        return None

def change_icon():
    """アイコン画像をtraQ API経由で変更する（毎回新しいr_sessionを取得）"""
    icon_path = get_icon_path()
    if not os.path.exists(icon_path):
        print(f"{icon_path} が見つかりません")
        return

    r_session_cookie = get_r_session_cookie()
    if not r_session_cookie:
        print("r_sessionクッキー取得できず、アイコン変更不可")
        return

    with open(icon_path, "rb") as f:
        files = {'file': (os.path.basename(icon_path), f, 'image/png')}
        cookies = {"r_session": r_session_cookie}
        url = f"{BASE_URL}/users/me/icon"
        response = httpx.put(url, files=files, cookies=cookies)

        print("POST先URL:", url)

    if response.status_code == 204:
        print("アイコン変更に成功しました")
    else:
        print(f"失敗: {response.status_code} {response.text}")

# スケジュール設定（例: 毎日0:00に実行）
schedule.every().day.at("20:45").do(change_icon)

if __name__ == "__main__":
    print("アイコン自動変更スケジューラ起動中")
    while True:
        schedule.run_pending()
        time.sleep(30)  

