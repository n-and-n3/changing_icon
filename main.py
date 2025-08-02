import os
from datetime import datetime
import httpx
import dotenv

# .envファイルから環境変数を読み込む
dotenv.load_dotenv()

# 必要な情報を環境変数から取得
BASE_URL = os.getenv("BASE_URL")          # 例: https://q.trap.jp/api/v3
SECRET_COOKIE = os.getenv("SECRET_COOKIE")  # traQのr_sessionクッキー

def get_today_icon_path():
    """今日の日付に対応するアイコン画像のパスを返す。例: icons/01.png"""
    today = datetime.now().day
    return f"assets/{today:02d}.png"

def change_icon():
    """アイコン画像をtraQ API経由で変更する"""
    icon_path = get_today_icon_path()
    if not os.path.exists(icon_path):
        print(f"{icon_path} が見つかりません")
        return

    with open(icon_path, "rb") as f:
        files = {'file': (os.path.basename(icon_path), f, 'image/png')}
        cookies = {"r_session": SECRET_COOKIE}
        url = f"{BASE_URL}/users/me/icon"
        response = httpx.post(url, files=files, cookies=cookies)

    if response.status_code == 204:
        print("アイコン変更に成功しました")
    else:
        print(f"失敗: {response.status_code} {response.text}")

if __name__ == "__main__":
    change_icon()