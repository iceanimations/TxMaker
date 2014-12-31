'''
Created on Dec 19, 2013
@author: qurban.ali
'''
from PyQt4.QtGui import *
from PyQt4 import uic
import utilities as utils
import multiprocessing as mp
import appUsageApp

def makeTx(command):
    utils.subprocess.call(command, shell=True)

Form, Base = uic.loadUiType(utils.uiFile())
class TxMaker(Form, Base):
    '''
    converts the given image to tx format
    '''
    def __init__(self, parent=None):
        super(TxMaker, self).__init__(parent)
        self.setupUi(self)
        
        self.makingLabel.hide()
        self.mayaFormats = ['.ma', '.mb', '.MB', '.MA']
        self.imageFormats = utils.imageFormats
        icon = QIcon(utils.join(utils.iPath, 'txm.png'))
        self.setWindowIcon(icon)
        
        self.browseButton.clicked.connect(self.browseFolder)
        self.selectAllButton.clicked.connect(self.selectAll)
        self.createButton.clicked.connect(self.createTx)
        self.closeButton.clicked.connect(self.closeWindow)
        self.clearButton.clicked.connect(self.clearAll)
        self.tutorialAction.triggered.connect(self.showTutorial)
        
        self.textureButtons = []
        self.textures = set()
        
        appUsageApp.updateDatabase('TxMaker')
        
    def showTutorial(self):
        utils.openURL(utils.join(utils.dPath, "tutorial.html"))
        
    def selectAll(self):
        '''checks all the texture buttons if user checks the selectAllButton'''
        for btn in self.textureButtons:
            btn.setChecked(self.selectAllButton.isChecked())
            
    def switchSelectAllButton(self):
        '''checks the selectAllButton if the user manually checks
        all the textures'''
        flag = True
        for btn in self.textureButtons:
            if not btn.isChecked():
                flag = False
                break
        self.selectAllButton.setChecked(flag)

    def listTextures(self, files):
        '''lists all specified textures on the window'''
        qApp.processEvents()
        for texture in files:
            if texture in self.textures:
                continue
            btn = QCheckBox(texture, self)
            btn.clicked.connect(self.switchSelectAllButton)
            self.texturesLayout.addWidget(btn)
            self.textureButtons.append(btn)
        self.textures.update(files)
        self.selectAllButton.setChecked(True)
        self.selectAll()
        self.totalTexturesLabel.setText("Total Textures: "+
                                        str(len(self.textures)))
            
    def clearWindow(self):
        for btn in self.textureButtons:
            btn.deleteLater()
        self.textureButtons[:] = []
        self.textures.clear()
        self.selectAllButton.setChecked(False)
        
    def clearAll(self):
        self.quickMakeButton.setChecked(True)
        self.totalTexturesLabel.setText("Total Textures: ")
        self.clearWindow()
    
    def createTx(self):
        makerPath = r"C:\solidangle\mtoadeploy\2015\bin\maketx.exe"
        if not utils.exists(makerPath):
            makerPath = r"C:\solidangle\mtoadeploy\2014\bin\maketx.exe"
            if not utils.exists(makerPath):
                makerPath = r"R:\Pipe_Repo\Users\Qurban\applications\maketx\maketx.exe"
        if self.textures:
            self.createButton.setEnabled(False)
            self.clearButton.setEnabled(False)
            newTex = []
            if not self.selectAllButton.isChecked():
                for btn in self.textureButtons:
                    if btn.isChecked():
                        newTex.append(makerPath+" -u --oiio \"%s\""%str(btn.text()))
            else:
                for tex in self.textures:
                    newTex.append(makerPath+" -u --oiio \"%s\""%tex)
            cpus = mp.cpu_count()
            if not self.quickMakeButton.isChecked():
                cpus = int(cpus/2)
            total = len(newTex)
            done = 0
            self.makingLabel.show()
            self.makingLabel.repaint()
            pool = mp.Pool(processes=cpus)
            it = pool.imap_unordered(makeTx, newTex)
            donePaths = []
            while 1:
                try:
                    donePaths.append(it.next(timeout=1))
                    done = len(donePaths)
                except mp.TimeoutError:
                    pass
                except StopIteration:
                    break
                self.makingLabel.setText("Making \"tx\" textures: "+
                                             str(done) +" of "+ str(total))
                qApp.processEvents()
            self.makingLabel.setText("Making \"tx\" textures:")
            self.makingLabel.hide()
            self.createButton.setEnabled(True)
            self.clearButton.setEnabled(True)
    
    def closeWindow(self):
        self.deleteLater()
    
    def browseFolder(self):
        formats = "*.png *.jpg *.jpeg *.tif *.tga *.map"
        fileNames = QFileDialog.getOpenFileNames(self, "Select File", "",
                                               formats)
        if fileNames:
            self.listTextures(fileNames)
            
    def msgBox(self, msg = None, btns = QMessageBox.Ok,
               icon = None, ques = None, details = None):
        '''
        dispalys the warnings
        @params:
            args: a dictionary containing the following sequence of variables
            {'msg': 'msg to be displayed'[, 'ques': 'question to be asked'],
            'btns': QMessageBox.btn1 | QMessageBox.btn2 | ....}
        '''
        if msg:
            mBox = QMessageBox(self)
            mBox.setWindowTitle('MakeTx')
            mBox.setText(msg)
            if ques:
                mBox.setInformativeText(ques)
            if icon:
                mBox.setIcon(icon)
            if details:
                mBox.setDetailedText(details)
            mBox.setStandardButtons(btns)
            buttonPressed = mBox.exec_()
            return buttonPressed