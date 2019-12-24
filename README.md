## インストール

**git**，**docker**，**docker-compose**入っていることが前提です．

ない方は，調べてインストールしてください．

## デバック

VNC を使うことで，docker 上の Headless Chrome ブラウザにアクセスし，selenium の動作を確認することができます．

### mac を使っている場合

- Finder > 移動 > サーバへ移動 > `vnc://localhost:5900` > 接続
- パスワード：`secret`
- VNC が別ウィンドウで開きます

### windows をつかっている場合

[VNC Viewer](https://www.realvnc.com/)
などをインストールして，`vnc://localhost:5900`にアクセスしましょう

### リポジトリのクローン

```bash
$ git clone https://github.com/sattosan/auto-footstanp.git

# クローンしたディレクトリに入る
$ cd auto-footstanp
```

### コンテナの起動

```bash
$ docker-compose up -d --build
```

### ログインに必要な情報を設定

`.env`を`./src`配下に作成

そして，以下のようにメールアドレスとパスワードを設定する

```txt:./src/.env
EMAIL = "example@gmail.com"
PASSWORD = "password"
```

## 実行

### プログラムの実行

```bash
$ docker-compose run pairs python main.py
```

### ログイン後，足跡つける人数を聞かれるので数字を入力

```bash
何人に足跡つけますか？ 数字を入力してください > 10
```

### 途中で中断する場合

- **Ctrl-c**を入力

```bash
$ dc run --rm pairs python main.py
Starting selenium-hub ... done
何人に足跡つけますか？ 数字を入力してください > 1000
==========1000人に足跡をつけます==========
1人目に足跡ぺた〜
2人目に足跡ぺた〜
^C
app shutdown!
```

## 終了

```bash
$ docker-compose down
```
