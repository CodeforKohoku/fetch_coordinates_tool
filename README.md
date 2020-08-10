# fetch_coordinates_tool

ChromeでGoogle Mapsにアクセスして住所から座標を取得するツール<br>
主な用途は以下の２つ<br>
1. csvファイルの住所一覧を読み込み、csvファイルに座標一覧を出力
2. 座標に間違いがないか、GoogleMaps上の目視確認で画面遷移の自動化
<br>

## 要件
- ChromeDriver https://sites.google.com/a/chromium.org/chromedriver/downloads<br>
  ※macであればbrew install chromedriverなどで可能と思われる
- python3系
- requirements.txtで定義されたpythonモジュール<br>
    `$ pip(またはpip3) install -t requirements.txt`

## 準備
1. 住所一覧のcsvファイルを準備
　※csvの列タイトル(先頭行)は「Add1」であること。

2. fetch_coord_by_chrome.pyのグローバル変数を実行環境に合わせて修正
    - DRIVER_PATH:  実行環境のGoogle Chomeドライバーの絶対パス<br>
        e.g "c:/driver/chromedriver.exe"

    - ASYNC_LIMIT:  並行処理の最大数<br>
        デフォルトでは実行環境のCPUコア数 - 1<br>
        ※スレッドセーフな処理を保証するため、ASYNC_LIMITの数だけドライバープロセスが起動される

    - MAX_ADDRESS:  csvファイルから読み込み込んだ住所一覧で先頭から座標対象とする数<br>
        ※処理の実行には時間がかかることが想定される。 e.g 並行数5、住所50件 約200秒<br>
        　一覧全てとする場合はMAX_ADDRESS = Noneとする<br>
        　MAX_ADDRESSでは絞るのではなく、csvファイルの一覧数を絞ってもよい。<br>

## 実行
1. 実行環境のターミナルを開く e.g Windowsならコマンドプロンプトなど
2. コマンドを引数に住所一覧csvファイルのパスを指定して実行<br>
    e.g `$ python3 .\fetch_coord_by_chrome.py 住所一覧のcsvファイルのパス`
3. 座標一覧のファイルが住所一覧csvファイルと同じパスで以下のフォーマットで出力される<br>
    住所一覧csvファイル_yyyyMMddhhmmss.py

## 注意点
1. 数件座標の取得に(高確率で)失敗する場合がある
2. 実行環境の性能に合わない、並行数を指定した場合など、処理が停止する場合がある。<br>
　 その場合、Chromeプロセスが正常終了されずに残る可能性があるので、<br>
　 タスクマネージャ、アクティビティモニタなどから終了させること。<br>
3. 2020/08/09現在でとりあえず動作する実装に留まる。