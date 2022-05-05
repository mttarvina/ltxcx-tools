import re, csv, time


class LimitExtractor:
    def __init__(self, srcFile, destPath):
        print('+ *** Running Module: TXT to CSV Limit Extractor...')
        self.srcFile = srcFile
        self.destPath = destPath


    def ExtractLimits(self, dump):
        self.progInfo = self.GetProgramInfo()
        if dump:
            self.destPath = './dump'
            csvName = self.progInfo["ProgramName"] + '_limits_dump.csv'
        else:
            csvName = self.progInfo["ProgramName"] + '_limits.csv'
         
        with open(f'{self.destPath}/{csvName}', 'w', newline='') as csvf:
            csvEncoder = csv.writer(csvf)

            for key in self.progInfo:
                csvEncoder.writerow(['Info', key, self.progInfo[key]])
            csvEncoder.writerow([None, None, None])
            csvEncoder.writerow([None, None, None])

            with open(self.srcFile, 'r') as tf:
                for line in tf:
                    if 'test no.' in line.casefold():
                        break
                csvEncoder.writerow(['Test#', 'Minimum', 'Unit', 'Maximum', 'Unit', 'Test Description'])
                line = next(tf)
                buf = line.strip().split()
                testNumLen = len(buf[0])                                       # count how many '-' are there in the Test No. column
                minSpecLen = len(buf[1])                                       # count how many '-' are there in the Minimum column
                maxSpecLen = len(buf[2])                                       # count how many '-' are there in the Maximum column
                testLabelLen = len(buf[-1])

                testCount = 0
                while True:
                    line = next(tf)                                       # go to next line
                    if line == '\n' or  ('device results' in line.casefold()):
                        break
                    
                    # --- look for strings within specific locations in the line
                    testNum = re.findall('[^ ]+', line[1:1+testNumLen])
                    minSpec = re.findall('[^ ]+', line[testNumLen+2 : testNumLen+2+minSpecLen])
                    maxSpec = re.findall('[^ ]+', line[testNumLen+minSpecLen+3 : testNumLen+minSpecLen+3+maxSpecLen])
                    testLabel = line.strip().split()[-1]

                    # --- if no strings found, make sure these string sets are not empty
                    if not testNum:
                        testNum = ['', ]
                    if not minSpec:
                        minSpec = ['', '']
                    if not maxSpec:
                        maxSpec = ['', '']
                    if not testLabel:
                        testlabel = ''

                    # --- if spec value has a unit, combine the two into one string
                    if len(minSpec) > 1:
                        # minSpec[0] = minSpec[0] + ' ' + minSpec[1]
                        # minSpec[0] = minSpec[0] + minSpec[1]
                        minSpec[0] = minSpec[0].replace('.000', '')
                    else:
                        minSpec.append('')
                    
                    if len(maxSpec) > 1:
                        # maxSpec[0] = maxSpec[0] + ' ' + maxSpec[1]
                        # maxSpec[0] = maxSpec[0] + maxSpec[1]
                        maxSpec[0] = maxSpec[0].replace('.000', '')
                    else:
                        maxSpec.append('')

                    print(f'+ Writing to CSV:\tTest#{testNum[0]}, Min = {minSpec[0]} {minSpec[1]}, Max = {maxSpec[0]} {maxSpec[1]}, {testLabel}')
                    csvEncoder.writerow([testNum[0], minSpec[0], minSpec[1], maxSpec[0], maxSpec[1], testLabel])
                    testCount = testCount + 1
                print(f'+ Found {testCount} test items')
            
        

    def GetProgramInfo(self):
        print('+ Extracting program info from datalog...')
        info = {}
        with open(self.srcFile, 'r') as tf:
            for line in tf:
                if 'test no.' in line.casefold():
                    break
                if 'program name' in line.casefold():
                    info["ProgramName"] = line.strip().split(':')[-1].strip()
                elif 'start time' in line.casefold():
                    info["TimeStamp"] = ' '.join(line.strip().split()[2:])
                elif 'device' in line.casefold():
                    info["Device"] = line.strip().split(':')[-1].strip()
                elif 'sublot id' in line.casefold():
                    info["SubLotID"] = line.strip().split(':')[-1].strip()
                elif 'lot id' in line.casefold():
                    info["LotID"] = line.strip().split(':')[-1].strip()
                elif 'tester node' in line.casefold():
                    info["TesterName"] = line.strip().split(':')[-1].strip()
                elif 'tester type' in line.casefold():
                    info["TesterType"] = line.strip().split(':')[-1].strip()
                elif 'operator' in line.casefold():
                    info["Operator"] = line.strip().split(':')[-1].strip()
                elif 'envision' in line.casefold():
                    info["Envision"] = line.strip().split(':')[-1].strip()
                elif 'fab id' in line.casefold():
                    info["FabID"] = line.strip().split(':')[-1].strip()
                elif 'active flow' in line.casefold():
                    info["Flow"] = line.strip().split(':')[-1].strip()
                elif 'adapter board' in line.casefold():
                    info["AdapterBoard"] = line.strip().split(':')[-1].strip()
        print('+ Found program details:')
        for key in info:
            print(f'+ - {key}: {info[key]}')
        return info


if __name__ == "__main__":
    src = './reference/VK78ABAtp01FTCHAR_SS_eng05_LIMIT_VERIFY___20220503145454.txt'
    dest = './limits_csv'
    stamp = time.perf_counter()
    extractor = LimitExtractor(src, dest)
    extractor.ExtractLimits(dump=False)
    stamp = time.perf_counter() - stamp
    print(f'+ Time Elapsed: {stamp} seconds')