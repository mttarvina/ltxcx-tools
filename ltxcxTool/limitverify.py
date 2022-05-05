import pandas as pd
import csv


refPath = './reference/Char_VK78A-0B_MAX20810_VK78A-0B_MAX20810_STD_LF_5Temps_2022042919828.csv'
refFile = refPath.replace('.csv', '')

refDF = pd.read_csv(refPath, sep=',', header=13, index_col='Test #')
refColumns = ['Test #', 'Test Name', 'Temp', 'Unit', 'EC/QA Low Limit (Override)', 'EC/QA High Limit (Override)']
for column in list(refDF.columns.values):
    if column not in refColumns:
        del refDF[column]

lg32C = refDF[refDF['Temp'] == 32]
# lg125C = refDF[refDF['Temp'] == 125]
# lgN40C = refDF[refDF['Temp'] == -40]


dlogPath = './limits_csv/VK78ABAtp01FTCHAR_SS_eng05_limits.csv'
dlogFile = dlogPath.replace('.csv', '')
outputPath = f'{dlogFile}_LG_verified.csv'

dlogDF = pd.read_csv(dlogPath, sep=',', header=14, index_col='Test#')
# print(dlogDF)
# print(dlogDF.loc[1001010])
# print(list(dlogDF.index.values))

lgDF = lg32C


with open(outputPath, 'w', newline='') as csvf:
    encoder = csv.writer(csvf)
    encoder.writerow(['Test#', 'DlogMin', 'DlogUnit', 'LGMin', 'LGUnit', 'CompareMin', '', 'DlogMax', 'DlogUnit', 'LGMax', 'LGUnit', 'CompareMax'])

    for testItem in list(dlogDF.index.values):
        dlogMin = dlogDF.at[testItem, 'Minimum']
        dlogUnit = dlogDF.at[testItem, 'Unit']
        dlogMax = dlogDF.at[testItem, 'Maximum']
        # dlogmaxUnit = dlogDF.at[testItem, 'Unit.1']
        try:
            lgMin = lgDF.at[testItem, 'EC/QA Low Limit (Override)']
            lgUnit = lgDF.at[testItem, 'Unit']
            lgMax = lgDF.at[testItem, 'EC/QA High Limit (Override)']
        except:
            lgMin = 0.0
            lgUnit = ''
            lgMax = 0.0
        
        # if testItem == 1002080:
        #     buf1 = lgMin - dlogMin
        #     buf2 = lgMax - dlogMax
        #     print(f'dlogMin: {dlogMin}, dlogUnit: {dlogUnit} ;;; lgMin: {lgMin}, lgUnit: {lgUnit} ;;; {buf1}')
        #     print(f'dlogMax: {dlogMax}, dlogUnit: {dlogUnit} ;;; lgMax: {lgMax}, lgUnit: {lgUnit} ;;; {buf2}')

        if (    ((-10e-3 < lgMin-dlogMin < 10e-3) and \
                (   str(dlogUnit).casefold() == str(lgUnit).casefold() or \
                    (dlogUnit == 'none' and lgUnit == 'one') or \
                    pd.isna(lgUnit)
                )) or \
                pd.isna(dlogMin) or \
                pd.isna(lgMin) \
            ):
            compareMin = ''
        else:
            compareMin = 'X'
        
        if (    ((-10e-3 < lgMax-dlogMax < 10e-3) and \
                (   str(dlogUnit).casefold() == str(lgUnit).casefold() or \
                    (dlogUnit == 'none' and lgUnit == 'one') or \
                    pd.isna(lgUnit)
                )) or \
                pd.isna(dlogMax) or \
                pd.isna(lgMax) \
            ):
            compareMax = ''
        else:
            compareMax = 'X'
        
        encoder.writerow([testItem, dlogMin, dlogUnit, lgMin, lgUnit, compareMin, '', dlogMax, dlogUnit, lgMax, lgUnit, compareMax])