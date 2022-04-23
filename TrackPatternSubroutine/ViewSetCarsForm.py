# coding=utf-8
# © 2021 Greg Ritacco

import jmri
import java.awt
import javax.swing

from psEntities import MainScriptEntities
from TrackPatternSubroutine import ViewEntities

'''Display methods for the Set Cars Form for Track X form'''

SCRIPT_NAME = 'OperationsPatternScripts.ViewSetCarsForm'
SCRIPT_REV = 20220101

def setCarsForTrackWindow(setCarsForTrackForm):

    setCarsWindow = jmri.util.JmriJFrame()
    setCarsWindow.add(setCarsForTrackForm)

    return setCarsWindow

def makeSetCarsForTrackForm(setCarsFormData):
    '''Creates and populates the "Set Cars Form for Track X" form'''

    configFile = MainScriptEntities.readConfigFile('TP')

    buttonDict = {}

    setCarsForm = javax.swing.JPanel()
    setCarsForm.setLayout(javax.swing.BoxLayout(setCarsForm, javax.swing.BoxLayout.PAGE_AXIS))

    setCarsFormHeader = makeSetCarsFormHeader(setCarsFormData)
    setCarsForm.add(setCarsFormHeader)
    setCarsForm.add(javax.swing.JSeparator())

    setCarsRowOfTracks, buttonList = makeSetCarsTrackButtons()
    buttonDict['trackButtons'] = buttonList
    setCarsForm.add(setCarsRowOfTracks)
    setCarsForm.add(javax.swing.JSeparator())

    setCarsFormBody = javax.swing.JPanel()
    setCarsFormBody.setLayout(javax.swing.BoxLayout(setCarsFormBody, javax.swing.BoxLayout.PAGE_AXIS))

    setCarsEqptRows = MakeSetCarsEqptRows(setCarsFormData)

    if setCarsFormData['locations'][0]['tracks'][0]['locos']:
        locoFormBody = javax.swing.JPanel()
        locoFormBody.setLayout(javax.swing.BoxLayout(locoFormBody, javax.swing.BoxLayout.PAGE_AXIS))
        locoFormBody.border = javax.swing.BorderFactory.createTitledBorder(u'Locomotives at ' + setCarsFormData['locations'][0]['tracks'][0]['trackName'])

        setCarsLocoRows = setCarsEqptRows.makeSetCarsLocoRows()
        for loco in setCarsLocoRows:
            locoFormBody.add(loco)
        setCarsFormBody.add(locoFormBody)

    if setCarsFormData['locations'][0]['tracks'][0]['cars']:
        carFormBody = javax.swing.JPanel()
        carFormBody.setLayout(javax.swing.BoxLayout(carFormBody, javax.swing.BoxLayout.PAGE_AXIS))
        carFormBody.border = javax.swing.BorderFactory.createTitledBorder(u'Cars at ' + setCarsFormData['locations'][0]['tracks'][0]['trackName'])

        setCarsCarRows = setCarsEqptRows.makesetCarsCarRows()
        for car in setCarsCarRows:
            carFormBody.add(car)
        setCarsFormBody.add(carFormBody)

    buttonDict['textBoxEntry'] = setCarsEqptRows.textBoxEntryList()

    setCarsFormPane = javax.swing.JScrollPane(setCarsFormBody)
    setCarsForm.add(setCarsFormPane)
    setCarsForm.add(javax.swing.JSeparator())

    setCarsSchedule, scheduleButton = makeSetCarsScheduleRow(setCarsFormData)
    buttonDict['scheduleButton'] = []
    if setCarsSchedule and MainScriptEntities.readConfigFile('TP')['AS']:
        setCarsForm.add(setCarsSchedule)
        buttonDict['scheduleButton'] = scheduleButton
        setCarsForm.add(javax.swing.JSeparator())

    setCarsFooter = MakeSetCarsFooter()
    buttonDict['footerButtons'] = setCarsFooter.getComponents()
    setCarsForm.add(setCarsFooter)

    return setCarsForm, buttonDict

def makeSwingBox(xWidth, yHeight):
    '''Makes a swing box to the desired size'''

    xName = javax.swing.Box(javax.swing.BoxLayout.X_AXIS)
    xName.setPreferredSize(java.awt.Dimension(width=xWidth, height=yHeight))

    return xName

def makeSetCarsFormHeader(setCarsFormData):
    '''Creates the "Set Cars Form for Track X" forms header'''

    configFile = MainScriptEntities.readConfigFile('TP')

    combinedHeader = javax.swing.JPanel()
    combinedHeader.setLayout(javax.swing.BoxLayout(combinedHeader, javax.swing.BoxLayout.PAGE_AXIS))
    combinedHeader.setAlignmentX(java.awt.Component.CENTER_ALIGNMENT)
    combinedHeader.border = javax.swing.BorderFactory.createEmptyBorder(10,0,10,0)

    headerRRLabel = javax.swing.JLabel(setCarsFormData['railroad'])
    headerRRLabel.setAlignmentX(java.awt.Component.CENTER_ALIGNMENT)
    headerRRBox = makeSwingBox(100, configFile['PH'])
    headerRRBox.add(headerRRLabel)

    headerYTLabel = javax.swing.JLabel()
    headerYTLabel.setAlignmentX(java.awt.Component.CENTER_ALIGNMENT)
    trackName = setCarsFormData['locations'][0]['tracks'][0]['trackName'] # There's only one track
    locationName = setCarsFormData['locations'][0]['locationName'] # There's only one location
    headerYTLabel.setText('Set Cars Form for track: ' + trackName + ' at ' + locationName)
    headerYTBox = makeSwingBox(100, configFile['PH'])
    headerYTBox.add(headerYTLabel)

    headerValidLabel = javax.swing.JLabel(setCarsFormData['date'])
    headerValidLabel.setAlignmentX(java.awt.Component.CENTER_ALIGNMENT)
    headerValidBox = makeSwingBox(100, configFile['PH'])
    headerValidBox.add(headerValidLabel)

    combinedHeader.add(headerRRLabel)
    combinedHeader.add(headerYTLabel)
    combinedHeader.add(headerValidLabel)

    return combinedHeader

