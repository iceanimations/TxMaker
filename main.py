'''
Created on Dec 19, 2013

@author: qurban.ali
'''
from PyQt4.QtGui import QApplication, QStyleFactory
import sys
import src.window as window

if __name__ == "__main__":
    
    # update the database, how many times this app is used
    try:
        import site
        site.addsitedir(r'r:/pipe_repo/users/qurban/utilities')
        import appUsageApp
        appUsageApp.updateDatabase('TxMaker')
    except: pass
    app = QApplication(sys.argv)
    win = window.TxMaker()
    win.show()
    sys.exit(app.exec_())