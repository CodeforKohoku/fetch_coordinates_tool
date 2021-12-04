
def deco_run(fn):

    def wrapper(cls):
        try:
            return fn(cls)

        except Exception as e:
            print(e)

        finally:
            print('closing opened browser processes...')
            del cls.driver

    return wrapper


def deco_fetch_address_list(fn):

    def wrapper(cls):
        fpath = cls.args.addfile

        try:
            return fn(cls)

        except UnicodeDecodeError as e:
            print(e)
            raise Exception('ファイルの文字コードを正しく読めません。' + fpath)

        except Exception as e:
            print(e)
            raise Exception('ファイルを正しく読み込めません。' + fpath)

        raise Exception('アドレス列(Add1)が見つかりません。 ' + fpath)

    return wrapper


def deco_gen_output(fn):

    def wrapper(cls):
        fpath = cls.gen_output_path()

        try:
            return fn(cls, fpath)

        except Exception as e:
            print(e)
            raise Exception('結果ファイルの書き出しに失敗しました。' + fpath)

    return wrapper
