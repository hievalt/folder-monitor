# -*- coding: utf-8 -*-
import os, sys, time, glob, shutil

def load():
    mPaths = []
    # Check OS
    # Windows
    if os.name == "nt":
        os.system("chcp 65001")
        for arg in sys.argv:
            if os.path.isdir(str(arg)):
                path = str(arg + "\**").replace("\\\\", "\\")
                mPaths.append(str(path + "\**").replace("\\\\", "\\"))
                lastFolder = str(os.path.basename(os.path.normpath(path)) + "\\").replace("\\\\", "\\")
    # Linux
    elif os.name == "posix":
        for arg in sys.argv:
            if os.path.isdir(str(arg)):
                path = arg
                mPaths.append(str(path + "/**").replace("//", "/"))
                lastFolder = str(os.path.basename(os.path.normpath(path)) + "/").replace("//", "/")
    else:
        print("Current operating system is not supported.")
        exit()
    
    print("\nFolder Monitor is loading...")
    print('')

    listHandler(mPaths, path)
    
#Initialize
def listHandler(mPaths, path):
    # Time of the last check (as UNIX timestamp)
    lastCheck = time.time()
    #Load folders
    folders = []
    for directory in mPaths:
        for item in glob.glob(directory, recursive=True):
            folders.append(item)
        
    folderString = str(mPaths)
    for ch in ['**',"'",'[',']']:
        if ch in folderString:
            folderString = folderString.replace(ch, "")
    print("Info: Monitoring %s" % folderString)
    print("Info: Folders contain total of %s items" % str(len(folders)))
    with open('folderMonitor_events.txt', 'a', encoding='utf-8') as f:
                f.write("Info: Monitored folders: %s\n" % folderString)
                f.close()
    print("Info: Press Ctrl+C to stop the monitor")
    print('')

# Loop that sends one folder to monitor. Goes through all folders that were given as parameters.
    while (True):
        folders[:] = monitor(folders, mPaths, lastCheck)[:]
        lastCheck = time.time()
        time.sleep(1)
            
        
# Loop for monitoring (Ctrl+C to break)
def monitor(folders, mPaths, lastCheck):
    newFiles = []
    for directory in mPaths:
        for item in glob.glob(directory, recursive=True):
            newFiles.append(item)
    
    if (folders != newFiles):
        changedFiles = set(folders).symmetric_difference(newFiles) # Get list of file differences
        # Check if files have been added or removed
        for f in changedFiles:
            if f in newFiles:
                addedMsg(f)
            elif f in folders:
                removedMsg(f)

    # Check if files have been edited (or accessed)
    for f in newFiles:
        checkEdited(f, lastCheck)
        # checkAccessed(f, lastCheck) 
        
    lastCheck = time.time()        
    folders[:] = newFiles[:]
    return folders

# File removed message    
def removedMsg(f):
    msg = time.strftime("%c") + " - REMOVED " + os.path.basename(f) + " FROM " + os.path.dirname(f)
    print(msg)
    with open('folderMonitor_events.txt', 'a', encoding='utf-8') as fl:
        fl.write(msg+"\n")
        fl.close()
#File added message        
def addedMsg(f):
    msg = time.strftime("%c") + " - ADDED " + os.path.basename(f) + " TO " + os.path.dirname(f)
    print(msg)
    with open('folderMonitor_events.txt', 'a', encoding='utf-8') as fl:
        fl.write(msg+"\n")
        fl.close()
        
# Check if file has been edited
def checkEdited(f, lastCheck):
    try:
        if int(lastCheck) < os.path.getmtime(f) and os.path.isfile(f):
            msg = time.strftime("%c") + " - EDITED " + os.path.basename(f) + " IN " + os.path.dirname(f)
            print(msg)
            with open('folderMonitor_events.txt', 'a', encoding='utf-8') as fl:
                fl.write(msg+"\n")
                fl.close()
                time.sleep(1)
    except Exception as e:
        #print(e) 
        pass

# Check if file has been accessed (NOT USED)
def checkAccessed(f, lastCheck):
    try:
        if int(lastCheck) < os.path.getatime(f) and os.path.isfile(f):
            msg = time.strftime("%c") + " - ACCESSED " + os.path.basename(f) + " IN " + os.path.dirname(f)
            print(msg)
            with open('folderMonitor_events.txt', 'a', encoding='utf-8') as fl:
                fl.write(msg+"\n")
                fl.close()
                time.sleep(1)
    except Exception as e:
        #print(e) 
        pass    
    
load()
