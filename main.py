import pandas as pd
import re
import time


class TestParser:
    df = pd.DataFrame(columns=['ids', 'values'])
    filePath = ""

    def __init__(self, filePath):
        self.filePath = filePath

    def parse_file(self):
        with open(self.filePath, 'rb') as f:

            for line in f:
                decodedLine = line.decode('utf_8', 'ignore').replace('\xa0', " ").strip()[4:]
                ids = re.findall(r'(.{4}000.)', decodedLine)
                values = re.split(r'.{4}000.{2}', decodedLine)[1:]
                lineDf = pd.DataFrame(data=[ids, values]).T
                lineDf.columns = ['ids', 'values']
                self.df = pd.merge(self.df, lineDf, on=['ids'], how='outer')
            # contents = f.readline().decode('utf_8', 'ignore')
            # for line in contents:
            #     print ('line: ' + line)
            #


def fromEpochToDate(epoch):
    if pd.isnull(epoch): return '-'
    else: return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))

a = '/Users/shlomokoppel/Downloads/ex_v7'
parser = TestParser(a)
parser.parse_file()
parser.df = parser.df.dropna(axis=1, how='all')
del parser.df['ids']
parser.df.columns = ['first_name','last_name','phone','date']
parser.df['date'] = parser.df['date'].astype(float).apply(fromEpochToDate)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(parser.df)
# print(parser.df.value)
