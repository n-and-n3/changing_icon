import os
from datetime import datetime
import httpx
import dotenv

# .envファイルから環境変数を読み込む
dotenv.load_dotenv()

# 必要な情報を環境変数から取得
BASE_URL = os.getenv("BASE_URL")               # 例: https://q.trap.jp/api/v3
TRAQ_USERNAME = os.getenv("TRAQ_USERNAME")     # traQのユーザー名
TRAQ_PASSWORD = os.getenv("TRAQ_PASSWORD")     # traQのパスワード

def get_today_icon_path():
    """今日の日付に対応するアイコン画像のパスを返す。例: assets/01.png"""
    today = datetime.now().day
    return f"assets/{today:02d}.png"

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
    icon_path = get_today_icon_path()
    if not os.path.exists(icon_path):
        print(f"{icon_path} が見つかりません")
        return

    r_session_cookie = get_r_session_cookie()
    if not r_session_cookie:
        print("r_sessionクッキー取得できず、アイコン変更不可")
        return
    print(r_session_cookie)

    with open(icon_path, "rb") as f:
        files = {'file': (os.path.basename(icon_path), f, 'image/png')}
        cookies = {"r_session": r_session_cookie}
        url = f"{BASE_URL}/users/me/icon"
        response = httpx.put(url, files=files, cookies=cookies)

        print("POST先URL:", url)
        print("r_session:", cookies.get("r_session"))

    if response.status_code == 204:
        print("アイコン変更に成功しました")
    else:
        print(f"失敗: {response.status_code} {response.text}")

if __name__ == "__main__":
    change_icon()