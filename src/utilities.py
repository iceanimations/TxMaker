'''
Created on Dec 19, 2013
@author: qurban.ali
'''
import os
import sys
import subprocess
import os.path as osp
import webbrowser as wb
import multiprocessing as mp

sPath = sys.modules[__name__].__file__
rPath = osp.dirname(osp.dirname(sPath))
uPath = osp.join(rPath, 'ui')
iPath = osp.join(rPath, 'icons')
dPath = osp.join(rPath, "docs")

def uiFile():
    '''returns path to main ui file'''
    return osp.join(uPath, 'window.ui')

def join(path1, path2):
    return osp.join(path1, path2)

def dirname(path):
    path = str(path)
    return osp.dirname(path)

def exists(path):
    path = str(path)
    return osp.exists(path)

def isfile(path):
    return osp.isfile(path)

def extension(path):
    path = str(path)
    return osp.splitext(path)[-1]

def openURL(url):
    wb.open_new_tab(url)

def paths(path):
    path = str(path)
    textures = []
    for f in os.listdir(path):
        fileName = osp.join(path, f)
        if osp.isfile(fileName) and extension(fileName) in imageFormats:
            textures.append(fileName)
    return textures

def sceneTextures(path):
    '''returns texture file names from maya scene'''
    path = str(path)
    import maya.cmds as cmds
    cmds.file(path, f = True, options = "v=0", o = True)
    files = cmds.ls(type = "file")
    textures = []
    for fn in files:
        fileName = cmds.getAttr(fn +".ftn")
        if extension(fileName) in imageFormats:
            textures.append(fileName)
    return textures


imageFormats = ['.png', '.PNG', '.jpg', '.JPG', '.JPEG', '.jpeg',
                '.tif', '.TIF', '.tga', '.TGA', '.map', '.MAP']