import re
import pandas as pd


class LG2EVOExporter:
    def __init__(self, csvPath) -> None:
        self.csvPath = csvPath
        self.columnList =   [   'Test #',
                                'Test Name',
                                'Temp',
                                'Unit',
                                'EC/QA Low Limit (Override)',
                                'EC/QA High Limit (Override)',
                                'FT Min',
                                'FT Max'
                            ]
        self.fileName = re.findall('[^/]+.csv', self.csvPath)[0].replace('.csv', '')
        self.srcDF = None
        self.roomDF = None
        self.hotDF = None
        self.coldDF = None       


    def ExtractDataFrames(self):
        self.srcDF = pd.read_csv(self.csvPath, sep=',', header=13)
        for column in list(self.srcDF.columns.values):
            if column not in self.columnList:
                del self.srcDF[column]
        print(self.srcDF)

        # extract limits at ROOM
        try:
            self.roomDF = self.srcDF[self.srcDF['Temp'] == 32]
        except:
            try: 
                self.roomDF = self.srcDF[self.srcDF['Temp'] == 25]
            except:
                self.roomDF = None

        # extract limits at HOT
        try: 
            self.hotDF = self.srcDF[self.srcDF['Temp'] == 125]
        except:
            self.hotDF = None

        # extract limits at COLD
        try: 
            self.coldDF = self.srcDF[self.srcDF['Temp'] == -40]
        except:
            self.coldDF = None


    def WriteToEVO(self, category):
        if 'room' in category.casefold():
            catDF = self.roomDF
        elif 'hot' in category.casefold():
            catDF = self.hotDF
        elif 'cold' in category.casefold():
            catDF = self.coldDF

        with open(f'./limits_evo/{self.fileName}.evo', 'a') as evf:
            line = f'\tCategory {category} ' + '{\n'
            evf.write(line)

            count = 0
            skippedItems = []
            for row in range(catDF.shape[0]):
                count+=1
                testNum = catDF.iloc[row]["Test #"]
                specUnit = catDF.iloc[row]["Unit"]

                if 'ft' in category.casefold():
                    specMin = catDF.iloc[row]["FT Min"]
                    specMax = catDF.iloc[row]["FT Max"]
                elif 'qa' in category.casefold():
                    specMin = catDF.iloc[row]["EC/QA Low Limit (Override)"]
                    specMax = catDF.iloc[row]["EC/QA High Limit (Override)"]
                

                if specUnit == 'none' or specUnit == 'code' or specUnit == 'V/us' or specUnit == 'Cel' or specUnit == 'one' or pd.isna(specUnit):
                    specUnit = ''
                if 'khz' in specUnit.casefold():
                    specUnit = 'KHz'
                if (specMax >= 3.0E+20) or (specMin < -3.0E+20) or pd.isna(specMax) or pd.isna(specMin):
                    skippedItems.append(testNum)
                    continue

                line = f'\t\tT{testNum}.Min = "{specMin}{specUnit}";\n\t\tT{testNum}.Max = "{specMax}{specUnit}";\n'
                evf.write(line)

            evf.write('\t}\n')
            print(f'\nFound {count} test items in Category: {category}')
            print('Skipped the following test items:')
            for item in skippedItems:
                print(f'\t - {item}')



if __name__ == "__main__":
    filePath = './reference/Char_VK78A-0B_MAX20810_VK78A-0B_MAX20810_STD_LF_5Temps_2022042919828.csv'
    app = LG2EVOExporter(filePath)
    app.ExtractDataFrames()
    app.WriteToEVO('FT_ROOM')
    app.WriteToEVO('FT_HOT')
    app.WriteToEVO('FT_COLD')
    app.WriteToEVO('QA_ROOM')
    app.WriteToEVO('QA_HOT')
    app.WriteToEVO('QA_COLD')
