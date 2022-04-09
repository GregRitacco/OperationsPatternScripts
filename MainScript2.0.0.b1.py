# No restrictions on use
# © 2021 Greg Ritacco

import jmri
from apps import Apps
import java
import java.awt
import java.awt.event
import javax.swing
import logging
import time
from sys import path as sysPath


def useThisVersion():
    '''Keep multiple versions of this plugin sorted out'''

    fileRoot = jmri.util.FileUtil.getPreferencesPath()
    currentFile = str(jmri.util.FileUtil.findFiles('MainScript2.0.0.b1.py', fileRoot).pop())
    currentDir = java.io.File(currentFile).getParent()

    return currentDir

_currentDir = useThisVersion()
sysPath.append(_currentDir)

from psEntities import MainScriptEntities

MainScriptEntities._currentPath = _currentDir
print('Current Pattern Scripts directory: ' + MainScriptEntities._currentPath)


'''Pattern Scripts Version 2.0.0 Pre Release b1'''

scriptName = 'OperationsPatternScripts.MainScript'
scriptRev = 20220101

class Logger():

    def __init__(self):

        logPath = jmri.util.FileUtil.getProfilePath() + 'operations\\buildstatus\\PatternScriptsLog.txt'
        logFileFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.psFileHandler = logging.FileHandler(logPath, mode='w', encoding='utf-8')
        self.psFileHandler.setFormatter(logFileFormat)

        return

    def startLogger(self):

        psLog = logging.getLogger('PS')
        psLog.setLevel(10)
        psLog.addHandler(self.psFileHandler)

        return

    def stopLogger(self):

        psLog = logging.getLogger('PS')
        psLog.removeHandler(self.psFileHandler)

        return


class MakePatternScriptsWindow():
    '''Makes a JMRI JFrame that the control panel is set into'''

    def __init__(self, scrollPanel):

        self.controlPanel = scrollPanel
        self.uniqueWindow = jmri.util.JmriJFrame(u'Pattern Scripts')
        self.uniqueWindow.setName('patternScripts')

        return

    def helpItemSelected(self, ACTION_PERFORMED):

        jmri.util.HelpUtil.openWebPage(self.helpStubPath)

        return

    def makeWindow(self):

        self.helpStubPath = MainScriptEntities.scrubPath()
        helpMenuItem = javax.swing.JMenuItem(u'Window Help...')
        helpMenuItem.addActionListener(self.helpItemSelected)

        helpMenu = javax.swing.JMenu(u'Help')
        helpMenu.add(helpMenuItem)

        toolsMenu = javax.swing.JMenu(u'Tools')
        toolsMenu.add(jmri.jmrit.operations.setup.OptionAction())
        toolsMenu.add(jmri.jmrit.operations.setup.PrintOptionAction())
        toolsMenu.add(jmri.jmrit.operations.setup.BuildReportOptionAction())

        psMenuBar = javax.swing.JMenuBar()
        psMenuBar.add(toolsMenu)
        psMenuBar.add(jmri.jmrit.operations.OperationsMenu())
        psMenuBar.add(jmri.util.WindowMenu(self.uniqueWindow))
        psMenuBar.add(helpMenu)

        self.uniqueWindow.addWindowListener(PatternScriptsWindowListener())
        self.uniqueWindow.setJMenuBar(psMenuBar)
        self.uniqueWindow.add(self.controlPanel)
        self.uniqueWindow.pack()
        self.uniqueWindow.setVisible(True)

        return

class PatternScriptsWindowListener(java.awt.event.WindowListener):
    '''Listener to respond to the plugin window operations. More on this later.'''

    def __init__(self):

        # self.psLog = logging.getLogger('PS')
        return

    def closeSetCarsWindows(self):

        for frameName in jmri.util.JmriJFrame.getFrameList():
            frame = jmri.util.JmriJFrame.getFrame(frameName)
            if frame.getName() == 'setCarsWindow':
                frame.dispose()
                frame.setVisible(False)

        return

    def windowClosed(self, WINDOW_CLOSED):

        self.closeSetCarsWindows()
        WINDOW_CLOSED.getSource().dispose()

        return

    def windowOpened(self, WINDOW_OPENED):
        return
    def windowClosing(self, WINDOW_CLOSING):
        return
    def windowActivated(self, WINDOW_ACTIVATED):
        return
    def windowDeactivated(self, WINDOW_DEACTIVATED):
        return

