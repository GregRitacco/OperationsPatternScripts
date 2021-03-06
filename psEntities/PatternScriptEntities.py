# coding=utf-8
# © 2021, 2022 Greg Ritacco

"""Support methods and package constants for all Pattern Script subroutines"""

import jmri as JMRI
import logging as LOGGING
from java import io as JAVA_IO
from HTMLParser import HTMLParser as HTML_PARSER

import time
from json import loads as jsonLoads, dumps as jsonDumps
from codecs import open as codecsOpen
from os import system as osSystem
import xml.etree.ElementTree as ET

PLUGIN_ROOT = ''
PROFILE_PATH = JMRI.util.FileUtil.getProfilePath()
ENCODING = ''
BUNDLE = {}
J_BUNDLE = JMRI.jmrit.operations.setup.Setup()
REPORT_ITEM_WIDTH_MATRIX = {}

SB = JMRI.jmrit.operations.setup.Bundle()

SCRIPT_NAME = 'OperationsPatternScripts.psEntities.PatternScriptEntities'
SCRIPT_REV = 20220101

LM = JMRI.InstanceManager.getDefault(JMRI.jmrit.operations.locations.LocationManager)
TM = JMRI.InstanceManager.getDefault(JMRI.jmrit.operations.trains.TrainManager)
EM = JMRI.InstanceManager.getDefault(JMRI.jmrit.operations.rollingstock.engines.EngineManager)
CM = JMRI.InstanceManager.getDefault(JMRI.jmrit.operations.rollingstock.cars.CarManager)

CMX = JMRI.InstanceManager.getDefault(JMRI.jmrit.operations.rollingstock.cars.CarManagerXml)

SM = JMRI.InstanceManager.getDefault(JMRI.jmrit.operations.locations.schedules.ScheduleManager)
PM = JMRI.InstanceManager.getDefault(JMRI.util.gui.GuiLafPreferencesManager)

_psLog = LOGGING.getLogger('PS.PE.PatternScriptEntities')


class Logger:

    def __init__(self, logPath):

        logFileFormat = LOGGING.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.psFileHandler = LOGGING.FileHandler(logPath, mode='w', encoding='utf-8')
        self.psFileHandler.setFormatter(logFileFormat)

        return

    def startLogger(self, log):

        psLog = LOGGING.getLogger(log)
        psLog.setLevel(10)
        psLog.addHandler(self.psFileHandler)

        return

    def stopLogger(self, log):

        psLog = LOGGING.getLogger(log)
        psLog.removeHandler(self.psFileHandler)

        return

    def initialLogMessage(self, log):

        log.debug('Initialize log file - DEBUG level test message')
        log.info('Initialize log file - INFO level test message')
        log.warning('Initialize log file - WARNING level test message')
        log.error('Initialize log file - ERROR level test message')
        log.critical('Initialize log file - CRITICAL level test message')

        return


class CheckTpDestination:
    """Verify or create a TrainPlayer destination directory"""

    def __init__(self):

        self.psLog = LOGGING.getLogger('PS.PE.PatternScriptEntities.CheckTpDestination')

        return

    def directoryExists(self):

        tpDirectory = JMRI.util.FileUtil.getHomePath() + 'AppData\\Roaming\\TrainPlayer\\Reports\\'
        tpDrrectoryFlag = JAVA_IO.File(tpDirectory).isDirectory()
        if tpDrrectoryFlag:
            self.psLog.info('TrainPlayer destination directory OK')
        else:
            self.psLog.warning('TrainPlayer Reports destination directory not found')
            print('TrainPlayer Reports destination directory not found')

        return tpDrrectoryFlag


