# File_rename_app
**Drag 'n Drop** - Single file/dir or batch dir renaming 'app' for all those 'files' that have terrible formatting.

Works on batch files pulled, say, [from edx-dl](https://github.com/coursera-dl/edx-dl), or files or dirs of files with *another.long.file.name.from.WAZUP.mkv* formatting.

Created in KIVY for some experience for the next semester, and to rename batches of my files.

The undo function is basic but works. Re/writes to log file that is placed in App root dir.

The replace/with phrase can be passed '*' for catching any char/space in a phrase. This needs to be in an information popup/win. NOTE: Parsing then passing the string variable to a string that can be used in a regex was also a bit of internet hunt, turns out your_regexstring = r"some_string {}".format(variable) does the job.

**TODO**: 
* Instructions,
* Walk function through a few more dirs, [maybe]
* Popup functionality: Errors, Info
* "Are You Sure?" popup - *e.g.* where someone has put a***/"" into replace/with phrase = mass deletion 

**NOTE** - KIVY resources are a bit weird and difficult to navigate for some of the more esoteric features, for example, the window.bind drop_file() call was tricky to implement, needing an __init__ call with super,  I struggled with how to code it so the variable was updated appropriately. Because of this there are a few bits of code that seem like they could be refactored, but doing so was breaking the link to the fullpath_name variable. For example, there are 2 fullpath_name calls in init and just outside. 

**POPUP** - Because of the way KIVY uses Popups, calling a Popup as a gatekeeper for file renaming buttons was challenging (as opposed to tkinter). The class can be called, but the func relies on the ok/cancel button press, which then needs to pass the func and a proceed variable back to the main class. The problem is in that the code doesn't pause when the Popup is raised. I had to implement the proceed variable in the main class init, and then utilise a gatekeeper(func_to_call) function, with a selection on the proceed variable, to raise a class instance of the PopupMsg. The PopupMsg *then* recreates the mainclassobj setting the proceed variable appropriately and then only on_press **ok** calling mainclassibj.gatekeeper(func_to_call) AGAIN. 
***I have no idea if this is a particularly efficient way of doing this.***

If you come across this and have advice or suggestions by all means let me know. FWIW I'll be doing some more basic stuff with kivy in semester 1 (Oz) but can't imagine I'll be working with it too much more for the time being. 

Feel free to play with it, at your own risk! :-)
