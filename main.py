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

# r_session の簡易メモ化（プロセス内キャッシュ）
_R_SESSION_COOKIE_CACHE: str | None = None
_R_SESSION_COOKIE_OBTAINED_AT: datetime | None = None


def get_list_of_icon_files():
    """assetsディレクトリ内のPNGファイルのリストを返す"""
    files = os.listdir("assets")
    png_files = [f for f in files if f.endswith('.png') and f[:-4].isdigit()]
    return png_files

def filename_to_number(filename):
    """ファイル名から番号を抽出する。例: '01.png' -> 1"""
    return int(filename[:-4])  # '.png'を除去して数値に変換

def get_icon_path():
    """アイコン画像のパスを返す。例: assets/01.png"""
    files = get_list_of_icon_files()
    next_icon = files[random.randrange(len(files))]
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


def invalidate_r_session_cookie_cache():
    global _R_SESSION_COOKIE_CACHE, _R_SESSION_COOKIE_OBTAINED_AT
    _R_SESSION_COOKIE_CACHE = None
    _R_SESSION_COOKIE_OBTAINED_AT = None


def get_r_session_cookie_cached():
    """r_session をメモ化して返す（未取得ならログインして取得）。"""
    global _R_SESSION_COOKIE_CACHE, _R_SESSION_COOKIE_OBTAINED_AT
    if _R_SESSION_COOKIE_CACHE:
        return _R_SESSION_COOKIE_CACHE

    cookie = get_r_session_cookie()
    if cookie:
        _R_SESSION_COOKIE_CACHE = cookie
        _R_SESSION_COOKIE_OBTAINED_AT = datetime.now()
    return cookie

def change_icon(icon_path):
    """アイコン画像をtraQ API経由で変更する（r_sessionはメモ化して再利用）"""
    if not os.path.exists(icon_path):
        print(f"{icon_path} が見つかりません")
        return

    url = f"{BASE_URL}/users/me/icon"

    def _put_icon(r_session_cookie: str):
        with open(icon_path, "rb") as f:
            files = {"file": (os.path.basename(icon_path), f, "image/png")}
            cookies = {"r_session": r_session_cookie}
            response = httpx.put(url, files=files, cookies=cookies)
            print("POST先URL:", url)
            return response

    r_session_cookie = get_r_session_cookie_cached()
    if not r_session_cookie:
        print("r_sessionクッキー取得できず、アイコン変更不可")
        return

    response = _put_icon(r_session_cookie)

    # セッションが失効していたら一度だけ取り直して再試行
    if response.status_code in (401, 403):
        invalidate_r_session_cookie_cache()
        new_cookie = get_r_session_cookie_cached()
        if new_cookie:
            response = _put_icon(new_cookie)

    if response.status_code == 204:
        print("アイコン変更に成功しました")
    else:
        print(f"失敗: {response.status_code} {response.text}")

def change_displayname(name):
    """表示名を変更する"""

    def _get_displayname(r_session_cookie: str):
        """
        # get で現在のプロフィールを取得
        url = f"{BASE_URL}/users/me"
        cookies = {"r_session": r_session_cookie}
        response = httpx.get(url, cookies=cookies)

        if response.status_code == 200:
            return response.json().get("displayName")
        else:
            print(f"プロフィール取得失敗: {response.status_code} {response.text}")
            return None
        """
        
        # patch で表示名を変更
        url = f"{BASE_URL}/users/me"
        data = {"displayName": name}
        cookies = {"r_session": r_session_cookie}
        response = httpx.patch(url, json=data, cookies=cookies)
        print("PATCH先URL:", url)
        return response
    
    r_session_cookie = get_r_session_cookie_cached()
    if not r_session_cookie:
        print("r_sessionクッキー取得できず、表示名変更不可")
        return
    
    response = _get_displayname(r_session_cookie)
    if response.status_code in (401, 403):
        invalidate_r_session_cookie_cache()
        new_cookie = get_r_session_cookie_cached()
        if new_cookie:
            response = _get_displayname(new_cookie)
    
    if response.status_code == 204:
        print("表示名変更に成功しました")
    else:
        print(f"失敗: {response.status_code} {response.text}")

def change_profile():
    """アイコンと表示名を変更する"""
    icon_path = get_icon_path()
    change_icon(icon_path)
    # アイコンのファイル名から番号を抽出して表示名にする（例: 01.png -> 1）
    denominator = filename_to_number(os.path.basename(icon_path))
    change_displayname(f"n&(n//{denominator})==0")

if __name__ == "__main__":
    print("アイコン自動変更スケジューラ起動中")
    while True:
        change_profile()
        time.sleep(30)  