class validateStubFile:
    """Copy of the JMRI Java version of createStubFile"""

    def __init__(self):

        self.stubLocation = JMRI.util.FileUtil.getPreferencesPath() + '\\jmrihelp\\'
        self.stubFileName = self.stubLocation + 'psStub.html'
        self.helpFilePath = ''
        self.newStubFile = ''

        return

    def validateStubLocation(self):

        if JAVA_IO.File(self.stubLocation).mkdir():
            _psLog.info('Stub location created at: ' + self.stubLocation)
        else:
            _psLog.info('Stub location already exists')

        return

    def makehelpFilePath(self):

        helpFilePath = PLUGIN_ROOT + '\psSupport\Help.' + psLocale() + '.html'
        if not JAVA_IO.File(helpFilePath).isFile():
            helpFilePath = PLUGIN_ROOT + '\psSupport\Help.en.html'

        helpFileUri = JAVA_IO.File(helpFilePath).toURI()
        self.helpFilePath = unicode(helpFileUri, ENCODING)

        return

    def updateStubTemplate(self):

        stubTemplateLocation = JMRI.util.FileUtil.getProgramPath() + 'help\\' \
                + psLocale()[:2] + '\\local\\stub_template.html'
        if not JAVA_IO.File(stubTemplateLocation).isFile():
            stubTemplateLocation = PLUGIN_ROOT + '\psEntities\stub_template.html'

        stubTemplate = genericReadReport(stubTemplateLocation)
        stubTemplate = stubTemplate.replace("../index.html#", "")
        stubTemplate = stubTemplate.replace("<!--HELP_KEY-->", self.helpFilePath)
        self.newStubFile = stubTemplate.replace("<!--URL_HELP_KEY-->", "")

        return self.newStubFile

    def writeStubFile(self):

        genericWriteReport(self.stubFileName, self.newStubFile)
        _psLog.debug('psStub writen from stub_template')

        return

    def isStubFile(self):

        self.validateStubLocation()
        self.makehelpFilePath()
        self.updateStubTemplate()
        self.writeStubFile()

        return


class xmlWrangler:
    """Generic queries on any operations xml file"""

    def __init__(self, xmlFile):

        self.xmlFile = xmlFile

        return

    def getXml(self, target):

        filePath = PROFILE_PATH + '\\operations\\' + self.xmlFile + '.xml'
        if not JAVA_IO.File(filePath).isFile():
            return False

        with codecsOpen(filePath, 'r', encoding=ENCODING) as textWorkFile:
            tree = ET.parse(textWorkFile)

            root = tree.getroot()
            subSection = root.findall(target)

            return subSection


def psLocale():

    return PM.getLocale().toString()
    # return unicode(PM.getLocale(), ENCODING)

def formatText(item, length):
    """Truncate each item to its defined length in PatternConfig.json and add a space at the end"""

    if len(item) < length:
        xItem = item.ljust(length)
    else:
        xItem = item[:length]

    return xItem + u' '

def makeReportItemWidthMatrix():
    """The report widths for each of the rolling stock attributes is defined in the config file.
    The keys for the width values are translated into whatever language the current profile is using.
    """

    reportItemMatrix = {}

    reportWidths = readConfigFile('RM')['AW']
    for rItem in reportWidths:
        reportItemMatrix[SB.handleGetMessage(rItem)] = reportWidths[rItem]

    reportItemMatrix[' '] = 1 # catches empty box added to Manifest Print Options

    return reportItemMatrix

def occuranceTally(listOfOccurances):
    """Tally the occurances of a word in a list and return a dictionary
    Home grown version of collections.Counter
    """

    dict = {}
    while len(listOfOccurances):
        occurance = listOfOccurances[-1]
        tally = 0
        for i in xrange(len(listOfOccurances) - 1, -1, -1): # run list from bottom up
            if (listOfOccurances[i] == occurance):
                tally += 1
                listOfOccurances.pop(i)
        dict[occurance] = tally

    return dict

def getAllLocations():
    """JMRI sorts the list"""

    allLocations = LM.getLocationsByNameList()
    locationList = []
    for item in allLocations:
        locationList.append(unicode(item.getName(), ENCODING))

    return locationList

def timeStamp(epochTime=0):
    """Valid Time, get local time adjusted for time zone and dst"""

    if epochTime == 0:
        epochTime = time.time()
    if time.localtime(epochTime).tm_isdst and time.daylight: # If local dst and dst are both 1
        timeOffset = time.altzone
    else:
        timeOffset = time.timezone # in seconds

    return time.strftime('%a %b %d %Y %I:%M %p %Z', time.gmtime(epochTime - timeOffset))

