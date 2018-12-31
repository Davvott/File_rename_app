# File_rename_app
**Drag 'n Drop** - Single file/dir or batch dir renaming 'app' for all those 'files' that have terrible formatting.

Works on batch files pulled, say, [from edx-dl](https://github.com/coursera-dl/edx-dl), or files or dirs of files with *another.long.file.name.from.WAZUP.mkv* formatting.

Created in KIVY for some experience for the next semester, and to rename batches of my files.

The undo function is basic but seems to work. Only basic testing done at this stage.

The replace/with phrase can be passed '*' for catching any char/space in a phrase. This needs to be in an information popup/win. Parsing then passing the string variable to a string that can be used in a regex was also a bit of internet hunt, turns out "some_string {}".format(variable) does the job.

**TODO**: 
* Instructions,
* Walk function through a few more dirs, [maybe]
* Popup functionality: Errors, Info, Proceed...
* "Are You Sure?" popup - *e.g.* where someone has put ****/"" into replace/with phrase = mass deletion 

**NOTE** - KIVY resources are a bit weird and difficult to navigate for some of the more esoteric features, for example, the window.bind drop_file() call was tricky to implement with reference to the pathname variable to be used in the core functions. I struggled with how to code it so the variable was updated appropriately. Because of this there are a few bits of code that seem like they could be refactored, but doing so was breaking the link to the variable. For example, there are 2 'list file' buttons, just because. Having said this, I didn't try creating a global variable.

If you come across this and have advice or suggestions by all means let me know. FWIW I'll be doing some more basic stuff with kivy in semester 1 (Oz) but can't imagine I'll be working with it too much more for the time being. 

Feel free to play with it, at your own risk! :-)
