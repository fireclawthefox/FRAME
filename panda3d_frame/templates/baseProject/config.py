# Python imports
import os

# Panda3D imoprts
from panda3d.core import (
    ConfigPageManager,
    ConfigVariableBool,
    OFileStream,
    loadPrcFileData,
    loadPrcFile,
    Filename)

#
# PATHS AND CONFIGS
#
# set company and application details
companyName = "{{COMPANY_NAME}}"
appName = "{{APP_NAME}}"
versionstring = "{{DATE_VERSION}}"

# build the path from the details we have
home = os.path.expanduser("~")
basedir = os.path.join(
    home,
    companyName,
    appName)
if not os.path.exists(basedir):
    os.makedirs(basedir)

# look for a config file
prcFile = os.path.join(basedir, f"{appName}.prc")
if os.path.exists(prcFile):
    mainConfig = loadPrcFile(Filename.fromOsSpecific(prcFile))

# set configurations that should not be changed from a config file
loadPrcFileData("",
f"""
    #
    # Model loading
    #
    model-path $MAIN_DIR/{appName}/assets/

    #
    # Window and graphics
    #
    window-title {appName}
    #show-frame-rate-meter 1

    #
    # Logging
    #
    #notify-level info
    notify-timestamp 1

    #
    # Audio
    #
    # Make sure to use OpenAL
    audio-library-name p3openal_audio
""")

config_variables = {}

def load_config():
    # NOTE: Add any custom changed configuration to this dictionary to make it show
    #       up in the application specific saved config file.
    # Structure:
    # Key:   configuration name
    # Value: The configurations value as represented in the config file (string)
    global config_variables
    config_variables = {
        # particles
        "particles-enabled": "#t" if base.particleMgrEnabled else "#f",
        # audio
        "audio-volume": str(round(base.musicManager.getVolume(), 2)),
        "audio-music-active": "#t" if ConfigVariableBool("audio-music-active").getValue() else "#f",
        "audio-sfx-active": "#t" if ConfigVariableBool("audio-sfx-active").getValue() else "#f",
        # logging
        "notify-output": os.path.join(basedir, "application.log"),
    }

def write_config():
    """Save current config in the prc file or if no prc file exists
    create one. The prc file is set in the prcFile variable"""
    page = None

    # Check if we have an existing configuration file
    if os.path.exists(prcFile):
        # open the config file and change values according to current
        # application settings
        page = loadPrcFile(Filename.fromOsSpecific(prcFile))
        removeDecls = []
        for dec in range(page.getNumDeclarations()):
            # Check if our variables are given.
            # NOTE: This check has to be done to not loose our base
            #       or other manual config changes by the user
            if page.getVariableName(dec) in config_variables.keys():
                removeDecls.append(page.modifyDeclaration(dec))
        for dec in removeDecls:
            page.deleteDeclaration(dec)
    else:
        # Create a config file and set default values
        cpMgr = ConfigPageManager.getGlobalPtr()
        page = cpMgr.makeExplicitPage("Application Config")

    # always write custom configurations
    for key, value in config_variables.items():
        page.makeDeclaration(key, value)
    # create a stream to the specified config file
    configfile = OFileStream(prcFile)
    # and now write it out
    page.write(configfile)
    # close the stream
    configfile.close()
