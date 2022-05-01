# coding=utf-8
# © 2021, 2022 Greg Ritacco

import jmri
import java.awt.event

import logging
from os import system as osSystem

from psEntities import PatternScriptEntities
# from TrainPlayerSubroutine import Model
from TrainPlayerSubroutine import View

SCRIPT_NAME = 'OperationsPatternScripts.TrainPlayerSubroutine.Controller'
SCRIPT_REV = 20220101

class StartUp:
    '''Start the Track Pattern subroutine'''

    def __init__(self, subroutineFrame=None):

        self.psLog = logging.getLogger('PS.TrianPlayer.Control')
        self.subroutineFrame = subroutineFrame

        return

    def makeSubroutineFrame(self):
        '''Makes the title border frame'''

        self.subroutineFrame = View.ManageGui().makeSubroutineFrame()
        subroutinePanel = self.makeSubroutinePanel()
        self.subroutineFrame.add(subroutinePanel)

        return self.subroutineFrame

    def makeSubroutinePanel(self):
        '''Makes the control panel that sits inside the frame'''

        self.subroutinePanel, self.widgets = View.ManageGui().makeSubroutinePanel()
        # self.activateWidgets()

        self.psLog.info('Track pattern makeFrame completed')

        return self.subroutinePanel

    def validateSubroutineConfig(self):
        '''Put a test here that validates config file ["T"]'''

        if not PatternScriptEntities.readConfigFile('PT')['AL']:
            PatternScriptEntities.writeNewConfigFile()
            Model.updatePatternLocation()

        return