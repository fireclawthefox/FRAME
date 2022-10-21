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
### Installing
To install the editor from source, run the following:
`python3 setup.py install --user`
This will install the application into your python site packages
Then just run it from the terminal like this:
`panda3d-frame`

### From source
To run the editor directly from source, call
`python3 -m panda3d_frame.__init__`
from within the FRAME editor folder.

Dependent on your installation of python, the call may differ slightly with for example leaving out the 3 at the end of python3 or adding .exe for running on windows.

## Official Editors
Official editors of the FRAME can be installed through the FRAMES editor store page. Currently those include the following:

### Scene Editor
https://github.com/fireclawthefox/SceneEditor

### GUI Designer
https://github.com/fireclawthefox/DirectGuiDesigner

### Logic Editor
https://github.com/fireclawthefox/NodeEditor

## Custom Editors
In addition to the editors installable through the FRAME itself, custom editors can be created and easily be added.

### Writing a custom editor
A template for an editor can be found in the sources templates/Editor/ folder.
The python file fouund in that template folder will be the main entry point class of your editor and contains all methods that will be used by the FRAME. If your editor doesn't make use of some of the methods, just leave them as they are but don't remove them. A description of what each function is used for can be found in the source.

After creating an editor, you can include it in the FRAME by creating a new editor definition file. A definition template is also located in the template folder mentioned above. Currently it consists of the following entries
|Tag|Description|
|--|--|
|name|The visible name of your editor|
|module|Module name from where to import your editor (e.g. the **x.y** part of `from x.y import Editor`|
|class|Class name to import from the module of youur editor (e.g. the **Editor** part of `from x.y import Editor`|
|configToEnable|The name users can set in the editors config to enable/disable the editor. This should start with "frame-enable-"|
|order|An integer value to set the order of the editor in the editor selection panel of the FRAME.|
|icon|An icon name or path relative to the location of the definition json file|
|fileExtension|Not yet used, but should contain the file extension used by the files saved by this editor|
|extraArgsFunc|A function name to be called from the class given in the class tag (example call `Editor.myExtraArgsFunc()`). This method should return what will be passed as arguments when instantiating the editor|
|extraArgs|A json list. Each list entry will be passed as a parameter when instantiating the editor class|

