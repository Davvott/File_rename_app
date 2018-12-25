import os
import re
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock

# One file at a time? Or one folder at a time? --- () to handle both
# Prompt Split_char default='.'
# Prompt Keyword End
# Final Button to Commit Changes
# TODO: Add PopUp functionality for Instructions; Error; COMMIT!
# TODO: Add '*' replace any char() functionality. e.g. 'E0*'
# TODO: set log.txt dirname to save to home folder
# TODO: Add '\n' to log.txt write; write_log()


class AutoRenameLayout(BoxLayout):

    fullpath_name = StringProperty('D:')
    keyword_end = StringProperty('720p')
    split_chars = StringProperty('.')
    replace_phrase = StringProperty('')
    with_phrase = StringProperty("")

    def check_dir(self):
        if os.path.exists(self.ids.text_label.text):
            self.ids.valid_path.text = "Directory exists"
            self.fullpath_name = self.ids.text_label.text
        else:
            self.ids.valid_path.text = "Directory does not exist"

    def list_files(self):
        self.check_dir()
        self.ids.display_files.text = self.display_file_log()

    def display_file_log(self):
        log = []
        current_dir = self.fullpath_name
        try:
            for filename in os.listdir(current_dir):
                log.append(filename)
        except:
            log.append(self.fullpath_name)
        return "\n".join(log)

    # All characters in TextInput to a space
    def split_recursion(self, split_chars, string):
        if split_chars == '':
            return string
        else:
            filename = " ".join(string.split(split_chars[0]))
            return self.split_recursion(split_chars[1:], filename)

    def replace_chars(self, file_string):

        replace_chars = self.replace_phrase.replace("*", ".")
        reg_phrase = r'{}'.format(replace_chars)
        regex = re.compile(reg_phrase)
        formatted_filename = regex.sub(self.with_phrase, file_string)
        return formatted_filename

    def rename_engine(self, string, is_a_dir=False):

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

    # The engine. More work to do.
    def file_rename(self, commit=False):
        log = []
        win_display = []

        # Test for individual file drop
        try:
            os.chdir(self.fullpath_name)
        except NotADirectoryError:
            dirname, old_name = os.path.split(self.fullpath_name)
            os.chdir(dirname)
            new_name = self.rename_engine(str(old_name))
            win_display.append(new_name)
            win_display = '\n'.join(win_display)
            self.ids.display_files.text = win_display
            if commit:
                log.append(old_name)
                log.append(str(new_name))
                os.rename(old_name, new_name)
                log.append(os.path.join(dirname, new_name))
                self.log_write(log)
                return
            else:
                return

        # Iterate through file/folders in dir
        for filename in os.listdir(self.fullpath_name):
            # File dir name
            old_name = str(filename)
            is_a_dir = False
            # Test for dir
            if os.path.isdir(filename):
                is_a_dir = True

            # New name
            new_name = self.rename_engine(old_name, is_a_dir)
            win_display.append(str(new_name))
            if commit:
                log.append(old_name)
                log.append(str(new_name))
                os.rename(filename, new_name)

        # Display potential renaming
        win_display = '\n'.join(win_display)
        self.ids.display_files.text = win_display

        # Log dir name
        if commit:
            log.append(str(self.fullpath_name))
            self.log_write(log)

    def log_write(self, log):
        openfile = open("log.txt", "a")
        for el in log:
            openfile.write(el + '\n')
        openfile.write('stop\n')
        openfile.close()

    # Split dir and base name for rename
    def dir_rename(self, commit=False):

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

        # update log_display
        log_display.append(str(new_name))

        if commit:
            log.append(old_name)
            log.append(new_name)
            log.append(dirname)  # For undo() loop
            os.rename(old_name, new_name)
            self.fullpath_name = os.path.join(dirname, new_name)
            self.log_write(log)

        log_display = '\n'.join(log_display)
        self.ids.display_files.text = log_display
        self.ids.dir_rename.text = log_display

    def undo_rename(self):
        # Initialize arrays
        undo_these_files = []
        original_filename = []

        # Open/assign/close log file
        # TODO: need to make sure we find correct log file and 'stop's are correct
        filenames = open('log.txt', 'r')
        content = [line.strip('\n') for line in filenames]
        filenames.close()

        content.pop()  # .pop('stop')
        working_dir = content.pop()
        os.chdir(working_dir)

        lastindex = None
        # Reverse Iterate -- Old name, new name ... dir, stop ...
        for i in range(len(content) - 1, -1, -1):
            if content[i] == 'stop':
                lastindex = i + 1  # include 'stop'
                break
            if i % 2 == 1:  # odd nums
                undo_these_files.append(content[i])
            else:
                original_filename.append(content[i])

        content = content[:lastindex]

        # Write abridged content to log
        openfile = open("log.txt", 'w')
        for el in content:
            openfile.write(el + '\n')
        openfile.close()

        assert len(undo_these_files) == len(original_filename)
        # Undo Rename
        for i in range(len(undo_these_files)):
            try:
                os.rename(undo_these_files[i], original_filename[i])
            except Exception:
                pass
        self.list_files()

    def update_fields(self, dt):
        Window.bind(on_dropfile=self._on_file_drop)

    def _on_file_drop(self, window, file_path):  # needs window, parameter
        # print(file_path)
        self.fullpath_name = file_path.decode("utf-8")  # convert byte to string
        self.list_files()


class AutoFileRenameApp(App):
    def build(self):
        root = AutoRenameLayout()
        # root.init_text()
        Clock.schedule_interval(root.update_fields, 1.0 / 10.0)
        return root


if __name__ == "__main__":
    AutoFileRenameApp().run()