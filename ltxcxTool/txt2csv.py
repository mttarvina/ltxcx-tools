import os, re


def get_program_details(txt_path):
    tf = open(txt_path, 'r')
    info = {}
    for line in tf:
        if 'Program Name:' in line:
            strList = line.strip().split()
            info['Program Name'] = strList[2]
        elif 'Start Time:' in line:
            strList = line.strip().split()
            info['Timestamp'] = strList[2]
        elif 'Device Name:' in line:
            strList = line.strip().split()
            info['Device Name'] = strList[2]
        elif 'Lot ID:' in line:
            strList = line.strip().split()
            info['Lot ID'] = strList[2]
        elif 'Sublot ID:' in line:
            strList = line.strip().split()
            info['Sublot ID'] = strList[2]
        elif 'Tester Node Name:' in line:
            strList = line.strip().split()
            info['Tester'] = strList[2]
        elif 'Operator ID:' in line:
            strList = line.strip().split()
            info['Operator ID'] = strList[2]
        elif 'Active Flow:' in line:
            strList = line.strip().split()
            info['Active Flow'] = strList[2]
        elif 'Adapter Board:' in line:
            strList = line.strip().split()
            info['Adapter Board'] = strList[3]
        elif 'Test No.' in line:
            break
    tf.close()
    return info




def write_to_csv(src_path, tp_info):

    dir_files = os.listdir(path='./out_csv')
    if '{}_limits.csv'.format(_tpInfo['Program Name']) in _dirFiles:
        os.remove('./limits_csv/{}_limits.csv'.format(_tpInfo['Program Name']))
        if _displayPrompt:
            print('++ --> Removing existing file of the same name in limits_csv')

    try:
        _csvHandler = open('./limits_csv/{}_limits.csv'.format(_tpInfo['Program Name']), 'w', newline='')
        _csvEncode = csv.writer(_csvHandler)
        try:
            _srcHandler = open(_srcPath, 'r')
            _tStart = time.perf_counter()

            if _displayPrompt:
                print('++ --> Writing program info to CSV')
            for _key in _tpInfo:
                _csvEncode.writerow(['Info', _key, _tpInfo[_key]])
            _csvEncode.writerow([None, None, None])
            _csvEncode.writerow([None, None, None])

            for _line in _srcHandler:
                if 'Test No.' in _line:
                    _strBuf = _line.strip().split()                             # _strBuf = ['Test', 'No.', 'Minimum', 'Maximum', ...] 
                    break
            
            if _displayPrompt:
                print('++ --> Writing column titles to CSV: {}, {}, {}, {}'.format(_strBuf[0] + _strBuf[1], _strBuf[2], _strBuf[3], _strBuf[-1]))
            _csvEncode.writerow([_strBuf[0] + ' ' + _strBuf[1], _strBuf[2], _strBuf[3], _strBuf[-1]])

            _line = next(_srcHandler)
            _strBuf = _line.strip().split()
            _testNumLen = len(_strBuf[0])                                       # count how many '-' are there in the Test No. column
            _minSpecLen = len(_strBuf[1])                                       # count how many '-' are there in the Minimum column
            _maxSpecLen = len(_strBuf[2])                                       # count how many '-' are there in the Maximum column

            _testCount = 0
            while True:
                _line = next(_srcHandler)                                       # go to next line
                if _line == '\n' or  ('Device Results' in _line):
                    break
                
                # --- look for strings within specific locations in the line
                _testLabel = _line.strip().split()[-1]
                _testNum = re.findall('[^ ]+', _line[1:1+_testNumLen])
                _minSpec = re.findall('[^ ]+', _line[_testNumLen+2:_testNumLen+2+_minSpecLen])
                _maxSpec = re.findall('[^ ]+', _line[_testNumLen+_minSpecLen+3:_testNumLen+_minSpecLen+3+_maxSpecLen])

                # --- if no strings found, make sure these string sets are not empty
                if not _testNum:
                    _testNum.append('')
                if not _minSpec:
                    _minSpec.append('')
                if not _maxSpec:
                    _maxSpec.append('')

                # --- if spec value has a unit, combine the two into one string
                if len(_minSpec) > 1:
                    _minSpec[0] = _minSpec[0] + _minSpec[1]
                if len(_maxSpec) > 1:
                    _maxSpec[0] = _maxSpec[0] + _maxSpec[1]

                if _displayPrompt:
                    print('++ --> Writing to CSV:\t\tTest Num = {:<15} Min = {:<15} Max = {:<15}\t{}'.format(_testNum[0], _minSpec[0], _maxSpec[0], _testLabel))
                _csvEncode.writerow([_testNum[0], _minSpec[0], _maxSpec[0], _testLabel])
                _testCount = _testCount + 1

            print('++ --> CSV write execution finished after: {:.4f} seconds'.format(time.perf_counter() - _tStart))
            print('++ --> Found {} test items'.format(_testCount))
            _srcHandler.close()
            _csvHandler.close()          
            _flag = True
        except:
            _flag = False
    except:
        _flag = False
    return _flag





def extract_limits(txt_path):
    # extract file name
    file_name = re.findall('[^/]+.txt', txt_path)
    print(f'+ File name: {file_name[-1]}')
    program_info = get_program_details(txt_path)