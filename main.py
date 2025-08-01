import httpx

with open(r"\\wsl.localhost\Ubuntu\home\kanat\develop\changing_icon\assets\n3.png", "rb") as f:
    files = {'file': ('r\\wsl.localhost\Ubuntu\home\kanat\develop\changing_icon\assets\n3.png', f, 'image/png')}
    response = httpx.post(
        "https://q.trap.jp/api/v3/users/me/icon",
        files=files,
        cookies={"r_session": "nQe6Vg2JDSRXVe1Nb48ll4txI0mQ3sEtjT0SONMFcVmbuoYZvS"}
    )
    print(response.status_code)