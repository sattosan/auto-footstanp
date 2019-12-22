## インストール

### リポジトリのクローン

```bash
$ git clone https://github.com/sattosan/auto-footstanp.git
```

### 必要パッケージのインストール

```bash
$ pip install selenium python-dotenv
```

その他に足りないものがあれば，随時入れる

### chrome ドライバーのダウンロード

以下のリンクから，自身の chrome のバージョンにあった**chromedriver**をダウンロードする
https://chromedriver.chromium.org/downloads

### ドライバーの保存先

ダウンロードしたドライバーを`./driver`に保存

### ログインに必要な情報を設定

`.env`をカレントディレクトリに作成

そして，以下のようにメールアドレスとパスワードを設定する

```txt:./.env
EMAIL = "example@gmail.com"
PASSWORD = "password"
```

## 実行

### プログラムの実行

```bash
$ python pairs.py
```

### 足跡つける人数を聞かれるので数字を入力

```bash
何人に足跡つけますか？ 数字を入力してください > 10
```
