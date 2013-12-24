'''
Created on Dec 19, 2013

@author: qurban.ali
'''
import site
#site.addsitedir(r"R:/Pipe_Repo/Users/Qurban/mayaize")
#import mayaize2013
site.addsitedir(r"R:\Python_Scripts")
from PyQt4.QtGui import QApplication, QStyleFactory
import sys
import window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('plastique'))
    win = window.TxMaker()
    win.show()
    sys.exit(app.exec_())