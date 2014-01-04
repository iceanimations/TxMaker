'''
Created on Dec 19, 2013
@author: qurban.ali
'''
from PyQt4.QtGui import *
from PyQt4 import uic
import utilities as utils
import multiprocessing as mp

def makeTx(fileName):
    command = r"R:\Pipe_Repo\Users\Qurban\applications\maketx\maketx.exe"
    args = " -u --oiio \"%s\""%fileName
    utils.subprocess.call(command + args, shell = True)
    return fileName

Form, Base = uic.loadUiType(utils.uiFile())
class TxMaker(Form, Base):
    '''
    converts the given image to tx format
    '''
    def __init__(self, parent = None):
        super(TxMaker, self).__init__(parent)
        self.setupUi(self)
        
        #pre-conditions
        self.waitLabel.hide()
        self.makingLabel.hide()
        self.folderButton.hide()
        self.sceneButton.hide()
        self.mayaFormats = ['.ma', '.mb', '.MB', '.MA']
        self.imageFormats = utils.imageFormats
        icon = QIcon(utils.join(utils.iPath, 'txm.png'))
        self.setWindowIcon(icon)
        
        # method bindings
        self.browseButton.clicked.connect(self.setFilePath)
        self.folderButton.clicked.connect(self.handleFolderSceneButtons)
        self.sceneButton.clicked.connect(self.handleFolderSceneButtons)
        self.pathBox.returnPressed.connect(self.listTextures)
        self.selectAllButton.clicked.connect(self.selectAll)
        self.createButton.clicked.connect(self.createTx)
        self.closeButton.clicked.connect(self.closeWindow)
        self.clearButton.clicked.connect(self.clearAll)
        self.tutorialAction.triggered.connect(self.showTutorial)
        
        # member variables
        self.folderTextures = True
        self.textureButtons = []
        self.textures = []
        
    def showTutorial(self):
        utils.openURL(utils.join(utils.dPath, "tutorial.html"))
        
    def handleFolderSceneButtons(self):
        self.folderTextures = self.folderButton.isChecked()
        
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
        
    def paths(self):
        '''returns the list of textures paths'''
        path = self.pathBox.text()
        if path:
            if utils.exists(path):
                if utils.isfile(path):
                    if utils.extension(path) not in self.mayaFormats:
                        path = utils.dirname(path)
                    else:
                        self.msgBox(msg = "Select textures form folder",
                                    icon = QMessageBox.Warning)
                return utils.paths(path)
            else:
                self.msgBox(msg = "The system can not find the path specified",
                            icon = QMessageBox.Warning)
        else:
            self.msgBox(msg = "You did not specify the path",
                        icon = QMessageBox.Warning)
    
    def sceneTextures(self):
        
        path = self.pathBox.text()
        if path:
            if utils.exists(path):
                if utils.extension(path) in self.mayaFormats:
                    return utils.sceneTextures(path)
                else:
                    self.msgBox(msg = "The selected file is not a Maya file",
                                icon = QMessageBox.Warning)
            else:
                self.msgBox(msg = "The system can not find the path specified",
                            icon = QMessageBox.Warning)
        else:
            self.msgBox(msg = "You did not specify the path",
                        icon = QMessageBox.Warning)

    def listTextures(self):
        '''lists all specified textures on the window'''
        self.waitLabel.show()
        self.waitLabel.repaint()
        if self.folderTextures:
            tex = self.paths()
        else:
            tex = self.sceneTextures()
        if tex is None: self.waitLabel.hide(); return
        if not tex:
            self.msgBox(msg = "No textures found")
            self.waitLabel.hide()
            return
        self.clearWindow()
        self.textures[:] = tex
        for texture in self.textures:
            btn = QCheckBox(texture, self)
            btn.clicked.connect(self.switchSelectAllButton)
            self.texturesLayout.addWidget(btn)
            self.textureButtons.append(btn)
        self.selectAllButton.setChecked(True)
        self.selectAll()
        self.totalTexturesLabel.setText("Total Textures: "+
                                        str(len(self.textures)))
        self.waitLabel.hide()
        
            
    def clearWindow(self):
        for btn in self.textureButtons:
            btn.deleteLater()
        self.textureButtons[:] = []
        self.textures[:] = []
        self.selectAllButton.setChecked(False)
        
    def clearAll(self):
        self.folderButton.setChecked(True)
        self.quickMakeButton.setChecked(True)
        self.pathBox.clear()
        self.folderTextures = True
        self.totalTexturesLabel.setText("Total Textures: ")
        self.clearWindow()
    
    def createTx(self):
        if self.textures:
            self.createButton.setEnabled(False)
            self.clearButton.setEnabled(False)
            newTex = []
            if not self.selectAllButton.isChecked():
                for btn in self.textureButtons:
                    if btn.isChecked():
                        newTex.append(str(btn.text()))
            else: newTex[:] = self.textures
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
                    donePaths.append(it.next(timeout=0.001))
                    done = len(donePaths)
                    self.makingLabel.setText("Making \"tx\" textures: "+
                                             str(done) +" of "+ str(total))
                    self.makingLabel.repaint()
                except mp.TimeoutError:
                    pass
                except StopIteration:
                    break                    
                qApp.processEvents()
            self.makingLabel.setText("Making \"tx\" textures:")
            self.makingLabel.hide()
            self.createButton.setEnabled(True)
            self.clearButton.setEnabled(True)
    
    def closeWindow(self):
        self.close()
        self.deleteLater()
    
    def setFilePath(self):
        if self.folderTextures:
            formats = "*.png *.jpg *.jpeg *.tif *.tga *.map"
        else:
            formats = "*.mb *.ma"
        fileName = QFileDialog.getOpenFileName(self, "Select File", "",
                                               formats)
        if fileName:
            if self.folderTextures:
                fileName = utils.dirname(fileName)
            self.pathBox.setText(fileName)
            self.pathBox.repaint()
            self.listTextures()
            
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