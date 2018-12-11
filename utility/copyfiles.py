#!/usr/bin/env python

import os
import pickle
import sys


class DirectoryReport:
    """
    After copying directory tree copied and already existing target filenames are saved as report in binary data.
    """
    report_filename = "copied_files_report.p"

    def __init__(self):
        self.copied_target_filenames = []
        self.existing_target_filenames = []

    def __repr__(self):
        return str(self.__dict__)

    def add_copied_target_filename(self, filename):
        self.copied_target_filenames.append(filename)

    def add_existing_target_filename(self, filename):
        self.existing_target_filenames.append(filename)

    def save_report(self):
        with open(self.report_filename, mode='wb') as file:
            file.write(pickle.dumps(self))

    @classmethod
    def load_report(cls):
        dr = None
        with open(cls.report_filename, mode='rb') as file:
            dr = pickle.load(file)
        return dr


class DirectoryCopy(DirectoryReport):

    """
    Directory tree of given source path is copied to target path considering already existing target files.
    """
    def copy_files(self, source_path='./../test/dir', target_path='./../test/dir2', write_report=False):
        # Report path
        self.source_path = source_path
        self.target_path = target_path

        print("Copy files from {} to {}\n".format(source_path, target_path))

        for dirname, dirnames, filenames in os.walk(source_path):
            """
            Handle all subdirectories first.
            """
            for subdirname in dirnames:
                source_joined_dirname = os.path.join(dirname, subdirname)
                target_joined_dirname = source_joined_dirname.replace(source_path, target_path)
                if not os.path.isdir(target_joined_dirname):
                    os.makedirs(target_joined_dirname)

            """
            Handle all filenames
            """
            for filename in filenames:
                source_joined_filename = os.path.join(dirname, filename)
                target_joined_filename = source_joined_filename.replace(source_path, target_path)
                with open(source_joined_filename, mode='r') as source_join_file:
                    source_joined_filecontent = source_join_file.readlines()
                    try:
                        # Write access only: Exclusive creation, fails if file exists
                        with open(target_joined_filename, mode='x') as target_joined_file:
                            target_joined_file.writelines(source_joined_filecontent)
                            self.add_copied_target_filename(target_joined_filename)
                    except FileExistsError:
                        self.add_existing_target_filename(target_joined_filename)

        if write_report:
            self.save_report()


if __name__ == '__main__':
    dc = DirectoryCopy()
    if len(sys.argv) == 3:
        source_path = sys.argv[1]
        target_path = sys.argv[2]
        dc.copy_files(source_path, target_path, write_report=True)
    else:
        dc.copy_files(write_report=True)
    print(dc.load_report())