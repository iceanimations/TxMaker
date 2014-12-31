'''
Created on Dec 19, 2013

@author: qurban.ali
'''
import site
site.addsitedir('r:/python_scripts/maya2015/pyqt')
site.addsitedir(r'r:/pipe_repo/users/qurban/utilities')
from PyQt4.QtGui import QApplication, QStyleFactory
import sys
import src.window as window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    global win
    win = window.TxMaker()
    win.show()
    sys.exit(app.exec_())