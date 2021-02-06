# regza-digest-auth
get digest authentication password from REGZA Apps Connect v2 API

レグザAppsコネクトのユーザー名とパスワードを設定できない最新のREGZAでDigest認証用のIDとパスワードを発行する

## How to use

1. REGZAの設定

#### `ネットワーク設定` -> `ネットワーク接続設定` -> `詳細設定` -> `アドレス設定（IPv4）` 

IPアドレスを `手動設定` にして、任意のアドレスに固定する

#### `ネットワーク設定` -> `外部連携設定` -> `レグザAppsコネクト`

`利用する` に変更する

2. IPアドレスとユーザーIDを書き換える

`register.py` を開き、 `ip` に前項で固定したIPアドレスを、 `user_id` に任意のMACアドレス形式のユーザーIDを記述する

```python
ip = "192.168.0.123" # set your REGZA IP Address
user_id = "AA-AA-AA-AA-AA-AA" # set any user ID (MAC address format)
```

3. 実行

パッケージのインストール

```shell
$ pip3 install -r requirements.txt
```

REGZAの電源を入れ、設定画面などを開いていないテレビ視聴状態で `register.py` を実行する

```shell
$ python3 register.py
```

REGZAの画面に表示される4桁の数字を入力すると、ユーザーIDとパスワードが表示される

```
pin: 1445
user_id: AA-AA-AA-AA-AA-AA
user_pw: Q9uDdC7=nGFo!KnCWP:XMCaW!1byRKcE
Registration successful.
```

取得したユーザーIDとパスワードは従来の `/remote/` の他、 `/v2/remote/` などのv2 APIへのアクセスに使用できる

- `/v2/remote/play/status` (method=GET)
- `/v2/remote/status/mute` (method=GET)
- `/v2/remote/settings/channel_list` (method=GET)

etc...