# File_rename_app
**Drag 'n Drop** - Single file/dir or batch dir renaming 'app' for all those 'files' that have terrible formatting.

Works on batch files pulled, say, [from edx-dl](https://github.com/coursera-dl/edx-dl), or files or dirs of files with *another.long.file.name.from.WAZUP.mkv* formatting.

Created in KIVY for some experience for the next semester, and to rename batches of my files.

The undo function is basic but works. Re/writes to log file that is placed in App root dir.

The replace/with phrase can be passed '*' for catching any char/space in a phrase. This needs to be in an information popup/win. NOTE: Parsing then passing the string variable to a string that can be used in a regex was also a bit of internet hunt, turns out your_regexstring = r"some_string {}".format(variable) does the job. i.e. Python String Formatting ftw

If replace_phrase has text, and with_ doesn't; guess what? It'll delete it!

**NOTE** - KIVY resources are a bit weird and difficult to navigate for some of the more esoteric features, for example, the window.bind drop_file() call was tricky to implement, I struggled with how to code it so the variable was updated appropriately. Because of this there are a few bits of code that seem like they could be refactored, but doing so was breaking the link to the fullpath_name variable. For example, there are 2 fullpath_name calls in init and just outside. I guess this is a case of potentially redundant code, but 'are you going to try and change it or refactor it if it only breaks again?'

**POPUP** - I've finally learned that this is the difference between static GUI and a dynamic GUI. I guess it is also to do with any logic required from the GUI should go through the main not the gui. So it makes sense to call the popup with the variables from the gatekeeper function.
--- I've now created a Popup(class) within the gatekeeper() function, that allows control over btn.bind(on_press=func()) to proceed with file/dir renaming. Given the event-driven style of Kivy, this allows the use of a Popup to gate-keep functionality without relying on time stalls or whatever while using the default kivy popup. Previously, I had created a whole Popup class but had to re-instance the main class() within it to hit the gatekeeper() and proceed with renaming. I assume not good, though I would be curious to know how much memory that takes up. I tried using EventDispatcher inheritance to bind to a ObjProp() variable within the Popup class, but it only registers change when the variable is changed <i>outside</i> the class, not by changing the variable=ObjProp() from the ok() function assigned to the ok button inside the Class. ---

TL;DR - Create a basic popup within your gate-keep func, you can control the binding of the buttons to proceed with logic and selection control easily. There's an extra layer of control in case your cat jumps on your keyboard... 


Feel free to play with it, at your own risk! :-)
