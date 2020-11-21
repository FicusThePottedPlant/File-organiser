import os
import shutil

from settings_for_bd import SecondForm


class OrganiseByFiles:
    def __init__(self, dir_path):
        self.directories = SecondForm().get_directories()
        new_direct = {'Другие': '', 'Папки': ''}
        try:  # If Python interpreter version below 3.9.X merge dict with old way
            self.directories |= new_direct
        except TypeError:
            self.directories = {**self.directories, **new_direct}
        self.to = dir_path
        self.type_of_files = ['.' + i.split('.')[-1] for i in os.listdir(self.to)]
        try:
            self.create_folders()
            self.organise_files()
            self.remaining_files()
            self.organise_folders()
        except shutil.Error:
            assert shutil.Error('Файл в папке открыт в другом приложении')

    @staticmethod
    def safe_move(file_path, out_dir):
        """Move files without overwriting on file with same file name
        :parameter file_path is path to the file
        :parameter out_dir is path to the new path of the file"""
        name = os.path.basename(file_path)
        if not os.path.exists(os.path.join(out_dir, name)):
            shutil.move(file_path, os.path.join(out_dir, name))
        else:
            base, extension = os.path.splitext(name)
            i = 1
            while os.path.exists(os.path.join(out_dir, f'{base}_{i}{extension}')):
                i += 1
            shutil.move(file_path, os.path.join(out_dir, f'{base}_{i}{extension}'))

    def create_folders(self):
        """create folders based on type of files"""
        c = 0
        for key in self.directories:
            for i in self.type_of_files:
                if i in self.directories[key] and key not in os.listdir(self.to):
                    os.mkdir(os.path.join(self.to, key))
                    c += 1
        if len(self.type_of_files) != c and 'Другие' not in os.listdir(self.to):
            os.mkdir(os.path.join(self.to, "Другие"))

    def organise_files(self):
        """organise files"""
        for file in os.listdir(self.to):
            if os.path.isfile(os.path.join(self.to, file)):
                src_path = os.path.join(self.to, file)
                for key in self.directories:
                    extension = self.directories[key]
                    if file.endswith(extension):
                        destination_path = os.path.join(self.to, key)
                        self.safe_move(src_path, destination_path)
                        break

    def remaining_files(self):
        """organise remaining files to folder 'Другие'"""
        for file in os.listdir(self.to):
            if os.path.isfile(os.path.join(self.to, file)):
                src_path = os.path.join(self.to, file)
                destination_path = os.path.join(self.to, "Другие")
                self.safe_move(src_path, destination_path)
                break

    def organise_folders(self):
        """organise folders in folder 'Папки'"""
        list_dir = os.listdir(self.to)
        organized_folders = [folder for folder in self.directories]
        for folder in list_dir:
            if folder not in organized_folders:
                src_path = os.path.join(self.to, folder)
                destination_path = os.path.join(self.to, "Папки")
                self.safe_move(src_path, destination_path)
