import argparse
import csv
import re
import time
import settings as C
import lib.utils as utils
from lib.browser import *
from lib.decorator.coordinator import *


__all__ = [
    "Coordinator"
]


class Coordinator:

    def __init__(self, args):
        assert isinstance(args, argparse.Namespace)
        self.args = args

        if args.browser == 'chrome':
            self.driver = ChromeDriver()

        else:
            raise Exception(
                '非対応のWebブラウザが選択されています。: ' + args.browser)


    @deco_run
    def run(self):

        self.driver.run(
            self.fetch_address_list())

        if self.driver.fetched:
            self.gen_output()
        else:
            print('取得した座標はありません。')

        if C.VISUAL_CHECK:
            input('\nブラウザの確認を終える場合は何かしらのキーを押下してください。')



    @deco_fetch_address_list
    def fetch_address_list(self):

        data = csv.reader(
            open(self.args.addfile, encoding=C.CSV_ENCODING)) # file not closed here

        for i, value in enumerate(next(data)):

            if value == 'Add1': # skip empty "" value
                return [row[i] for row in data if row[i]][: C.MAX_ADDR_NUM]


    @deco_gen_output
    def gen_output(self, fpath):
        assert isinstance(fpath, str) # passed by decorator

        w = csv.writer(open(
            fpath, mode='w', encoding="utf-8_sig", newline=""))

        print('< 取得一覧 >')

        for add, (x, y) in self.driver.fetched:
            print(f'{add}:\tx: {x}, y: {y}')
            w.writerow((add, x, y))
        

    def gen_output_path(self): # add tstamp after re.sub because addfile can have no csv
        tstamp = utils.format_unixtime(time.time())
        return re.sub('.csv$', '', self.args.addfile) + f'_{ tstamp }.csv'

