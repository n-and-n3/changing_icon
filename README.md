# changing_icon
アイコンを変えるボットの中身

## セットアップ

Debian/Ubuntu 系では PEP 668 により、システム Python に対して `pip install` が拒否されることがあります。
このリポジトリは `venv` を作ってその中に依存を入れてください。

### 1) venv を作成

```bash
sudo apt update
sudo apt install -y python3-venv

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
```

### 2) 環境変数を設定

`.env` を作成して、以下を設定します。

```env
BASE_URL=https://q.trap.jp/api/v3
TRAQ_USERNAME=your_name
TRAQ_PASSWORD=your_password
```

### 3) 実行

```bash
source .venv/bin/activate
python main.py
```
