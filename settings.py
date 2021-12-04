from multiprocessing import cpu_count

# ツールを実行する環境(PC)のGoogle Chromeドライバーのフォルダパスを指定してください。
# ドライバーがない場合は、以下よりダウンロードして、配置したパスを指定ください。
#   https://chromedriver.chromium.org/downloads
CHROME_DRIVER_PATH = "c:/driver/chromedriver.exe"

# 住所一覧のCSVファイルの上から順に処理する最大の住所数を指定します。
# 無制限とする場合は、以下のように指定してください。
# ※無制限とすることは非推奨です。
#   住所数によっては長時間要することが予想され、
#   実行時のモードによってはキャンセル処理が困難な場合があります。
MAX_ADDR_NUM = 2

# 住所一覧が記載されたCSVファイルの文字コードを指定してください。
#  ※以下、Windows環境の場合
#
#  住所のCSVファイルをエクセルで開いて日本語が文字化けしない場合、
#  以下のように指定してください。(Noneの場合デフォルトの文字コードcp932の想定です)
#   CSV_ENCODING = None
#
#  GoogleスプレッドシートからCSV形式でダウンロードしたファイルを
#  エクセルで開くと日本語が文字化けすることが想定されます。
#  この場合は以下のように指定してください。
#   CSV_ENCODING = "utf-8_sig"
CSV_ENCODING = "utf-8_sig"

# Webブラウザ上のマップで住所の座標を目視で確認する場合にTrueを指定してください。
# 座標を取得してCSVファイルを生成するだけであれば、Falseを指定してください。
# Falseの場合、ツールの実行時にWebブラウザはデスクトップ上に表示されません。
VISUAL_CHECK = False

# VISUAL_CHECK = Trueの場合にWebブラウザのタブ数の上限値をしていします。
# 指定した上限値まで自動でタブを開き、各タブごとに１つの住所をマップ表示します。
# 上限数に達すると、タブを削除するまで次の住所の処理は待ち受けとなります。
# 指定できる値は1から10までです。
MAX_TAB_NUM = 3


''' 以降は基本的に変更する必要がありません。  '''

# 日本語版Google MapsのURL
MAP_URL = "https://www.google.co.jp/maps/?hl=ja"

# 住所取得の処理を非同期で並列実行するか指定します。
# VISUAL_CHECK = Trueの場合は、ここで指定する値はFalseに上書きされます。
ASYNC_MODE = True

# ASYNC_MODE = Trueの場合の最大並列数を指定します。
# ASYNC_LIMIT = cpu_count() - 1の場合、環境のCPUコア数を考慮した数が設定されます。
ASYNC_LIMIT = cpu_count() - 1


''' 以降は変更しないでください。  '''


if MAX_ADDR_NUM is None:
    pass
elif isinstance(MAX_ADDR_NUM, int) and MAX_ADDR_NUM > 1:
    pass
else:
    print(
f"""\nMAX_ADDR_NUMの値が正しくありません。
任意の自然数あるいはNoneを指定してください。
""")
    exit(1)


if isinstance(MAX_TAB_NUM, int) and 0 < MAX_TAB_NUM and MAX_TAB_NUM < 11:
    pass
else:
    print(
f"""\nMAX_TAB_NUMの値が正しくありません。
1以上10以下の任意の自然数を指定してください。
""")
    exit(1)

