# fetch_coordinates_tool

ChromeでGoogle Mapsにアクセスして住所から座標を取得するツール<br>
主な用途は以下の２つ<br>
1. csvファイルの住所一覧を読み込み、csvファイルに座標一覧を出力
2. 座標の妥当性チェックのGoogleMaps上の目視確認のための画面遷移の自動化
<br>

用途1のイメージ<br>

`ツールが読み取る住所一覧のcsv`<br>
<img src="samples/sample_address_csv.png" width="200px" alt="住所一覧" title="address_list">

`ツールが出力する座標一覧のcsv`<br>
<img src="samples/sample_coord_csv.png" width="200px" alt="座標一覧" title="coord_list">

## 要件
- ChromeDriver https://sites.google.com/a/chromium.org/chromedriver/downloads<br>
  ※macであればbrew install chromedriverなどで可能と思われる
- python3系
- requirements.txtで定義されたpythonモジュール<br>
    `$ pip(またはpip3) install -t requirements.txt`

## 準備
1. 住所一覧のcsvファイルを準備
　※csvの列タイトル(先頭行)は「Add1」であること。

2. fetch_coord_by_chrome.pyのグローバル変数を必要であれば修正
    - DRIVER_PATH:  実行環境のGoogle Chomeドライバーの絶対パス<br>
        e.g "c:/driver/chromedriver.exe"

    - CSV_ENCODING:<br>
    住所一覧csvファイルの文字のエンコーディング<br>
    　スプレッドシートからコピペの場合、デフォルトのNoneで基本問題なし<br>
    　スプレッドシートからcsv形式を指定してダウングレードした場合、<br>
    　"utf-8_sig" を指定する(※BOM付きのエンコーディング)<br>

    - VISUAL_CHECK:<br>
    座標のブラウザの目視確認をする場合True<br>
    　Chromeが自動起動し、BATCH_SIZEで指定したタブ数までGoogle Mapsを起動し住所検索まで実施される<br>
    　ASYNC_LIMITは常にFalse扱いとなる

    - BATCH_SIZE:<br>
    VISUAL_CHECKがTrueの時、ブラウザタブの数<br>
    　自動処理はタブ数がBATCH_SIZEに達すると待ち受けに入る<br>
    　目視確認済みのタブを削除すると、またBATCH_SIZEまで処理が進む<br>

    - ASYNC_LIMIT:<br>
    並行処理の最大数<br>
    　デフォルトでは実行環境のCPUコア数 - 1<br>
    　※スレッドセーフな処理を保証するため、ASYNC_LIMITの数だけドライバープロセスが起動される

    - MAX_ADDRESS:<br>
    csvファイルから読み込み込んだ住所一覧で先頭から座標対象とする数<br>
    　※処理の実行には時間がかかることが想定される。 (例) 並行数5、住所50件 約200秒<br>
    　一覧全てとする場合はMAX_ADDRESS = Noneとする<br>
    　MAX_ADDRESSでは絞るのではなく、csvファイルの一覧数を絞ってもよい。<br>

## 実行
    1. 実行環境のターミナルを開く e.g Windowsならコマンドプロンプトなど

    2. コマンドを引数に住所一覧csvファイルのパスを指定して実行
        (例) `$ python3 .\fetch_coord_by_chrome.py 住所一覧のcsvファイルのパス`

    3. ブラウザの確認  ※目視確認(VISUAL_CHECK=True)の場合
        自動でGoogle Maps上で住所検索されたポイントが問題ないか確認
        問題なければ、該当のブラウザタブを閉じる(Ctrl + wやタブの閉じるボタン)
        タブはBATCH_SIZEまで自動起動され、既存のタブが閉じられるまで待ち受けとなる

    4. 座標一覧のファイルが住所一覧csvファイルと同じパスで以下のフォーマットで出力される
        (例) 住所一覧csvファイル_yyyyMMddhhmmss.py

## 注意点
    1. 数件座標の取得に失敗する場合がある
        ※特に並行数をCPUコア数に対してオーバーコミットした場合など
    2. 実行環境の性能に合わない、並行数を指定した場合など、処理が停止する場合がある。
    　 その場合、Chromeプロセスが正常終了されずに残る可能性があるので、
    　 タスクマネージャ、アクティビティモニタなどから終了させること。
    3. 2020/08/09現在でとりあえず動作する実装に留まる。