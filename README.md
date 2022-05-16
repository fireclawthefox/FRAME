# FRAME

**NOTE:** This is currently heavily work in progress and is not intended for productive use yet.

The FRee Adaptable Modular Editor for Panda3D.

This application gives home to multiple editors like a scene editor, gui editor and many others to come. It will automatically embed installed and supported editors.

Once editors are installed on your system, they will appear in FRAME and can be selected from the left sidebar. They will work the same as if run standalone.

Editors can be installed and updated directly from within FRAME using the Store page.

## Installation/Preparation
Currently the FRAME editor doesn't have an installer yet. Running from source only requires 3 steps though.

1. Download the sorcecode hosted here on github
2. run `pip install -r requirements.txt` from within the FRAME editor folder
3. run FRAMEs main.py (see below)

## Run FRAME
To run the editor, call `python3 main.py` from within the FRAME editor folder. Dependent on your installation of python, the call may differ slightly with for example leaving out the 3 at the end of python3 or adding .exe for running on windows.
