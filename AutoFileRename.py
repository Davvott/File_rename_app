import os
import re
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock


class AutoRenameLayout(BoxLayout):

    fullpath_name = StringProperty('D:')
    keyword_end = StringProperty('720p')
    split_chars = StringProperty('.')
    replace_phrase = StringProperty('')
    with_phrase = StringProperty("")
    _rootpath = StringProperty(os.path.abspath(os.path.curdir))

    def check_dir(self):
        """
        Checks pathname is a valid directory.
        """
        if os.path.exists(self.ids.text_label.text):
            self.ids.valid_path.text = "Directory exists"
            self.fullpath_name = self.ids.text_label.text
        else:
            self.ids.valid_path.text = "Directory does not exist"

    def list_files(self):
        """ Checks dir and calls file log to display box """
        self.check_dir()
        self.ids.display_files.text = self.display_file_log()

    def display_file_log(self):
        """ Creates itemised list of all files in dir. """
        log = []
        current_dir = self.fullpath_name
        try:
            for filename in os.listdir(current_dir):
                log.append(filename)
        except:
            log.append(self.fullpath_name)
        return "\n".join(log)

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
        """Regex driven phrase replacement
            Uses .format() method to insert variable into regex expression string
        Args:
            file_string: basename as string
        Returns:
            Formatted filename
        """
        replace_chars = self.replace_phrase.replace("*", ".")
        reg_phrase = r'{}'.format(replace_chars)
        regex = re.compile(reg_phrase)
        formatted_filename = regex.sub(self.with_phrase, file_string)
        return formatted_filename

    def rename_engine(self, string, is_a_dir=False):
        """ Main engine for rename.
        Args:
            string: The basename of file/dir
            is_a_dir: Boolean value for suffix sub
        Returns:
            Re-named basename
        """
        # Replace chars before split
        if self.replace_phrase == '':
            pass
        elif "*" in self.replace_phrase:
            string = self.replace_chars(string)
        else:
            string = string.replace(self.replace_phrase, self.with_phrase)

        # Split filename on multiple characters
        file_string = self.split_recursion(self.split_chars, string)
        file_name_list = file_string.split()

        # Index of keyword from file_name_list
        try:
            end_indice = file_name_list.index(self.keyword_end)
        except:
            end_indice = -2

        if not is_a_dir:
            file_suffix = file_name_list[-1]
            new_name = " ".join(file_name_list[:end_indice + 1]) + "." + file_suffix
        else:
            if self.keyword_end == "" or self.keyword_end not in file_string:
                new_name = " ".join(file_name_list)
            else:
                new_name = " ".join(file_name_list[:end_indice + 1])
        return new_name

    def file_rename(self, commit=False):
        """Iterates through dir, displaying possible rename.
        On Commit will rename and file log.
        Args:
            commit=False: Allows testing of renaming.
        Returns:
              Display of file changes, and os.path.rename()
        """
        log = []
        win_display = []

        # Test for individual file drop
        try:
            os.chdir(self.fullpath_name)
        except FileNotFoundError:
            return
        except NotADirectoryError:
            dirname, old_name = os.path.split(self.fullpath_name)
            os.chdir(dirname)
            new_name = self.rename_engine(str(old_name))
            win_display.append(new_name)
            win_display = '\n'.join(win_display)
            self.ids.display_files.text = win_display
            if commit:
                os.rename(old_name, new_name)
                log.append(old_name)
                log.append(str(new_name))
                log.append(dirname)
                self.log_write(log)
                return
            else:
                return

        # Iterate through file/folders in dir
        for filename in os.listdir(self.fullpath_name):
            # File dir name
            old_name = str(filename)
            is_a_dir = os.path.isdir(filename)

            # New name
            new_name = self.rename_engine(old_name, is_a_dir)
            win_display.append(str(new_name))
            if commit:
                try:
                    os.rename(filename, new_name)
                    log.append(old_name)
                    log.append(str(new_name))
                except PermissionError:
                    self._alert(old_name + ": Might be open or in use.\n"
                                "It has not been renamed.")

        # Display potential renaming
        win_display = '\n'.join(win_display)
        self.ids.display_files.text = win_display

        # Log dir name
        if commit:
            log.append(str(self.fullpath_name))
            self.log_write(log)

    def dir_rename(self, commit=False):
        """Called on dir name only.
        Args:
            commit=False:
        Returns:
            Renamed directory, and os.path.rename if commit.
        """
        if not os.path.isdir(self.fullpath_name):
            self.ids.display_files.text = "Not a directory."
            return
        dirname = os.path.dirname(self.fullpath_name)
        basename = os.path.basename(self.fullpath_name)

        os.chdir(dirname)
        log = []
        log_display = []
        old_name = str(basename)
        new_name = self.rename_engine(old_name, is_a_dir=True)

        log_display.append(str(new_name))

        if commit:
            try:
                os.rename(old_name, new_name)
                log.append(old_name)
                log.append(new_name)
                log.append(dirname)
                self.fullpath_name = os.path.join(dirname, new_name)
                self.log_write(log)
                self.list_files()
            except PermissionError:
                self._alert("Permission Error. File in use")
            finally:
                return
        log_display = '\n'.join(log_display)
        self.ids.display_files.text = log_display
        self.ids.dir_rename.text = log_display

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
        """ Looks for log.txt in cwd, iterates backwards through undoing
        filename changes. Limited working at the moment, for immediate undo.
        Needs to be updated for logfile in home dir.
        Calls self.list_files() to window display.
        """
        # Initialize arrays
        undo_these_files = []
        original_filename = []

        # Open/assign/close log file
        homepath = str(self._rootpath)
        try:
            os.chdir(homepath)
            filenames = open('log.txt', 'r')
        except FileNotFoundError:
            self._alert('File not found for Undo.')
            filenames.close()
            return
        content = [line.strip('\n') for line in filenames]
        filenames.close()

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
        self.list_files()

    def update_fields(self, dt):
        """Called every 1/30s to check for dropped file."""
        Window.bind(on_dropfile=self._on_file_drop)

    def _on_file_drop(self, window, file_path):
        """Assigns decoded file_path to self.fullpathname
            Calls list_files() to display window
            Requires 'unused' 'window' parameter to function correctly
        """
        self.fullpath_name = file_path.decode("utf-8")  # convert byte to string
        self.list_files()

    def _alert(self, msg):
        """Popup Msg box"""
        pass


class AutoFileRenameApp(App):
    def build(self):
        root = AutoRenameLayout()
        Clock.schedule_interval(root.update_fields, 1.0 / 10.0)
        return root


if __name__ == "__main__":
    AutoFileRenameApp().run()