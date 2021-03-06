# coding=utf-8
# © 2021, 2022 Greg Ritacco

from psEntities import PatternScriptEntities
from PatternTracksSubroutine import Model
from PatternTracksSubroutine import View

SCRIPT_NAME = 'OperationsPatternScripts.PatternTracksSubroutine.Controller'
SCRIPT_REV = 20220101

class LocationComboBox(PatternScriptEntities.JAVA_AWT.event.ActionListener):
    """Event triggered from location combobox selection"""

    def __init__(self, subroutineFrame):

        self.subroutineFrame = subroutineFrame

    def actionPerformed(self, EVENT):

        Model.updatePatternLocation(EVENT.getSource().getSelectedItem())
        subroutinePanel = StartUp(self.subroutineFrame).makeSubroutinePanel()
        self.subroutineFrame.removeAll()
        self.subroutineFrame.add(subroutinePanel)
        self.subroutineFrame.revalidate()

        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return

class StartUp:
    """Start the pattern tracks subroutine"""

    def __init__(self, subroutineFrame=None):

        self.psLog = PatternScriptEntities.LOGGING.getLogger('PS.PT.Controller')
        self.subroutineFrame = subroutineFrame

        return

    def makeSubroutineFrame(self):
        """Makes the title border frame"""

        self.subroutineFrame = View.ManageGui().makeSubroutineFrame()
        subroutinePanel = self.makeSubroutinePanel()
        self.subroutineFrame.add(subroutinePanel)

        self.psLog.info('pattern tracks makeFrame completed')

        return self.subroutineFrame

    def makeSubroutinePanel(self):
        """Makes the control panel that sits inside the frame"""

        if not PatternScriptEntities.readConfigFile('PT')['AL']:
            Model.updateLocations()

        self.subroutinePanel, self.widgets = View.ManageGui().makeSubroutinePanel()
        self.activateWidgets()

        return self.subroutinePanel

    def activateWidgets(self):

        self.widgets[0].addActionListener(LocationComboBox(self.subroutineFrame))
        self.widgets[1].actionPerformed = self.yardTrackOnlyCheckBox
        self.widgets[4].actionPerformed = self.patternButton
        self.widgets[5].actionPerformed = self.setCarsButton

        return

    def yardTrackOnlyCheckBox(self, EVENT):

        if (self.widgets[1].selected):
            trackList = Model.makeTrackList(self.widgets[0].getSelectedItem(), 'Yard')
        else:
            trackList = Model.makeTrackList(self.widgets[0].getSelectedItem(), None)

        configFile = PatternScriptEntities.readConfigFile()
        trackDict = Model.updatePatternTracks(trackList)
        configFile['PT'].update({'PT': trackDict})
        configFile['PT'].update({'PA': self.widgets[1].selected})
        configFile['PT'].update({'PI': self.widgets[2].selected})
        PatternScriptEntities.writeConfigFile(configFile)

        subroutinePanel = StartUp(self.subroutineFrame).makeSubroutinePanel()
        self.subroutineFrame.removeAll()
        self.subroutineFrame.add(subroutinePanel)
        self.subroutineFrame.revalidate()

        return

    def patternButton(self, EVENT):
        """Makes a pattern tracks report based on the config file (PR)"""

        self.psLog.debug('Controller.patternButton')

        Model.updateConfigFile(self.widgets)

        PatternScriptEntities.REPORT_ITEM_WIDTH_MATRIX = PatternScriptEntities.makeReportItemWidthMatrix()

        if not Model.verifySelectedTracks():
            self.psLog.warning('Track not found, re-select the location')
            return

        if not Model.getSelectedTracks():
            self.psLog.warning('No tracks were selected for the pattern button')
            return

        locationDict = Model.makeLocationDict()
        modifiedReport = Model.makeReport(locationDict, 'PR')

        workEventName, textListForPrint = Model.makeWorkEventList(modifiedReport, trackTotals=True)
        workEventPath = PatternScriptEntities.PROFILE_PATH + 'operations\\patternReports\\' + workEventName + '.txt'
        PatternScriptEntities.genericWriteReport(workEventPath, textListForPrint)

        fileToOpen = PatternScriptEntities.JAVA_IO.File(workEventPath)
        if fileToOpen.isFile():
            PatternScriptEntities.genericDisplayReport(fileToOpen)
        else:
            self.psLog.warning('Not found: ' + workEventPath)

        if PatternScriptEntities.JMRI.jmrit.operations.setup.Setup.isGenerateCsvSwitchListEnabled():
            Model.writeCsvSwitchList(modifiedReport)

        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return

    def setCarsButton(self, EVENT):
        """Opens a "Pattern Report for Track X" window for each checked track"""

        self.psLog.debug('Controller.setCarsButton')

        Model.updateConfigFile(self.widgets)

        PatternScriptEntities.REPORT_ITEM_WIDTH_MATRIX = PatternScriptEntities.makeReportItemWidthMatrix()

        if not Model.verifySelectedTracks():
            self.psLog.warning('Track not found, re-select the location')
            return

        Model.onScButtonPress()

        if PatternScriptEntities.readConfigFile('PT')['TI']: # TrainPlayer Include
            Model.resetTrainPlayerSwitchlist()

        print(SCRIPT_NAME + ' ' + str(SCRIPT_REV))

        return