def makeSetCarsTrackButtons():

    location =  MainScriptEntities.readConfigFile('TP')['PL']
    allTracksAtLoc =  MainScriptEntities.LM.getLocationByName(location).getTracksByNameList(None)

    buttonPanel = javax.swing.JPanel()
    buttonPanel.border = javax.swing.BorderFactory.createTitledBorder(u'Tracks at ' + location)
    buttonList = []
    for track in allTracksAtLoc:
        selectTrackButton = javax.swing.JButton(track.getName())
        buttonList.append(selectTrackButton)
        buttonPanel.add(selectTrackButton)

    return buttonPanel, buttonList

class MakeSetCarsEqptRows():

    def __init__(self, setCarsFormData):

        self.SCRIPT_NAME = 'OperationsPatternScripts.MakeSetCarsEqptRows'
        self.SCRIPT_REV = 20220101

        self.reportWidth = MainScriptEntities.readConfigFile('TP')['RW']
        fontSize = MainScriptEntities.PM.getFontSize()
        self.panelHeight = fontSize + 4
        self.panelWidth = fontSize - 2

        self.setCarsFormData = setCarsFormData
        self.textBoxEntry = []
        # MainScriptEntities.setColors()

        return

    def makeSetCarsLocoRows(self):
        '''Creates the locomotive lines of the pattern report form'''

        listOfLocoRows = []
        locos = self.setCarsFormData['locations'][0]['tracks'][0]['locos']

        for loco in locos:
            combinedInputLine = javax.swing.JPanel()
            combinedInputLine.setBackground(MainScriptEntities.getLocoColor())
            if loco['On Train']:
                combinedInputLine.setBackground(MainScriptEntities.getAlertColor())
            inputText = javax.swing.JTextField(5)
            self.textBoxEntry.append(inputText)
            inputBox = makeSwingBox(self.panelWidth * 6, self.panelHeight)
            inputBox.add(inputText)
            combinedInputLine.add(inputBox)

            for item in jmri.jmrit.operations.setup.Setup.getDropEngineMessageFormat():
                label = javax.swing.JLabel(loco[item])
                box = makeSwingBox(self.reportWidth[item] * self.panelWidth, self.panelHeight)
                box.add(label)
                combinedInputLine.add(box)

            combinedInputLine.add(javax.swing.Box.createHorizontalGlue())

            listOfLocoRows.append(combinedInputLine)

        return listOfLocoRows

    def makesetCarsCarRows(self):
        '''Creates the car lines of the pattern report form'''

        listOfCarRows = []
        cars = self.setCarsFormData['locations'][0]['tracks'][0]['cars']

        for car in cars:
            combinedInputLine = javax.swing.JPanel()
            combinedInputLine.setBackground(MainScriptEntities.getCarColor())
            if car['On Train']:
                combinedInputLine.setBackground(MainScriptEntities.getAlertColor())
            inputText = javax.swing.JTextField(5)
            self.textBoxEntry.append(inputText)
            inputBox = makeSwingBox(self.panelWidth * 6, self.panelHeight)
            inputBox.add(inputText)
            combinedInputLine.add(inputBox)

            for item in jmri.jmrit.operations.setup.Setup.getLocalSwitchListMessageFormat():
                label = javax.swing.JLabel(car[item])
                box = makeSwingBox(self.reportWidth[item] * self.panelWidth, self.panelHeight)
                box.add(label)
                combinedInputLine.add(box)
            combinedInputLine.add(javax.swing.Box.createHorizontalGlue())
            listOfCarRows.append(combinedInputLine)

        return listOfCarRows

    def textBoxEntryList(self):

        return self.textBoxEntry

def makeSetCarsScheduleRow(setCarsFormData):
    '''Using [0] to avoid for loop since there is only 1 location and track'''

    trackLocation = setCarsFormData['locations'][0]['locationName']
    trackName = setCarsFormData['locations'][0]['tracks'][0]['trackName']
    trackObject = MainScriptEntities.LM.getLocationByName(trackLocation).getTrackByName(trackName, None)
    scheduleObject = trackObject.getSchedule()
    schedulePanel = None
    scheduleList = []
    if (scheduleObject):
        schedulePanel = javax.swing.JPanel()
        schedulePanel.border = javax.swing.BorderFactory.createTitledBorder('Schedule for ' + trackName)
        scheduleButton = javax.swing.JButton(scheduleObject.getName())
        scheduleList.append(scheduleButton)
        schedulePanel.add(javax.swing.JLabel(u'Schedule: '))
        schedulePanel.add(scheduleButton)

    return schedulePanel, scheduleList

def MakeSetCarsFooter():

    combinedFooter = javax.swing.JPanel()
    combinedFooter.border = javax.swing.BorderFactory.createTitledBorder('Action')

    printButton = javax.swing.JButton(unicode(u'Print', MainScriptEntities.setEncoding()))
    combinedFooter.add(printButton)

    setButton = javax.swing.JButton(unicode(u'Set', MainScriptEntities.setEncoding()))
    combinedFooter.add(setButton)

    if MainScriptEntities.readConfigFile('TP')['TI']:
        trainPlayerButton = javax.swing.JButton(unicode(u'TrainPlayer', MainScriptEntities.setEncoding()))
        combinedFooter.add(trainPlayerButton)

    return combinedFooter