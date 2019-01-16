from tkinter import *
from tkinter import ttk, filedialog, messagebox
import os
import re
# TODO: Implement file, dir, and edge testing
# TODO: Information dialogbox
# TODO: drop down filedialog?


def update_listbox(log):
    """Clears and Updates Listbox
    Args:
        log: list of strings
    """
    _filelist.set('')
    for item in log:
        _filelist_box.insert(END, item)


def check_dir():
    """
    Checks pathname is a valid directory.
    """
    path = _pathname.get()
    if os.path.exists(str(path)):
        _status_msg.set("Directory exists")
        return True
    else:
        _status_msg.set("Directory does not exist")
        _alert("Directory does not exist")
        # Listbox functionality interprets space char as \n
        # return True/False
        return False


def list_files():
    """ Checks dir and calls file log to display box """
    check_dir()
    path = _pathname.get()

    _filelist.set('')
    filelist = display_file_log(path)
    update_listbox(filelist)

    updatebasename = '\\' + os.path.basename(path)
    _dir_path.set(updatebasename)


def display_file_log(path):
    """ Creates itemised list of all files in dir.
    Args:
        path: passed path=_pathname from tk
    """
    log = []
    current_dir = str(path)
    try:
        for filename in os.listdir(current_dir):
            log.append(filename)
    except:
        log.append(str(os.path.basename(path)))
    return log


def split_recursion(split_chars, string):
    """ Splits file/dir name on all split_chars.
    Args:
        split_chars: Should be string of special characters "._-="
        string: The basename of file/dir
    Returns:
        Recursively split basename as string.
    """
    if split_chars == '':
        return string
    else:
        filename = " ".join(string.split(split_chars[0]))
        return split_recursion(split_chars[1:], filename)


def replace_chars(file_string):
    """Regex driven phrase replacement. Called by rename_engine()
        Uses .format() method to insert variable into regex expression string
    Args:
        file_string: basename as string
    Returns:
        Formatted filename
    """
    replace_phrase = _replace_phrase.get()
    with_phrase = _with_phrase.get()
    replaced_chars = replace_phrase.replace("*", ".")
    reg_phrase = r'{}'.format(replaced_chars)
    regex = re.compile(reg_phrase)
    formatted_filename = regex.sub(with_phrase, file_string)
    return formatted_filename


def check_values():
    """Gate keeping on file-rename replace values"""
    replace_phrase = _replace_phrase.get()
    with_phrase = _with_phrase.get()
    # Replace chars before split
    if len(replace_phrase) == 1:
        proceed = ask_proceed(
                title='Proceed?',
                message='Are you sure you want to replace:\n'
                + "'" + str(replace_phrase) + "'" + " with "
                + "'" + str(with_phrase) + " ?")
        if not proceed:
            return False
    return True


def rename_engine(string, is_a_dir=False):
    """ Main engine for rename.
    Args:
        string: The basename of file/dir
        is_a_dir: Boolean value for suffix sub
    Returns:
        Re-named basename
    """
    replace_phrase = _replace_phrase.get()
    with_phrase = _with_phrase.get()
    # Replace chars before split
    if replace_phrase == '':
        pass
    elif "*" in replace_phrase:
        string = replace_chars(string)
    else:
        string = string.replace(replace_phrase, with_phrase)

    # Split filename on multiple characters
    split_chars = _splitchars.get()
    file_string = split_recursion(split_chars, string)
    file_name_list = file_string.split()

    keyword_end = _endafter_var.get()
    try:
        end_indice = file_name_list.index(keyword_end)
    except ValueError:
        end_indice = -2

    if not is_a_dir:
        file_suffix = file_name_list[-1]
        new_name = " ".join(file_name_list[:end_indice + 1]) + "." + file_suffix
    else:
        if keyword_end == "" or keyword_end not in file_string:
            new_name = " ".join(file_name_list)
        else:
            new_name = " ".join(file_name_list[:end_indice + 1])
    return new_name


def rename_commit():
    """Gatekeeper function to call file_rename with commit=True
    avoid tk bug when calling from .Label(func(para))
    """
    file_rename(commit=True)


