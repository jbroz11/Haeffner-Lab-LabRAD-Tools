from PyQt4 import QtGui
import sys
import os
import subprocess
from functools import partial

class CONFIG_EDITOR(QtGui.QMainWindow):

    def __init__(self):
        super(CONFIG_EDITOR, self).__init__()

        self.current_file = None
        self.get_config_files('/home/lattice/LabRAD')
        self.initUI()


    def get_config_files(self, folder = '.'):
        # finds all config files in folder
        self.config_path_list = []
        self.config_file_list = []
        
        for (paths, dirs, files) in os.walk(folder):
            for file in files:
                if      'config' in file \
                    and 'example' not in file \
                    and 'sample' not in file \
                    and '.pyc' not in file \
                    and '.jar' not in file \
                    and '.git' not in paths: # check if filename contains string 'config'

                    self.config_path_list.append(paths)
                    self.config_file_list.append(file)



    def initUI(self):
        newAction = QtGui.QAction('New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('Create new file')
        newAction.triggered.connect(self.newFile)

        saveAction = QtGui.QAction('Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current file')
        saveAction.triggered.connect(self.saveFile)

        openAction = QtGui.QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open a file')
        openAction.triggered.connect(partial(self.openFile, None))

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(openAction)

        fileMenu = menubar.addMenu('&Config Files')

        self.file_actions = []
        for k, path in sorted(zip(self.config_file_list, self.config_path_list)):
            hlp = path.split('/')
            self.file_actions.append(QtGui.QAction(hlp[-1] + '/' + k, self))
            self.file_actions[-1].triggered.connect(partial(self.open_config_file, k, path))
            fileMenu.addAction(self.file_actions[-1])

        self.text = QtGui.QTextEdit(self)
        self.setCentralWidget(self.text)
        self.setGeometry(300,300,300,300)
        self.setWindowTitle('Notepad')
        self.show()

    def open_config_file(self, filename, path):
        full_filename = os.path.join(path, filename)
        self.openFile(full_filename)
        self.current_file = full_filename

    def newFile(self):
        self.text.clear()
        self.current_file = None

    def saveFile(self):
        if self.current_file is None:
            # dialog appears only for non-config files
            filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))

        to_save_filename = self.current_file
        f = open(to_save_filename, 'w')
        filedata = self.text.toPlainText()
        f.write(filedata)
        f.close()

    def openFile(self, filename = None):
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))

        try:
            f = open(filename, 'r')
            filedata = f.read()
            self.text.setText(filedata)
            f.close()            
        except:
            return
         


def main():

    app = QtGui.QApplication(sys.argv)

    config_editor = CONFIG_EDITOR()

    sys.exit(app.exec_())

     

if __name__ == '__main__':

    main()

  
