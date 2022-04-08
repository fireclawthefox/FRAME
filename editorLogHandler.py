import sys
import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from logging import StreamHandler


from panda3d.core import (
    loadPrcFileData,
    loadPrcFile,
    Filename,
    ConfigVariableSearchPath,
)

def setup_log(editor_name):
    # check if we have a config file
    home = os.path.expanduser("~")
    basePath = os.path.join(home, f".{editor_name}")
    if not os.path.exists(basePath):
        os.makedirs(basePath)
    logPath = os.path.join(basePath, "logs")
    if not os.path.exists(logPath):
        os.makedirs(logPath)

    # Remove log files older than 30 days
    for f in os.listdir(logPath):
        fParts = f.split(".")
        fDate = datetime.now()
        try:
            fDate = datetime.strptime(fParts[-1], "%Y-%m-%d_%H")
            delta = datetime.now() - fDate
            if delta.days > 30:
                #print(f"remove {os.path.join(logPath, f)}")
                os.remove(os.path.join(logPath, f))
        except Exception:
            # this file does not have a date ending
            pass

    logfile = os.path.join(logPath, f"{editor_name}.log")
    handler = TimedRotatingFileHandler(logfile)
    consoleHandler = StreamHandler()
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[handler])#, consoleHandler])


    prcFileName = os.path.join(basePath, f".{editor_name}.prc")
    if os.path.exists(prcFileName):
        loadPrcFile(Filename.fromOsSpecific(prcFileName))
    else:
        with open(prcFileName, "w") as prcFile:
            prcFile.write("skip-ask-for-quit #f\n")
            prcFile.write("frame-enable-scene-editor #t\n")
            prcFile.write("frame-enable-gui-editor #t\n")

    return logfile
