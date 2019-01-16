import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter import StringVar
from tkinter import Listbox
from tkinter import Radiobutton
import os
import re


# TODO: Information popup/Alert
# TODO: variable reference - pass into classes or refer up?
# TODO: clear logfile.txt on startup
# TODO: save / import settings re: Movie, Music, Edx
# TODO: Implmement walk_dir func()btn

class DirBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Labels, Buttons, Entry's
        _pathname_frame = ttk.LabelFrame(self.parent, text='Dir path', padding='5 5 5 5')
        _pathname_frame.pack(side='top', fill='x')
        _pathname_entry = ttk.Entry(_pathname_frame, width=40, textvariable=self.parent._pathname)
        _pathname_entry.pack(side='left', fill='both', expand=True)
        _fetch_btn = ttk.Button(_pathname_frame, text="List Files", command=self.parent.list_files)
        _fetch_btn.pack(side='right', padx=5)
        _updir_btn = ttk.Button(_pathname_frame, text='cd\\.', command=self.parent.updir)
        _updir_btn.pack(side='right', padx=5)
        # Events, Btn Clicks, Mouse Clicks


class ContentBox(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        _filelist_frame = ttk.LabelFrame(self.parent, text='File List', padding='5 5 5 5')
        _filelist_frame.pack(side='top', fill='both', expand=True)

        self._filelist_box = Listbox(_filelist_frame, listvariable=self.parent._filelist, height=10, width=25)
        self._filelist_box.pack(side='left', fill='both', expand=True, padx=5)
        self._filelist_box.bind('<Double-1>', self.parent.listbox_select)
        _scrollbar = ttk.Scrollbar(_filelist_frame, orient='vertical', command=self._filelist_box.yview)
        _scrollbar.pack(side='left', fill='y')
        self._filelist_box.configure(yscrollcommand=_scrollbar.set)



class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        _settings_frame = ttk.LabelFrame(self.parent, text='Settings', padding='5 5 5 5')
        _settings_frame.pack(side='top', fill='both', expand=True)

        # --- END ON / SPLIT ON / REPLACE WITH --- Frames
        _end_on_frame = ttk.LabelFrame(
            _settings_frame, text='End on Phrase:', padding='2 2 2 2')
        _end_on_frame.pack(side='left', fill='x', expand=True)

        _split_on_frame = ttk.LabelFrame(
            _settings_frame, text='Split on chars:', padding='2 2 2 2')
        _split_on_frame.pack(side='left', fill='x', expand=True)

        _replace_phrase_frame = ttk.LabelFrame(
            _settings_frame, text='Replace Phrase, With Phrase:', padding='2 2 2 2')
        _replace_phrase_frame.pack(side='left', fill='x', expand=True)

        # Events, Btn Clicks, Mouse Clicks
        _endafter_720_radio = ttk.Radiobutton(
            _end_on_frame, text='720p', variable=self.parent._endafter_var, value='720p')
        _endafter_720_radio.pack(side='left')
        _endafter_720_radio.configure(state='normal')
        # _endafter_720_radio.grid(row=1, column=0, padx=5, pady=2, sticky=W)

        _endafter_1080_radio = ttk.Radiobutton(
            _end_on_frame, text='1080p or ', variable=self.parent._endafter_var, value='1080p')
        _endafter_1080_radio.pack(side='left')

        _endafter_entry = ttk.Entry(
            _end_on_frame, width=20, textvariable=self.parent._endafter_var)
        _endafter_entry.pack(side='left', fill='x', expand=True)

        # SPLIT CHAR ENTRY
        _splitchar_entry = ttk.Entry(
            _split_on_frame, width=5, textvariable=self.parent._splitchars)
        _splitchar_entry.pack(side='left', fill='x', expand=True)

        # REPLACE / WITH PHRASE ENTRY
        _replace_phrase_entry = ttk.Entry(
            _replace_phrase_frame, width=10, textvariable=self.parent._replace_phrase)
        _replace_phrase_entry.pack(side='left', fill='x', expand=True)

        _replace_with_entry = ttk.Entry(
            _replace_phrase_frame, width=10, textvariable=self.parent._with_phrase)
        _replace_with_entry.pack(side='left', fill='x', expand=True)

class ButtonsBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Labels, Buttons, Entry's
        _buttons_frame = ttk.Frame(self.parent, padding='5 5 5 5')
        _buttons_frame.pack(side='top', fill='x')
        # Apply Changes! Button
        _apply_btn = ttk.Button(
            _buttons_frame, text='Apply Changes !', command=self.parent.rename_commit)
        _apply_btn.pack(side='right', padx=5)
        # Test Changes Button
        _test_changes_btn = ttk.Button(
            _buttons_frame, text='Test Changes ?', command=self.parent.file_rename)
        _test_changes_btn.pack(side='right', padx=5)
        # UNDO Button
        _undo_btn = ttk.Button(
            _buttons_frame, text='Undo', command=self.parent.undo_rename)
        _undo_btn.pack(side='left', padx=5)
        # Events, Btn Clicks, Mouse Clicks


class Statusbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Labels, Buttons, Entry's
        _status_frame = ttk.Frame(
            self.parent, relief='sunken', padding='5 5 5 5')
        _status_frame.pack(side='bottom', fill='x', padx=5, pady=5)

        # Label holds status_msg, starting West, extends L/R
        _status = ttk.Label(
            _status_frame, textvariable=self.parent._status_msg, anchor='w')
        _status.pack(side='left', fill='x')

        # Events, Btn Clicks, Mouse Clicks


class DirName(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        # Labels, Buttons, Entry's
        _dir_path_frame = ttk.LabelFrame(self.parent, text='Rename Directory', padding='5 5 5 5')
        _dir_path_frame.pack(side='top', fill='x', expand=True)
        _dir_label = ttk.Label(_dir_path_frame, width=40, textvariable=self.parent._dir_path)
        _dir_label.pack(side='left', fill='x', expand=True)
        _dir_path_btn = ttk.Button(_dir_path_frame, text='Rename Dir', command=self.parent.dir_rename)
        _dir_path_btn.pack(side='right', padx=5)
        # Events, Btn Clicks, Mouse Clicks


class MainApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self._rootpath = os.path.abspath(os.path.curdir)
        self._pathname = StringVar()
        self._pathname.set('D:\\')
        self._filelist = StringVar()
        self._filelist.set('')
        self._endafter_var = StringVar()
        self._endafter_var.set('720p')
        self._splitchars = StringVar()
        self._splitchars.set('.')
        self._replace_phrase = StringVar()
        self._replace_phrase.set('')
        self._with_phrase = StringVar()
        self._with_phrase.set('')
        self._dir_path = StringVar()
        self._dir_path.set('D:\\')
        self._status_msg = StringVar()
        self._status_msg.set('Type a Path to start...')

        self.dir_bar = DirBar(self)
        self.content = ContentBox(self)
        self.statusbar = Statusbar(self)
        self.toolbar = Toolbar(self)
        self.command_bar = ButtonsBar(self)
        self.dir_name = DirName(self)

        self.dir_bar.pack(side='top', fill='x', expand=True)
        self.toolbar.pack(side="top", fill="x")
        self.content.pack(side='top', fill='both', expand=True, padx=5, pady=5)
        self.command_bar.pack(side='top', fill='x', expand=True, padx=5, pady=5)
        self.dir_name.pack(side="top", fill="both", expand=True)
        self.statusbar.pack(side="bottom", fill="x")


    def update_listbox(self, log):
        """Clears and Updates Listbox
        Args:
            log: list of strings
        """
        self._filelist.set('')
        for item in log:
            self.content._filelist_box.insert(-1, item)

    def check_dir(self):
        """
        Checks pathname is a valid directory.
        """
        path = self._pathname.get()
        if os.path.exists(str(path)):
            self._status_msg.set("Directory exists")
            return True
        else:
            self._status_msg.set("Directory does not exist")
            self._alert("Directory does not exist")
            # Listbox functionality interprets space char as \n
            # return True/False
            return False

    def list_files(self):
        """ Checks dir and calls file log to display box """
        self.check_dir()
        path = self._pathname.get()

        self._filelist.set('')
        filelist = self.display_file_log(path)
        self.update_listbox(filelist)

        updatebasename = '\\' + os.path.basename(path)
        self._dir_path.set(updatebasename)

    def display_file_log(self, path):
        """ Creates itemised list of all files in dir.
        Args:
            path: passed path=self._pathname from tk
        """
        log = []
        current_dir = str(path)
        try:
            for filename in os.listdir(current_dir):
                log.append(filename)
        except:
            log.append(str(os.path.basename(path)))
        return log

    def split_recursion(self, split_chars, string):
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
            return self.split_recursion(split_chars[1:], filename)

    def replace_chars(self, file_string):
        """Regex driven phrase replacement. Called by rename_engine()
            Uses .format() method to insert variable into regex expression string
        Args:
            file_string: basename as string
        Returns:
            Formatted filename
        """
        replace_phrase = self._replace_phrase.get()
        with_phrase = self._with_phrase.get()
        replaced_chars = replace_phrase.replace("*", ".")
        reg_phrase = r'{}'.format(replaced_chars)
        regex = re.compile(reg_phrase)
        formatted_filename = regex.sub(with_phrase, file_string)
        return formatted_filename

    def check_values(self):
        """Gate keeping on file-rename replace values"""
        replace_phrase = self._replace_phrase.get()
        with_phrase = self._with_phrase.get()
        # Replace chars before split
        if len(replace_phrase) == 1:
            proceed = self.ask_proceed(
                title='Proceed?',
                message='Are you sure you want to replace:\n'
                        + "'" + str(replace_phrase) + "'" + " with "
                        + "'" + str(with_phrase) + " ?")
            if not proceed:
                return False
        return True

    def rename_engine(self, string, is_a_dir=False):
        """ Main engine for rename.
        Args:
            string: The basename of file/dir
            is_a_dir: Boolean value for suffix sub
        Returns:
            Re-named basename
        """
        replace_phrase = self._replace_phrase.get()
        with_phrase = self._with_phrase.get()
        # Replace chars before split
        if replace_phrase == '':
            pass
        elif "*" in replace_phrase:
            string = self.replace_chars(string)
        else:
            string = string.replace(replace_phrase, with_phrase)

        # Split filename on multiple characters
        split_chars = self._splitchars.get()
        file_string = self.split_recursion(split_chars, string)
        file_name_list = file_string.split()

        keyword_end = self._endafter_var.get()
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

    def rename_commit(self):
        """Gatekeeper function to call file_rename with commit=True
        avoid tk bug when calling from .Label(func(para))
        """
        self.file_rename(commit=True)

    def file_rename(self, commit=False):
        """Iterates through dir, displaying possible rename.
        Uses commit and self.ask_proceed() to gatekeep os.rename()
        Args:
            commit: =False, must be True to rename
        Returns:
              Display of file changes, and os.path.rename()
        """
        log = []
        win_display = []
        # Gate-keeping
        if commit:
            proceed = self.ask_proceed()
            if not proceed:
                return
        if not self.check_values():
            proceed = False
            return

        path = self._pathname.get()
        try:
            os.chdir(path)
        except FileNotFoundError:  # .get() called on startup
            return
        except NotADirectoryError:  # path is file
            dirname, old_name = os.path.split(path)
            os.chdir(dirname)
            new_name = self.rename_engine(str(old_name))
            win_display.append(new_name)
            self.update_listbox(win_display)

            if commit and proceed:
                try:
                    os.rename(old_name, new_name)
                    log.append(old_name)
                    log.append(str(new_name))
                    log.append(dirname)
                    self.log_write(log)
                    return
                except PermissionError:
                    self._alert("File in use or open.")
                    return
            self._sb('File name successfully tested for rename')
            return

        # Iterate through file/folders in dir
        for filename in os.listdir(path):
            # File/dir name
            old_name = str(filename)
            is_a_dir = os.path.isdir(filename)

            # New name
            new_name = self.rename_engine(old_name, is_a_dir)
            win_display.append(new_name)
            if commit and proceed:
                try:
                    os.rename(filename, new_name)
                    log.append(old_name)
                    log.append(str(new_name))
                except PermissionError:
                    self._alert(old_name + "Might be open or in use.\n"
                                      "It has not been renamed.")
        self.update_listbox(win_display)

        # Log dir name
        if commit and proceed:
            log.append(str(path))
            self.log_write(log)

    def dir_rename(self, commit=True):
        """Called on dir only.
        Args:
            commit=True:
        Returns:
            Renamed directory, and os.path.rename if commit.
        """
        proceed = self.ask_proceed()
        path = self._pathname.get()

        if not os.path.isdir(path):
            self._status_msg.set("Not a directory.")
            self._alert("Not a Directory!")
            return
        dirname = os.path.dirname(path)
        basename = os.path.basename(path)

        os.chdir(dirname)
        log = []
        log_display = []
        old_name = str(basename)
        new_name = self.rename_engine(old_name, is_a_dir=True)

        # update log_display
        log_display.append('Potential Dir rename:')
        log_display.append(str(new_name))

        if commit and proceed:
            try:
                os.rename(old_name, new_name)
                newpath = os.path.join(dirname, new_name)
                self._pathname.set(newpath)
                log.append(old_name)
                log.append(new_name)
                log.append(dirname)  # For undo() loop
                self.log_write(log)
                self.list_files()
            except PermissionError:
                self._alert("Permission Error. File in use.")
        else:
            self.update_listbox(log_display)
            self._sb('Dir not yet Renamed')

    def log_write(self, log):
        """Writes log file for committed filename changes.
        Args:
            log: takes list of file changes
        Returns:
            None. Writes log.txt to whatever dir rename is occuring in.
        """
        homepath = str(self._rootpath)
        os.chdir(homepath)
        openfile = open("log.txt", "a")
        openfile.write('stop\n')
        for el in log:
            openfile.write(el + '\n')
        openfile.close()

    def undo_rename(self):
        """ Looks for log.txt in home dir, iterates backwards undoing
        filename changes. Limited working at the moment, for immediate undo only.
        Calls list_files() to window display.
        """
        if not self.ask_proceed():
            return

        undo_these_files = []
        original_filename = []

        # Open/assign/close log file

        homepath = str(self._rootpath)
        try:
            os.chdir(homepath)
            logfiles = open('log.txt', 'r')
        except FileNotFoundError:
            self._alert('File not found for Undo.')
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
            else:  # odds: 'old names'
                original_filename.append(content[i])

        content = content[:lastindex]  # exclude 'stop'

        # assert len(undo_these_files) == len(original_filename)
        # Undo Rename
        for i in range(len(undo_these_files)):
            try:
                os.rename(undo_these_files[i], original_filename[i])
            except PermissionError:
                self._alert('PermissionError.\n'
                       'Make sure all files are closed.')
                pass
            except FileNotFoundError:
                self._alert('FileNotFound.\n' +
                       undo_these_files[i] +
                       ' has not been re-renamed.')

        # Rewrite abridged content to log
        os.chdir(homepath)
        openfile = open("log.txt", 'w')
        for el in content:
            openfile.write(el + '\n')
        openfile.close()

        # Check that pathname is updated in display
        self._pathname.set(working_dir)
        self.list_files()

    def _sb(self, msg):
        """Update Status_msg"""
        self._status_msg.set(msg)

    def ask_proceed(self, title='Renaming - Proceed?',
                    message='Do you wish to proceed?'):
        """Messagebox to pass bool to proceed with operation"""
        proceed = messagebox.askokcancel(
            title,
            message)
        return proceed

    def _alert(self, msg):
        """Popup Msg Box"""
        messagebox.showinfo(message=msg)

    def listbox_select(self, event):
        try:
            init_path = self._pathname.get()
            pathname = self.content._filelist_box.selection_get()
            add_pathname = str(self._pathname.get()) + "\\" + pathname
            self._pathname.set(add_pathname)
            if not self.check_dir():
                self._pathname.set(init_path)
            self.list_files()
        except:
            self._sb('Did not work')

    def updir(self):
        try:
            init_pathname = self._pathname.get()
            pathname = init_pathname.split('\\')
            newname = "\\".join(pathname[:-1])
            self._pathname.set(newname)
            if not self.check_dir():
                self._pathname.set(init_pathname)
            self.list_files()
        except:
            self._sb('Operation did not work')


if __name__ == "__main__":
    root = tk.Tk()
    root.title('File Renaming App')
    MainApp(root).pack(side="top", fill="both", expand=True, padx=5, pady=5)

    root.mainloop()