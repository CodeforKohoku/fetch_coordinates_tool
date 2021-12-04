import argparse
import warnings
warnings.filterwarnings('ignore')
from lib.coordinator import Coordinator


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b', '--browser',
        help='web browser: chrome',
        default='chrome'
    )
    parser.add_argument(
        '-a', '--addfile',
        help='file path to a csv file of addresses',
        required=True
    )
    return parser.parse_args()


if __name__=='__main__':
    try:
        Coordinator(args()).run()

    except KeyboardInterrupt:
        print('Exited by Ctrl + C')
