#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import os
import shutil
from pathlib import Path
import zipfile

"""Copy Special exercise
"""


# +++your code here+++
# Write functions and modify main() to call them


class DuplicateSpecialFileFound(Exception):
    """
    Exception for when a duplicate special file is found in the specified directory or its subdirectories
    """

    def __init__(self, msg="A duplicate special file was found in the directory specified"):
        """
        Constructor function for the exception, accepts a message argument so the message to be shown can be customized
        """
        self.msg = msg


def check_duplicate_special_files(files):
    """
    Checks if a list of file paths contains files with the same file name
    :param files: A list containing file paths
    """
    file_list = []
    for f in files:
        file_comp = os.path.split(f)
        filename = file_comp[-1]
        if filename not in file_list:
            file_list.append(filename)
        elif filename in file_list:
            raise DuplicateSpecialFileFound()


def get_special_paths(folder):
    """
    Searches a folder or directory recursively for files that have a particular pattern in their filename
    :param folder: Directory to search in
    :return list: Contains the absolute path strings of files that match the __w__ pattern
    """
    matched_path_objects = list(Path(folder).resolve().rglob("*__*__*"))
    match_path_strings = list(map(os.fspath, matched_path_objects))
    check_duplicate_special_files(match_path_strings)
    return match_path_strings


def test_get_special_paths():
    """
    Test Function to test the get_special_paths function
    """
    # OS.path.join used here to get the proper absolute path to the test file regardless of system
    assert get_special_paths(r".\Test_Files") == [os.path.join(os.getcwd(), "Test_Files", "lorem__ipsum__.jpg")]


def copy_to(paths, folder):
    """
    Copies files from list of file paths to directory
    :param paths: List of file paths
    :param folder: Directory to write to
    """
    if not os.path.exists(folder):
        raise ValueError("Destination directory does not exist")
    for p in paths:
        shutil.copy(p, folder)


def test_copy_to():
    """
    Tests the copy_to function
    """
    copy_to(get_special_paths(r".\Test_Files"), r".\Test_Files\directory1")
    assert os.listdir(r".\Test_Files\directory1") == ["lorem__ipsum__.jpg"]


def zip_to(paths, zippath):
    """
    Creates a zip file of the filepaths specified in paths
    :param paths: List of file paths
    :param zippath: path to zipfile, including the name of the zipfile
    """
    zip_folder_name = os.path.splitext(zippath)[0]
    if not os.path.exists(zip_folder_name):
        os.mkdir(zip_folder_name)
    copy_to(paths, zip_folder_name)
    # shutil.make_archive(zippath, "zip", zip_folder_name)
    zip_handle = zipfile.ZipFile(zippath, "w", zipfile.ZIP_DEFLATED)
    zip_folder_path = Path(zip_folder_name)
    for file in zip_folder_path.rglob("*"):
        zip_handle.write(file, os.path.basename(file))
    zip_handle.close()
    if os.path.exists(zip_folder_name):
        shutil.rmtree(zip_folder_name)


def test_zip_to():
    """
    Tests that the zip_to function is functioning properly. Checks that the output file of zip_to has PK in its
    header, specifying a zip file
    :return:
    """
    zip_to(get_special_paths(r".\Test_Files"), r".\Test_Zip_File\test.zip")
    assert zipfile.is_zipfile(r".\Test_Zip_File\test.zip")


def create_test_files():
    """
    Creates the test files used to test the program
    """
    os.mkdir("Test_Files")
    os.mkdir(r"Test_Files\directory1")
    os.mkdir(r"Test_Zip_File")
    with open(r"Test_Files\__test_1.txt", "w") as test_1:
        pass
    with open(r"Test_Files\lorem__ipsum__.jpg", "w") as test_2:
        pass
    with open(r"Test_Files\test3.txt", "w") as test_3:
        pass


def remove_test_files():
    """
    This function helps remove the test files previously created to test the program
    """
    if os.path.exists("Test_Files") and os.path.isdir("Test_Files"):
        # Removing the test directory if it exists
        shutil.rmtree("Test_Files")
    if os.path.exists(r"Test_Files\directory1") and os.path.isdir(r"Test_Files\directory1"):
        shutil.rmtree(r"Test_Files\directory1")
    if os.path.exists(r"Test_Zip_File") and os.path.isdir(r"Test_Zip_File"):
        shutil.rmtree(r"Test_Zip_File")


def tests():
    create_test_files()
    test_get_special_paths()
    test_zip_to()
    test_copy_to()
    remove_test_files()


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    # +++your code here+++
    # Call your functions
    tests()
    dir_path = args[0]
    try:
        match_files = get_special_paths(dir_path)
        if todir:
            copy_to(match_files, todir)
        elif tozip:
            zip_to(match_files, tozip)
        else:
            for file in match_files:
                print(file)
    except FileNotFoundError as n:
        print("Invalid file specified")
    except ValueError as v:
        print(v.args[0])
    except DuplicateSpecialFileFound as d:
        print(d.msg)
    except OSError as e:
        print("File may be in use by the system")


if __name__ == "__main__":
    main()
