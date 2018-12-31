import pandas as pd
import re
import time


class TestParser:
    df = pd.DataFrame(columns=['ids', 'values'])
    filePath = ""

    def __init__(self, filePath):
        self.filePath = filePath

    def parseFile(self):
        with open(self.filePath, 'rb') as f:

            for line in f:
                decodedLine = line.decode('utf_8', 'ignore').strip()[4:]
                ids = re.findall(r'(.{4}000.)', decodedLine)
                values = re.split(r'.{4}000.{2}', decodedLine)[1:]
                self.appendDf(ids, values)

            self.cleanDf()

    def appendDf(self, ids, values):
        lineDf = pd.DataFrame(data=[ids, values]).T
        lineDf.columns = ['ids', 'values']
        self.df = pd.merge(self.df, lineDf, on=['ids'], how='outer')

    def fromEpochToDate(self, epoch):
        if pd.isnull(epoch): return '-'
        else: return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))

    def cleanDf(self):
        self.df = self.df.dropna(axis=1, how='all')
        del self.df['ids']
        self.df.columns = ['first_name', 'last_name', 'phone', 'date']
        self.df['date'] = self.df['date'].astype(float).apply(self.fromEpochToDate)



a = '/ex_v7'
parser = TestParser(a)
parser.parseFile()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(parser.df)
# print(parser.df.value)
