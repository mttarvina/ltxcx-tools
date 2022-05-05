
import sys, json, time
from PyQt5 import QtCore, QtGui, QtWidgets
from ltxcxTool.appgui import Ui_LTXCX_Tool
from ltxcxTool.accuracyTool import CXTester
from ltxcxTool.evo2db import Evo2DbExporter
from ltxcxTool.preset import Preset


class LTXCXApp():
    def __init__(self, MainWindow):
        self.parentGUI = MainWindow
        self.preset = Preset()
        self.tester = CXTester(self.preset.spec)
        self.ui = Ui_LTXCX_Tool()
        self.ui.setupUi(MainWindow)
        self.SetupLogic()

    def SetupLogic(self):

        with open(self.preset.config, 'r') as jf:
            self.config = json.load(jf)
        with open(self.preset.spec, 'r') as jf:
            self.specs = json.load(jf)

        # t0 ::: define global variables
        self.t0Card = None
        self.t0Mode = None
        self.t0FVal = 0.0
        self.t0MVal = 0.0

        # t0 ::: initialize UI object values
        self.ui.t0CardSelect.addItems(self.config["t0"]["resource_card"])
        self.ui.t0Mode.addItems(self.config["t0"]["mode"])
        self.T0ClearResult()
        
        # t0 ::: connect signals
        self.ui.t0CardSelect.activated.connect(self.T0CardChanged)
        self.ui.t0Mode.activated.connect(self.T0ModeChanged)
        self.ui.t0BtnCalc.clicked.connect(self.T0CalcAccuracy)

        # t1 ::: connect signals
        self.ui.t1BtnBrowseFile.clicked.connect(self.T1BrowseFile)

        # t3 ::: connect signals
        self.ui.t3BtnExtractEvoLimits.clicked.connect(self.T3ExportEVO2DB)
        
        self.T0InitializeGuiInputs()


    def T0InitializeGuiInputs(self):
        self.ui.t0Mode.setEnabled(False)
        self.ui.t0LabelMode.setEnabled(False)
        self.ui.t0MRange.setEnabled(False)
        self.ui.t0LabelMrange.setEnabled(False)
        self.ui.t0MVal.setEnabled(False)
        self.ui.t0LabelMval.setEnabled(False)
        self.ui.t0FvoltsAtMamps.setEnabled(False)
        self.ui.t0LabelFvolts.setEnabled(False)
        self.ui.t0FRange.setEnabled(False)
        self.ui.t0LabelFrange.setEnabled(False)
        self.ui.t0FVal.setEnabled(False)
        self.ui.t0LabelFval.setEnabled(False)
        self.ui.t0MvoltsAtFamps.setEnabled(False)
        self.ui.t0LabelMvolts.setEnabled(False)
        self.ui.t0BtnCalc.setEnabled(False)


    def T0DisableInputFields(self):
        self.ui.t0MRange.setEnabled(False)
        self.ui.t0LabelMrange.setEnabled(False)
        self.ui.t0MVal.setEnabled(False)
        self.ui.t0LabelMval.setEnabled(False)
        self.ui.t0FvoltsAtMamps.setEnabled(False)
        self.ui.t0LabelFvolts.setEnabled(False)
        self.ui.t0FRange.setEnabled(False)
        self.ui.t0LabelFrange.setEnabled(False)
        self.ui.t0FVal.setEnabled(False)
        self.ui.t0LabelFval.setEnabled(False)
        self.ui.t0MvoltsAtFamps.setEnabled(False)
        self.ui.t0LabelMvolts.setEnabled(False)
        self.ui.t0BtnCalc.setEnabled(False)


    def T0DisplayError(self, prompt):
        self.ui.t0RangeErr.clear()
        self.ui.t0RPVErr.clear()
        self.ui.t0FMErr.clear()
        self.ui.t0FMVal.setText(f'ERROR: {prompt}')


    def T0ClearResult(self):
        self.ui.t0RangeErr.clear()
        self.ui.t0RPVErr.clear()
        self.ui.t0FMErr.clear()
        self.ui.t0FMVal.clear()


    def T0CardChanged(self):
        self.t0Card = self.ui.t0CardSelect.currentText()
        self.ui.t0Mode.setEnabled(True)
        self.ui.t0LabelMode.setEnabled(True)


    def T0ModeChanged(self):
        self.t0Mode = self.ui.t0Mode.currentText()

        if self.t0Mode == 'Force V':
            self.T0SetupForForceV()
        elif self.t0Mode == 'Force I':
            self.T0SetupForForceI()
        elif self.t0Mode == 'Measure V':
            self.T0SetupForMeasureV()
        elif self.t0Mode == 'Measure I':
            self.T0SetupForMeasureI()
        else:
            self.T0DisableInputFields()


    def T0SetupForForceV(self):
        self.ui.t0MRange.setEnabled(False)
        self.ui.t0LabelMrange.setEnabled(False)
        self.ui.t0MVal.setEnabled(False)
        self.ui.t0LabelMval.setEnabled(False)
        self.ui.t0FvoltsAtMamps.setEnabled(False)
        self.ui.t0LabelFvolts.setEnabled(False)
        self.ui.t0FRange.setEnabled(True)
        self.ui.t0LabelFrange.setEnabled(True)
        self.ui.t0FVal.setEnabled(True)
        self.ui.t0LabelFval.setEnabled(True)
        self.ui.t0MvoltsAtFamps.setEnabled(False)
        self.ui.t0LabelMvolts.setEnabled(False)
        self.ui.t0BtnCalc.setEnabled(True)

        if self.t0Card == 'OVI':
            self.ui.t0FRange.clear()
            self.ui.t0FRange.addItems(self.specs["spec"]["ovi"]["fv"]["range"])
        elif self.t0Card == 'VI16':
            self.ui.t0FRange.clear()
            self.ui.t0FRange.addItems(self.specs["spec"]["vi16"]["fv"]["range"])


    def T0SetupForForceI(self):
        self.ui.t0MRange.setEnabled(False)
        self.ui.t0LabelMrange.setEnabled(False)
        self.ui.t0MVal.setEnabled(False)
        self.ui.t0LabelMval.setEnabled(False)
        self.ui.t0FvoltsAtMamps.setEnabled(False)
        self.ui.t0LabelFvolts.setEnabled(False)
        self.ui.t0FRange.setEnabled(True)
        self.ui.t0LabelFrange.setEnabled(True)
        self.ui.t0FVal.setEnabled(True)
        self.ui.t0LabelFval.setEnabled(True)
        self.ui.t0MvoltsAtFamps.setEnabled(True)
        self.ui.t0LabelMvolts.setEnabled(True)
        self.ui.t0BtnCalc.setEnabled(True)

        if self.t0Card == 'OVI':
            self.ui.t0FRange.clear()
            self.ui.t0FRange.addItems(self.specs["spec"]["ovi"]["fi"]["range"])
        elif self.t0Card == 'VI16':
            self.ui.t0FRange.clear()
            self.ui.t0FRange.addItems(self.specs["spec"]["vi16"]["fi"]["range"])


    def T0SetupForMeasureV(self):
        self.ui.t0MRange.setEnabled(True)
        self.ui.t0LabelMrange.setEnabled(True)
        self.ui.t0MVal.setEnabled(True)
        self.ui.t0LabelMval.setEnabled(True)
        self.ui.t0FvoltsAtMamps.setEnabled(False)
        self.ui.t0LabelFvolts.setEnabled(False)
        self.ui.t0FRange.setEnabled(False)
        self.ui.t0LabelFrange.setEnabled(False)
        self.ui.t0FVal.setEnabled(False)
        self.ui.t0LabelFval.setEnabled(False)
        self.ui.t0MvoltsAtFamps.setEnabled(False)
        self.ui.t0LabelMvolts.setEnabled(False)
        self.ui.t0BtnCalc.setEnabled(True)

        if self.t0Card == 'OVI':
            self.ui.t0MRange.clear()
            self.ui.t0MRange.addItems(self.specs["spec"]["ovi"]["mv"]["range"])
        elif self.t0Card == 'VI16':
            self.ui.t0MRange.clear()
            self.ui.t0MRange.addItems(self.specs["spec"]["vi16"]["mv"]["range"])

    
    def T0SetupForMeasureI(self):
        self.ui.t0MRange.setEnabled(True)
        self.ui.t0LabelMrange.setEnabled(True)
        self.ui.t0MVal.setEnabled(True)
        self.ui.t0LabelMval.setEnabled(True)
        self.ui.t0FvoltsAtMamps.setEnabled(True)
        self.ui.t0LabelFvolts.setEnabled(True)
        self.ui.t0FRange.setEnabled(False)
        self.ui.t0LabelFrange.setEnabled(False)
        self.ui.t0FVal.setEnabled(False)
        self.ui.t0LabelFval.setEnabled(False)
        self.ui.t0MvoltsAtFamps.setEnabled(False)
        self.ui.t0LabelMvolts.setEnabled(False)
        self.ui.t0BtnCalc.setEnabled(True)

        if self.t0Card == 'OVI':
            self.ui.t0MRange.clear()
            self.ui.t0MRange.addItems(self.specs["spec"]["ovi"]["mi"]["range"])
        if self.t0Card == 'VI16':
            self.ui.t0MRange.clear()
            self.ui.t0MRange.addItems(self.specs["spec"]["vi16"]["mi"]["range"])


    def T0CalcAccuracy(self):
        if self.t0Card == 'OVI':
            if self.t0Mode == 'Force V':
                self.ui.consoleLog.insertPlainText('+ T0: Calc OVI force V\n')
                try:
                    forceVal = float(self.ui.t0FVal.text())
                    forceRange = self.ui.t0FRange.currentText()
                    result = self.tester.ovi_calc_force_v(forceVal, forceRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText('')
                        self.ui.t0FMErr.setText(f'{result["voltage_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}')
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError()

            elif self.t0Mode == 'Force I':
                self.ui.consoleLog.insertPlainText('+ T0: Calc OVI force I\n')
                try:
                    forceVal = float(self.ui.t0FVal.text())
                    measuredV = float(self.ui.t0MvoltsAtFamps.text())
                    forceRange = self.ui.t0FRange.currentText()
                    result = self.tester.ovi_calc_force_i(forceVal, measuredV, forceRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText(f'{result["range_pervolt_error"]}')
                        self.ui.t0FMErr.setText(f'{result["current_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}') 
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError()

            elif self.t0Mode == 'Measure V':
                self.ui.consoleLog.insertPlainText('+ T0: Calc OVI measure V\n')
                try:
                    measureVal = float(self.ui.t0MVal.text())
                    measureRange = self.ui.t0MRange.currentText()
                    result = self.tester.ovi_calc_measure_v(measureVal, measureRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText('')
                        self.ui.t0FMErr.setText(f'{result["voltage_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}')
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError()

            elif self.t0Mode == 'Measure I':
                self.ui.consoleLog.insertPlainText('+ T0: Calc OVI measure I\n')
                try:
                    forceVal = float(self.ui.t0MVal.text())
                    forcedV = float(self.ui.t0FvoltsAtMamps.text())
                    forceRange = self.ui.t0MRange.currentText()
                    result = self.tester.ovi_calc_measure_i(forceVal, forcedV, forceRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText(f'{result["range_pervolt_error"]}')
                        self.ui.t0FMErr.setText(f'{result["current_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}') 
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError() 

        elif self.t0Card == 'VI16':
            if self.t0Mode == 'Force V':        # DONE
                self.ui.consoleLog.insertPlainText('+ T0: Calc VI16 force V\n')
                try:
                    forceVal = float(self.ui.t0FVal.text())
                    forceRange = self.ui.t0FRange.currentText()
                    result = self.tester.vi16_calc_force_v(forceVal, forceRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText('')
                        self.ui.t0FMErr.setText(f'{result["voltage_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}')
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError()

            elif self.t0Mode == 'Force I':      # DONE
                self.ui.consoleLog.insertPlainText('+ T0: Calc VI16 force I\n')
                try:
                    forceVal = float(self.ui.t0FVal.text())
                    measuredV = float(self.ui.t0MvoltsAtFamps.text())
                    forceRange = self.ui.t0FRange.currentText()
                    result = self.tester.vi16_calc_force_i(forceVal, measuredV, forceRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText(f'{result["range_pervolt_error"]}')
                        self.ui.t0FMErr.setText(f'{result["current_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}') 
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError()

            elif self.t0Mode == 'Measure V':        # DONE
                self.ui.consoleLog.insertPlainText('+ T0: Calc VI16 measure V\n')
                try:
                    measureVal = float(self.ui.t0MVal.text())
                    measureRange = self.ui.t0MRange.currentText()
                    result = self.tester.vi16_calc_measure_v(measureVal, measureRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText('')
                        self.ui.t0FMErr.setText(f'{result["voltage_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}')
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError()

            elif self.t0Mode == 'Measure I':
                self.ui.consoleLog.insertPlainText('+ T0: Calc VI16 measure I\n')
                try:
                    forceVal = float(self.ui.t0MVal.text())
                    forcedV = float(self.ui.t0FvoltsAtMamps.text())
                    forceRange = self.ui.t0MRange.currentText()
                    result = self.tester.vi16_calc_measure_i(forceVal, forcedV, forceRange)
                    if result:
                        self.ui.t0RangeErr.setText(f'{result["range_error"]}')
                        self.ui.t0RPVErr.setText(f'{result["range_pervolt_error"]}')
                        self.ui.t0FMErr.setText(f'{result["current_error"]}')
                        self.ui.t0FMVal.setText(f'{result["value"]}') 
                    else:
                        self.T0DisplayError()
                except:
                    self.T0DisplayError() 




    def T1BrowseFile(self):
        filePath = self.BrowseFile("Select a datalog text file", "Text (*.txt)")


    def T3ExportEVO2DB(self):
        evoPath = self.BrowseFile("Select an EVO file", "EVO (*.evo)")
        dbPath = self.BrowseFolder('Select where to save database')
        self.T3ToggleButtons(False)
        evo2db = Evo2DbExporter()
        stamp = time.perf_counter()
        evo2db.ExtractData(evoPath)
        evo2db.Export2DB(dbPath)
        stamp = time.perf_counter() - stamp
        print(f'+ Elapsed Time: {stamp} seconds')
        self.T3ToggleButtons(True)


    def T3ToggleButtons(self, state):
        self.ui.t3BtnExtractEvoLimits.setEnabled(state)
        self.ui.t3BtnCreateNew.setEnabled(state)
        self.ui.t3BtnGenerateEvo.setEnabled(state)
        self.ui.t3BtnVerifyLimits.setEnabled(state)


    def BrowseFile(self, prompt, fileFilter):
        file = None
        while (file == None):
            buf = QtWidgets.QFileDialog.getOpenFileNames(self.parentGUI, prompt, "", fileFilter)
            if buf[0]:
                file = buf[0][0]
        return file


    def BrowseFolder(self, prompt):
        folder = None
        while (folder == None):
            folder = QtWidgets.QFileDialog.getExistingDirectory(self.parentGUI, prompt, options=QtWidgets.QFileDialog.ShowDirsOnly)
        return folder


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = LTXCXApp(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())