def convertJmriDateToEpoch(jmriTime):
    """2022-02-26T17:16:17.807+0000"""

    epochTime = time.mktime(time.strptime(jmriTime, "%Y-%m-%dT%H:%M:%S.%f+0000"))

    if time.localtime(epochTime).tm_isdst and time.daylight: # If local dst and dst are both 1
        epochTime -= time.altzone
    else:
        epochTime -= time.timezone # in seconds

    return epochTime

def genericReadReport(filePath):
    """try/except catches initial read of config file"""

    try:
        ENCODING
    except UnboundLocalError:
        ENCODING = 'utf-8'

    with codecsOpen(filePath, 'r', encoding=ENCODING) as textWorkFile:
        genericReport = textWorkFile.read()

    return genericReport

def genericWriteReport(filePath, genericReport):

    with codecsOpen(filePath, 'wb', encoding=ENCODING) as textWorkFile:
        textWorkFile.write(genericReport)

    return

def genericDisplayReport(genericReportPath):
    """Dealer's choice, the JMRI or Java version"""

    # JMRI.util.HelpUtil.openWindowsFile(genericReportPath)
    JAVA_AWT.Desktop.getDesktop().edit(genericReportPath)

    return

def loadJson(switchList):

    jsonSwitchList = jsonLoads(switchList)

    return jsonSwitchList

def dumpJson(switchList):

    jsonSwitchList = jsonDumps(switchList, indent=2, sort_keys=True)

    return jsonSwitchList

def validateFileDestinationDirestories():
    """Checks that the folders this plugin writes to exist"""

    destDirPath = JMRI.util.FileUtil.getProfilePath() + 'operations\\'
    listOfDirectories = ['csvManifests', 'csvSwitchLists', 'jsonManifests', 'switchLists', 'patternReports']
    x = 0
    for directory in listOfDirectories:
        testDirectory = destDirPath + directory + '\\'
        if JAVA_IO.File(testDirectory).isDirectory():
            x += 1
        else:
            JAVA_IO.File(testDirectory).mkdir()
            _psLog.warning(directory + ' created at ' + destDirPath)

    if x == len(listOfDirectories):
        _psLog.info('Destination folders check OK')

    return

def validateConfigFileVersion():
    """Checks that the config file is the current version"""

    configFilePath = PLUGIN_ROOT + '\psEntities\PatternConfig.json'
    validPatternConfig = loadJson(genericReadReport(configFilePath))
    userPatternConfig = getConfigFile()

    if validPatternConfig['CP']['RV'] == userPatternConfig['CP']['RV']:
        _psLog.info('The PatternConfig.json file is the correct version')
        return True
    else:
        _psLog.warning('PatternConfig.json version mismatch')
        return False

def backupConfigFile():

    copyFrom = JAVA_IO.File(PROFILE_PATH + 'operations\\PatternConfig.json')
    copyTo = JAVA_IO.File(PROFILE_PATH + 'operations\\PatternConfig.json.bak')
    JMRI.util.FileUtil.copy(copyFrom, copyTo)

    return

def restoreConfigFile():
    """Depricate in v3"""

    copyFrom = JAVA_IO.File(JMRI.util.FileUtil.getProfilePath() + 'operations\PatternConfig.json.bak')
    copyTo = JAVA_IO.File(PROFILE_PATH + 'operations\\PatternConfig.json')
    JMRI.util.FileUtil.copy(copyFrom, copyTo)

    return

def mergeConfigFiles():
    """Implemented in v3"""
    return

def readConfigFile(subConfig=None):

    configFile = tryConfigFile()

    if not subConfig:
        return configFile
    else:
        return configFile[subConfig]

def tryConfigFile():
    """Catch some user edit mistakes"""

    try:
        configFile = getConfigFile()
    except ValueError:
        restoreConfigFile()
        configFile = getConfigFile()
        _psLog.warning('Defective PatternConfig.json found, new file restored from backup')
    except IOError:
        writeNewConfigFile()
        configFile = getConfigFile()
        _psLog.warning('No PatternConfig.json found, new file written')

    return configFile

