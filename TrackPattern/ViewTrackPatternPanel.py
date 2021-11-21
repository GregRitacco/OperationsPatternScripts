# coding=utf-8
# Extended ìÄÅÉî
# Creates the track pattern and its panel
# No restrictions on use
# © 2021 Greg Ritacco

import jmri
import javax.swing
import java.awt
from sys import path
path.append(jmri.util.FileUtil.getHomePath() + 'JMRI\\OperationsTrackPattern')
import MainScriptEntities

class TrackPatternPanel:
    '''Makes the track pattern subroutine panel'''

    scriptRev = 'TrackPattern.ViewTrackPatternPanel v20211101'

    def __init__(self):

        self.configFile = MainScriptEntities.readConfigFile('TP')
        self.patternInput = javax.swing.JTextField(20) # the location is typed into this box
        self.useYardTracks = javax.swing.JCheckBox(u'Yard tracks only ', self.configFile['PA'])
        self.ignoreLength = javax.swing.JCheckBox(u'Ignore track length ', self.configFile['PI'])
        self.ypButton = javax.swing.JButton()
        self.scButton = javax.swing.JButton()
        self.prButton = javax.swing.JButton()
        self.trackCheckBoxes = []
        self.controlObjects = []

        return

    def makePatternFrame(self):
        '''Make the panel that all the track pattern controls are added to'''

        tpFrame = javax.swing.JPanel() # the track pattern panel
        tpFrame.setLayout(javax.swing.BoxLayout(tpFrame, javax.swing.BoxLayout.Y_AXIS))
        tpFrame.border = javax.swing.BorderFactory.createTitledBorder(u'Track Pattern')

        return tpFrame

    def makeLocationInputBox(self):
        '''Make the field that the user types the location into'''

        patternLabel = javax.swing.JLabel(u'  Location: ')
        patternLabel.setAlignmentX(javax.swing.JLabel.RIGHT_ALIGNMENT)
        self.patternInput.setText(self.configFile['PL']) # pattern location
        patternInputBox = javax.swing.Box(javax.swing.BoxLayout.X_AXIS) # make a box for the label and input box
        patternInputBox.setPreferredSize(java.awt.Dimension(self.configFile['PW'], self.configFile['PH']))
        patternInputBox.add(patternLabel)
        patternInputBox.add(self.patternInput)

        return patternInputBox

    def makeLocationComboBox(self):
        '''make the combo box of user selectable locations'''

        patternLabel = javax.swing.JLabel(u'Location:')
        locationList = self.configFile['AL']
        self.locationComboBox = javax.swing.JComboBox(locationList)
        self.locationComboBox.setSelectedItem(self.configFile['PL'])
        # self.locationComboBox.addActionListener(ComboBoxListener())
        patternComboBox = javax.swing.Box(javax.swing.BoxLayout.X_AXIS)
        patternComboBox.add(patternLabel)
        patternComboBox.add(javax.swing.Box.createRigidArea(java.awt.Dimension(8,0)))
        patternComboBox.add(self.locationComboBox)

        return patternComboBox

    def makeLocationCheckBoxes(self):
        '''Any tarck type and ignore length flags'''

        flagInputBox = javax.swing.Box(javax.swing.BoxLayout.X_AXIS) # make a box for the label and input box
        flagInputBox.setPreferredSize(java.awt.Dimension(self.configFile['PW'], self.configFile['PH']))
        flagInputBox.add(self.useYardTracks)
        flagInputBox.add(self.ignoreLength)

        return flagInputBox

    def makeTrackCheckBoxes(self):
        '''Make a panel of check boxes, one for each track'''

        rowLabel = javax.swing.JLabel()
        tracksPanel = javax.swing.JPanel()
        tracksPanel.setAlignmentX(javax.swing.JPanel.CENTER_ALIGNMENT)
        tracksPanel.add(rowLabel)
        trackDict = self.configFile['PT'] # pattern tracks
        if (trackDict):
            rowLabel.text = u'Track List: '
            for track, flag in trackDict.items():
                x = javax.swing.JCheckBox(track, flag)
                tracksPanel.add(x)
                self.trackCheckBoxes.append(x)
            self.ypButton.setEnabled(True)
            self.scButton.setEnabled(True)
        else:
            self.ypButton.setEnabled(False)
            self.scButton.setEnabled(False)
            rowLabel.text = u'TThere are no yard tracks for this location'

        return tracksPanel

    def makeButtonPanel(self):
        '''button panel added to makeTrackPatternPanel'''

        self.ypButton.text = u'Pattern'
        self.scButton.text = u'Set Cars'
        self.prButton.text = u'View Log'
        buttonPanel = javax.swing.JPanel()
        buttonPanel.setAlignmentX(javax.swing.JPanel.CENTER_ALIGNMENT)
        buttonPanel.add(self.ypButton)
        buttonPanel.add(self.scButton)
        buttonPanel.add(self.prButton)

        return buttonPanel

    def getPanelWidgets(self):
        '''A list of the widgets created by this class'''

        self.controlObjects.append(self.locationComboBox)
        self.controlObjects.append(self.useYardTracks)
        self.controlObjects.append(self.ignoreLength)
        self.controlObjects.append(self.trackCheckBoxes)
        self.controlObjects.append(self.ypButton)
        self.controlObjects.append(self.scButton)
        self.controlObjects.append(self.prButton)

        return self.controlObjects

    def makePatternControls(self):
        '''Make the Track Pattern panel object'''

        tpPanel = javax.swing.JPanel() # the track pattern panel
        tpPanel.setLayout(javax.swing.BoxLayout(tpPanel, javax.swing.BoxLayout.Y_AXIS))
        inputRow = javax.swing.JPanel()
        inputRow.setLayout(javax.swing.BoxLayout(inputRow, javax.swing.BoxLayout.X_AXIS))
        inputRow.add(javax.swing.Box.createRigidArea(java.awt.Dimension(12,0)))
        inputRow.add(self.makeLocationComboBox())
        inputRow.add(javax.swing.Box.createRigidArea(java.awt.Dimension(8,0)))
        inputRow.add(self.makeLocationCheckBoxes())
        trackCheckBoxes = self.makeTrackCheckBoxes()
        buttonPanel = self.makeButtonPanel()
        tpPanel.add(inputRow)
        tpPanel.add(trackCheckBoxes)
        tpPanel.add(buttonPanel)
        controlObjects = self.getPanelWidgets()

        return tpPanel, controlObjects

    print(scriptRev)