class StartPsPlugin(jmri.jmrit.automat.AbstractAutomaton):
    '''Start the the Pattern Scripts plugin and add selected subroutines'''

    def init(self):

    # fire up logging
        self.psLog = logging.getLogger('PS')
        self.psLog.debug('Log File for Pattern Scripts Plugin - DEBUG level test message')
        self.psLog.info('Log File for Pattern Scripts Plugin - INFO level test message')
        self.psLog.warning('Log File for Pattern Scripts Plugin - WARNING level test message')
        self.psLog.error('Log File for Pattern Scripts Plugin - ERROR level test message')
        self.psLog.critical('Log File for Pattern Scripts Plugin - CRITICAL level test message')

        return

    def handle(self):
        '''Make and populate the Pattern Scripts control panel'''

        yTimeNow = time.time()
        MainScriptEntities.validateStubFile()
        MainScriptEntities.validateFileDestinationDirestories()
        MainScriptEntities.readConfigFile()
        if not MainScriptEntities.validateConfigFile():
            MainScriptEntities.backupConfigFile()
            self.psLog.warning('PatternConfig.json.bak file written')
            MainScriptEntities.writeNewConfigFile()
            self.psLog.warning('New PatternConfig.JSON file created for this profile')
    # make a list of subroutines for the control panel
        subroutineList = []
        controlPanelConfig = MainScriptEntities.readConfigFile('CP')
        for subroutineIncludes, isIncluded in controlPanelConfig['SI'].items():
            if (isIncluded):
            # import selected subroutines and add them to a list
                xModule = __import__(subroutineIncludes, fromlist=['Controller'])
                subroutineFrame = xModule.Controller.StartUp().makeSubroutineFrame()
                subroutinePanel = xModule.Controller.StartUp().makeSubroutinePanel()
                subroutineFrame.add(subroutinePanel)
                subroutineList.append(subroutineFrame)
                self.psLog.info(subroutineIncludes + ' subroutine added to control panel')
    # plug in the subroutine list into the control panel
        controlPanel, scrollPanel = MainScriptEntities.makeControlPanel()
        for subroutine in subroutineList:
            controlPanel.add(subroutine)

        psWindow = MakePatternScriptsWindow(scrollPanel)
        psWindow.makeWindow()

        self.psLog.info('Current Pattern Scripts directory: ' + MainScriptEntities._currentPath)
        self.psLog.info('Main script run time (sec): ' + ('%s' % (time.time() - yTimeNow))[:6])

        return False

class panelProFrame:
    '''Adds a button to the PanelPro frame'''

    def __init__(self):

        self.patternScriptsButton = javax.swing.JButton(text = 'Pattern Scripts', name = 'psButton')
        self.logger = Logger()
        self.psPlugin = StartPsPlugin()

        return

    def patternButtonStart(self, MOUSE_CLICKED):

        self.logger.startLogger()
        self.psPlugin.start()
        self.patternScriptsButton.setText('Restart Pattern Scripts')
        self.patternScriptsButton.actionPerformed = self.patternButtonRestart

        return

    def patternButtonRestart(self, MOUSE_CLICKED):

        self.closePsWindow()
        self.logger.stopLogger()
        self.logger.startLogger()
        self.psPlugin.start()

        return

    def closePsWindow(self):

        for frameName in jmri.util.JmriJFrame.getFrameList():
            frame = jmri.util.JmriJFrame.getFrame(frameName)
            if frame.getName() == 'patternScripts':
                frame.dispose()
                frame.setVisible(False)

        return

    def addPsButton(self):
        self.patternScriptsButton.actionPerformed = self.patternButtonStart
        Apps.buttonSpace().add(self.patternScriptsButton)
        Apps.buttonSpace().revalidate()

        print(scriptName + ' ' + str(scriptRev))

        return

panelProFrame().addPsButton()