def file_rename(commit=False):
    """Iterates through dir, displaying possible rename.
    Uses commit and ask_proceed() to gatekeep os.rename()
    Args:
        commit: =False, must be True to rename
    Returns:
          Display of file changes, and os.path.rename()
    """
    log = []
    win_display = []
    # Gate-keeping
    if commit:
        proceed = ask_proceed()
        if not proceed:
            return
    if not check_values():
        proceed = False
        return

    path = _pathname.get()
    try:
        os.chdir(path)
    except FileNotFoundError:  # .get() called on startup
        return
    except NotADirectoryError:  # path is file
        dirname, old_name = os.path.split(path)
        os.chdir(dirname)
        new_name = rename_engine(str(old_name))
        win_display.append(new_name)
        update_listbox(win_display)

        if commit and proceed:
            try:
                os.rename(old_name, new_name)
                log.append(old_name)
                log.append(str(new_name))
                log.append(dirname)
                log_write(log)
                return
            except PermissionError:
                _alert("File in use or open.")
                return
        _sb('File name successfully tested for rename')
        return

    # Iterate through file/folders in dir
    for filename in os.listdir(path):
        # File/dir name
        old_name = str(filename)
        is_a_dir = os.path.isdir(filename)

        # New name
        new_name = rename_engine(old_name, is_a_dir)
        win_display.append(new_name)
        if commit and proceed:
            try:
                os.rename(filename, new_name)
                log.append(old_name)
                log.append(str(new_name))
            except PermissionError:
                _alert(old_name + "Might be open or in use.\n"
                                  "It has not been renamed.")
    update_listbox(win_display)

    # Log dir name
    if commit and proceed:
        log.append(str(path))
        log_write(log)


def dir_rename(commit=True):
    """Called on dir only.
    Args:
        commit=True:
    Returns:
        Renamed directory, and os.path.rename if commit.
    """
    proceed = ask_proceed()
    path = _pathname.get()

    if not os.path.isdir(path):
        _status_msg.set("Not a directory.")
        _alert("Not a Directory!")
        return
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)

    os.chdir(dirname)
    log = []
    log_display = []
    old_name = str(basename)
    new_name = rename_engine(old_name, is_a_dir=True)

    # update log_display
    log_display.append('Potential Dir rename:')
    log_display.append(str(new_name))

    if commit and proceed:
        try:
            os.rename(old_name, new_name)
            newpath = os.path.join(dirname, new_name)
            _pathname.set(newpath)
            log.append(old_name)
            log.append(new_name)
            log.append(dirname)  # For undo() loop
            log_write(log)
            list_files()
        except PermissionError:
            _alert("Permission Error. File in use.")
    else:
        update_listbox(log_display)
        _sb('Dir not yet Renamed')


def log_write(log):
    """Writes log file for committed filename changes.
    Args:
        log: takes list of file changes
    Returns:
        None. Writes log.txt to whatever dir rename is occuring in.
    """
    homepath = str(_rootpath)
    os.chdir(homepath)
    openfile = open("log.txt", "a")
    openfile.write('stop\n')
    for el in log:
        openfile.write(el + '\n')
    openfile.close()


def undo_rename():
    """ Looks for log.txt in home dir, iterates backwards undoing
    filename changes. Limited working at the moment, for immediate undo only.
    Calls list_files() to window display.
    """
    if not ask_proceed():
        return

    undo_these_files = []
    original_filename = []

    # Open/assign/close log file

    homepath = str(_rootpath)
    try:
        os.chdir(homepath)
        logfiles = open('log.txt', 'r')
    except FileNotFoundError:
        _alert('File not found for Undo.')
        logfiles.close()
        return
    content = [line.strip('\n') for line in logfiles]
    logfiles.close()

    working_dir = content.pop()
    os.chdir(working_dir)

    lastindex = None
    # Reverse Iterate -- ['stop', Old name, new name, ...]
    for i in range(len(content) - 1, -1, -1):
        if content[i] == 'stop':
            lastindex = i
            break
        if i % 2 == 0:  # evens: 'cur_names'
            undo_these_files.append(content[i])
        else:           # odds: 'old names'
            original_filename.append(content[i])

    content = content[:lastindex]  # exclude 'stop'

    # assert len(undo_these_files) == len(original_filename)
    # Undo Rename
    for i in range(len(undo_these_files)):
        try:
            os.rename(undo_these_files[i], original_filename[i])
        except PermissionError:
            _alert('PermissionError.\n'
                   'Make sure all files are closed.')
            pass
        except FileNotFoundError:
            _alert('FileNotFound.\n'+
                   undo_these_files[i] +
                   ' has not been re-renamed.')

    # Rewrite abridged content to log
    os.chdir(homepath)
    openfile = open("log.txt", 'w')
    for el in content:
        openfile.write(el + '\n')
    openfile.close()

    # Check that pathname is updated in display
    list_files()


