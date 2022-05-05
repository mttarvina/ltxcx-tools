import os, re, time
import sqlite3


class Evo2DbExporter:
    def __init__(self):
        print('\n+ *** Running Module: EVO to Database Exporter')
        self.evoPath = None
        self.evoFile = None
        self.categories = []
        self.inheritance = []


    def GetFileName(self, path):
        file = re.findall('[^/]+.evo', path)
        if file:
            return file[0].replace('.evo', '')
        else:
            return None
    

    def ExtractData(self, evoPath):
        self.evoPath = evoPath
        self.evoFile = self.GetFileName(evoPath)

        print('+ Extracting limits from EVO file...')
        with open(f'./dump/{self.evoFile}_dump.txt', 'w') as tf:
            with open(self.evoPath, 'r') as evf:
                for line in evf:
                    if ';' == line.strip():
                        continue
                    if 'evblankline' in line.strip().casefold():
                        continue
                    if 'category' in line.strip().casefold():
                        buf = line.replace('{', '').strip().split()
                        self.categories.append(buf[-1])
                    if 'inherit' in line.strip().casefold():
                        buf = line.replace(';', '').strip().split()
                        pair = (self.categories[-1], buf[-1])
                        self.inheritance.append(pair)
                    tf.write(line.rstrip())
                    tf.write('\n')
        for category in self.categories:
            print(f'+ Found Category: {category}')
        for relation in self.inheritance:
            print(f'+ Found Inhertance: {relation[-1]}-->{relation[0]}')


    def CreateDBTables(self):
        print('Creating Database Tables...')
        for category in self.categories:
            sql = self.CreateTableSQL(tableType='category', tableName=category)
            self.cur.executescript(sql)
        sql = self.CreateTableSQL(tableType='inheritance')
        self.cur.executescript(sql)


    def Export2DB(self, destPath):
        print('+ Exporting to Database...')
        self.db = sqlite3.connect(f'file:{destPath}/{self.evoFile}.db?mode=rwc', timeout=5000, uri=True)
        self.cur = self.db.cursor()
        self.CreateDBTables()

        category, testNum, minSpec, maxSpec, typSpec, valSpec = None, None, None, None, None, None
        with open(f'./dump/{self.evoFile}_dump.txt', 'r') as tf:
            # export limits to database
            for line in tf:
                if 'paramglobals' in line.casefold():
                    break
                if 'category' in line.strip().casefold():
                    category = line.replace('{', '').strip().split()[-1]
                if '=' in line:
                    buf = line.replace(';', '').strip().split('=')
                    testParam = buf[0]
                    testVal = buf[-1]

                    if testParam.startswith('T'):
                        try:
                            x = int(testParam[1:2])
                            testParam = testParam.replace('T', '')
                        except:
                            pass

                    if '.min' in testParam.casefold():
                        testNum = testParam.strip().split('.')[0]
                        minSpec = testVal.strip().replace('"', '')
                        self.AddToLimitsTable(category, testNum, 'Min', minSpec)
                    elif '.max' in testParam.casefold():
                        testNum = testParam.strip().split('.')[0]
                        maxSpec = testVal.strip().replace('"', '')
                        self.AddToLimitsTable(category, testNum, 'Max', maxSpec)
                    elif '.typ' in testParam.casefold():
                        testNum = testParam.strip().split('.')[0]
                        typSpec = testVal.strip().replace('"', '')
                        self.AddToLimitsTable(category, testNum, 'Typ', typSpec)                        
                    else:
                        testNum = testParam.strip()
                        valSpec = testVal.strip().replace('"', '')
                        self.AddToLimitsTable(category, testNum, 'Val', valSpec)
            
            # export inheritance to database
            for item in self.inheritance:
                self.AddToInhertanceTable(item)
        self.cur.close()


    def AddToLimitsTable(self, category, testNum, spec, val):
        print(f'+ Adding T{testNum}-{spec} to {category}')
        self.cur.execute('INSERT OR IGNORE INTO {} (TestNumber) VALUES ( ? )'.format(category), ( testNum, ))
        if spec == 'Min':
            self.cur.execute('UPDATE {} SET Min = "{}" WHERE TestNumber = "{}"'.format(category, val, testNum))
        elif spec == 'Max':
            self.cur.execute('UPDATE {} SET Max = "{}" WHERE TestNumber = "{}"'.format(category, val, testNum))
        elif spec == 'Typ':
            self.cur.execute('UPDATE {} SET Typ = "{}" WHERE TestNumber = "{}"'.format(category, val, testNum))
        elif spec == 'Val':
            self.cur.execute('UPDATE {} SET Value = "{}" WHERE TestNumber = "{}"'.format(category, val, testNum))
        self.db.commit()
    
    
    def AddToInhertanceTable(self, relation):
        print(f'+ Adding {relation[-1]}-->{relation[0]} to Inheritance')
        self.cur.execute('INSERT OR IGNORE INTO INHERITANCE (Category) VALUES ( ? )', ( relation[0], ))
        self.cur.execute('UPDATE INHERITANCE SET Parent = "{}" WHERE Category = "{}"'.format(relation[-1], relation[0]))
        self.db.commit()


    def CreateTableSQL(self, tableType, tableName=None):
        if tableType == 'category':
            sql = '''
                DROP TABLE IF EXISTS {};
                CREATE TABLE {} (
                    id          INTEGER NOT NULL PRIMARY KEY,
                    TestNumber  TEXT UNIQUE,
                    TestName    TEXT,
                    Value       TEXT,
                    Min         TEXT,
                    Typ         TEXT,
                    Max         TEXT
                );
            '''.format(tableName, tableName)
        
        elif tableType == 'inheritance':
            sql = '''
                DROP TABLE IF EXISTS INHERITANCE;
                CREATE TABLE INHERITANCE (
                    id          INTEGER NOT NULL PRIMARY KEY,
                    Category    TEXT,
                    Parent      TEXT
                );
            '''
        return sql


if __name__ == '__main__':
    evoPath = './reference/VK76_limits.evo'
    dbPath = './limits_db'

    evo2db = Evo2DbExporter()

    stamp = time.perf_counter()
    evo2db.ExtractData(evoPath)
    evo2db.Export2DB(dbPath)
    stamp = time.perf_counter() - stamp
    print(f'+ Elapsed Time: {stamp} seconds')