def getConfigFile():

    configFilePath = PROFILE_PATH + 'operations\PatternConfig.json'

    return loadJson(genericReadReport(configFilePath))

def writeConfigFile(configFile):

    configFilePath = PROFILE_PATH + 'operations\\PatternConfig.json'
    formattedConfigFile = dumpJson(configFile)
    genericWriteReport(configFilePath, formattedConfigFile)

    return

def writeNewConfigFile():

    defaultConfigFilePath = PLUGIN_ROOT + '\psEntities\PatternConfig.json'
    copyFrom = JAVA_IO.File(defaultConfigFilePath)
    copyTo = JAVA_IO.File(PROFILE_PATH + 'operations\\PatternConfig.json')
    JMRI.util.FileUtil.copy(copyFrom, copyTo)

    return

def deleteConfigFile():

    configFilePath = PROFILE_PATH + 'operations\PatternConfig.json'
    JAVA_IO.File(configFilePath).delete()

    return

def makePatternLog():
    """creates a pattern log for display based on the log level, as set by getBuildReportLevel"""

    outputPatternLog = ''
    buildReportLevel = JMRI.jmrit.operations.setup.Setup.getBuildReportLevel()
    # loggingIndex = readConfigFile('LI')
    loggingIndex = logIndex()
    logLevel = loggingIndex[buildReportLevel]

    logFileLocation = PROFILE_PATH + 'operations\\buildstatus\\PatternScriptsLog.txt'
    patternLogFile = genericReadReport(logFileLocation)
    for thisLine in patternLogFile.splitlines():

        if (loggingIndex['9'] in thisLine and int(buildReportLevel) > 0): # critical
            outputPatternLog += thisLine + '\n'
        if (loggingIndex['7'] in thisLine and int(buildReportLevel) > 0): # error
            outputPatternLog += thisLine + '\n'
        if (loggingIndex['5'] in thisLine and int(buildReportLevel) > 0): # warning
            outputPatternLog += thisLine + '\n'
        if (loggingIndex['3'] in thisLine and int(buildReportLevel) > 2): # info
            outputPatternLog += thisLine + '\n'
        if (loggingIndex['1'] in thisLine and int(buildReportLevel) > 4): # debug
            outputPatternLog += thisLine + '\n'

    return 'PatternScriptsLog_temp', outputPatternLog

def logIndex():
    """Moved here but may be put back into configFile"""

    loggingIndex = {"9": "- CRITICAL -", "7": "- ERROR -", "5": "- WARNING -", "3": "- INFO -", "1": "- DEBUG -"}

    return loggingIndex

def getGenericColor(colorName):
    """A bit of protection against bad edits"""

    colorPalette = readConfigFile('CD')['CP']

    try:
        r = colorPalette[colorName]["R"]
        g = colorPalette[colorName]["G"]
        b = colorPalette[colorName]["B"]
        a = colorPalette[colorName]["A"]

        return JAVA_AWT.Color(r, g, b, a)

    except KeyError:

        return None

def getCarColor():

    colorName = readConfigFile('CD')['carColor']
    color = getGenericColor(colorName)
    if not color:
        _psLog.warning('Car color definition not found in PatternConfig.json')

    return color

def getLocoColor():

    colorName = readConfigFile('CD')['locoColor']
    color = getGenericColor(colorName)
    if not color:
        _psLog.warning('Engine color definition not found in PatternConfig.json')

    return color

def getAlertColor():

    colorName = readConfigFile('CD')['alertColor']
    color = getGenericColor(colorName)
    if not color:
        _psLog.warning('Alert color definition not found in PatternConfig.json')

    return color

"""
Items from Config File that may be put back:

"EM": {
"1": "Mac Classic ",
"2": "open -a TextEdit ",
"4": "start notepad.exe ",
"5": "nano ",
"6": "OS2 ",
"7": "kwrite "
},

"LI": {
  "0" : "Editing these is not recommended",
  "9": "- CRITICAL -",
  "7": "- ERROR -",
  "5": "- WARNING -",
  "3": "- INFO -",
  "1": "- DEBUG -"
},

"""