def _sb(msg):
    """Update Status_msg"""
    _status_msg.set(msg)


def ask_proceed(title='Renaming - Proceed?',
                message='Do you wish to proceed?'):
    """Messagebox to pass bool to proceed with operation"""
    proceed = messagebox.askokcancel(
        title,
        message)
    return proceed


def _alert(msg):
    """Popup Msg Box"""
    messagebox.showinfo(message=msg)


def listbox_select(event):
    try:
        init_path = _pathname.get()
        pathname = _filelist_box.selection_get()
        add_pathname = str(_pathname.get()) + "\\" + pathname
        _pathname.set(add_pathname)
        if not check_dir():
            _pathname.set(init_path)
        list_files()
    except:
        _sb('Did not work')


def updir():
    try:
        init_pathname = _pathname.get()
        pathname = init_pathname.split('\\')
        newname = "\\".join(pathname[:-1])
        _pathname.set(newname)
        if not check_dir():
            _pathname.set(init_pathname)
        list_files()
    except:
        _sb('Operation did not work')
        print('updir did not work')


if __name__ == '__main__':
    # Main instance of tk class
    _root = Tk()
    _root.title('File Re-name')
    _rootpath = os.path.abspath(os.path.curdir)

    # ---- Main Frame, with _root parent, internal padding=5
    _mainframe = ttk.Frame(_root, padding='5 5 5 5 ')
    _mainframe.pack(side=TOP, fill=BOTH, expand=TRUE)

    # ---- Info / FIle dropdown Frame
    # _dropdown_frame = ttk.Frame(_mainframe, padding='2 2 2 2')
    # _dropdown_frame.pack(side=TOP, fill=X, expand=TRUE)
    # _info_btn = ttk.Button(_dropdown_frame, text='INFO', padding='2 2 2 2')
    # _info_btn.pack(side=RIGHT, padx=2, pady=2)

    # --- PATH Frame, _mainframe parent, so pos=0,0 within, expand East West
    _pathname_frame = ttk.LabelFrame(_mainframe, text='Dir path', padding='5 5 5 5')
    _pathname_frame.pack(side=TOP, fill=X)

    # PATH Text Box
    _pathname = StringVar()
    _pathname.set('D:\\')

    _pathname_entry = ttk.Entry(_pathname_frame, width=40, textvariable=_pathname)
    _pathname_entry.pack(side=LEFT, fill=BOTH, expand=TRUE)
    _fetch_btn = ttk.Button(_pathname_frame, text="List Files", command=list_files)
    _fetch_btn.pack(side=RIGHT, padx=5)
    _updir_btn = ttk.Button(_pathname_frame, text='cd\\.', command=updir)
    _updir_btn.pack(side=RIGHT)
    # --- FILE LIST Frame, holds Listbox and Radio frame
    _filelist_frame = ttk.LabelFrame(_mainframe, text='File List', padding='5 5 5 5')
    _filelist_frame.pack(side=TOP, fill=BOTH, expand=TRUE)

    _filelist = StringVar()

    _filelist_box = Listbox(_filelist_frame, listvariable=_filelist, height=10, width=25)
    _filelist_box.pack(side=LEFT, fill=BOTH, expand=TRUE, padx=5)
    _filelist_box.bind('<Double-1>', listbox_select)


    # Side scrollbar for filelist_box
    _scrollbar = ttk.Scrollbar(_filelist_frame, orient=VERTICAL, command=_filelist_box.yview)
    _scrollbar.pack(side=LEFT, fill=Y)
    _filelist_box.configure(yscrollcommand=_scrollbar.set)

    # ---- Settings Frame
    _settings_frame = ttk.LabelFrame(_mainframe, text='Settings', padding='5 5 5 5')
    _settings_frame.pack(side=TOP, fill=BOTH, expand=TRUE)

    # --- END ON / SPLIT ON / REPLACE WITH --- Frames
    _end_on_frame = ttk.LabelFrame(
        _settings_frame, text='End on Phrase:', padding='2 2 2 2')
    _end_on_frame.pack(side=LEFT, fill=X, expand=TRUE)

    _split_on_frame = ttk.LabelFrame(
        _settings_frame, text='Split on chars:', padding='2 2 2 2')
    _split_on_frame.pack(side=LEFT, fill=X, expand=TRUE)

    _replace_phrase_frame = ttk.LabelFrame(
        _settings_frame, text='Replace Phrase, With Phrase:', padding='2 2 2 2')
    _replace_phrase_frame.pack(side=LEFT, fill=X, expand=TRUE)

    # Initialize variables
    _endafter_var = StringVar()
    _endafter_var.set('720p')
    _splitchars = StringVar()
    _splitchars.set('.')
    _replace_phrase = StringVar()
    _replace_phrase.set('')
    _with_phrase = StringVar()
    _with_phrase.set('')

    # Radio Buttons: assign to _endafter_var
    _endafter_720_radio = ttk.Radiobutton(
        _end_on_frame, text='720p', variable=_endafter_var, value='720p')
    _endafter_720_radio.pack(side=LEFT)
    _endafter_720_radio.configure(state='normal')
    # _endafter_720_radio.grid(row=1, column=0, padx=5, pady=2, sticky=W)

    _endafter_1080_radio = ttk.Radiobutton(
        _end_on_frame, text='1080p or ', variable=_endafter_var, value='1080p')
    _endafter_1080_radio.pack(side=LEFT)

    _endafter_entry = ttk.Entry(
        _end_on_frame, width=20, textvariable=_endafter_var)
    _endafter_entry.pack(side=LEFT, fill=X, expand=TRUE)

    # SPLIT CHAR ENTRY
    _splitchar_entry = ttk.Entry(
        _split_on_frame, width=5, textvariable=_splitchars)
    _splitchar_entry.pack(side=LEFT, fill=X, expand=TRUE)

    # REPLACE / WITH PHRASE ENTRY
    _replace_phrase_entry = ttk.Entry(
        _replace_phrase_frame, width=10, textvariable=_replace_phrase)
    _replace_phrase_entry.pack(side=LEFT, fill=X, expand=TRUE)

    _replace_with_entry = ttk.Entry(
        _replace_phrase_frame, width=10, textvariable=_with_phrase)
    _replace_with_entry.pack(side=LEFT, fill=X, expand=TRUE)

    # BUTTONS FRAME
    _buttons_frame = ttk.Frame(_mainframe, padding='5 5 5 5')
    _buttons_frame.pack(side=TOP, fill=X)
    # Apply Changes! Button
    _apply_btn = ttk.Button(
        _buttons_frame, text='Apply Changes !', command=rename_commit)
    _apply_btn.pack(side=RIGHT, padx=5)
    # Test Changes Button
    _test_changes_btn = ttk.Button(
        _buttons_frame, text='Test Changes ?', command=file_rename)
    _test_changes_btn.pack(side=RIGHT, padx=5)
    # UNDO Button
    _undo_btn = ttk.Button(
        _buttons_frame, text='Undo', command=undo_rename)
    _undo_btn.pack(side=LEFT, padx=5)

    # DIR Path Entry FRAME
    _dir_path_frame = ttk.LabelFrame(_mainframe, text='Rename Directory', padding='5 5 5 5')
    _dir_path_frame.pack(side=TOP, fill=X, expand=True)
    _dir_path = StringVar()
    _dir_path.set('D:\\')
    _dir_label = ttk.Label(_dir_path_frame, width=40, textvariable=_dir_path)
    _dir_label.pack(side=LEFT, fill=X, expand=True)
    _dir_path_btn = ttk.Button(_dir_path_frame, text='Rename Dir', command=dir_rename)
    _dir_path_btn.pack(side=RIGHT, padx=5)

    # STATUS FRAME
    _status_frame = ttk.Frame(
        _root, relief='sunken', padding='5 5 5 5')
    _status_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)

    _status_msg = StringVar()
    _status_msg.set('Type a Path to start...')

    # Label holds status_msg, starting West, extends L/R
    _status = ttk.Label(
        _status_frame, textvariable=_status_msg, anchor=W)
    _status.pack(side=LEFT, fill=X)

    _root.mainloop()

