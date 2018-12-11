import os
import shutil
import unittest
from utility import copyfiles as cf

class TestCopyDirectory(unittest.TestCase):

    report_filename = "copied_files_report.p"
    copied_target_filenames = ['./dir2/file1.txt', './dir2/sub/file2.txt']
    existing_target_filenames = []

    def setUp(self):
        # Cleanup directories
        if os.path.exists(self.report_filename):
            os.remove(self.report_filename)
        shutil.rmtree("./dir2", ignore_errors=True)

        self.dc = cf.DirectoryCopy()


    def test_copy_files(self):
        self.dc.copy_files("./dir", "./dir2")

        self.assertListEqual(self.copied_target_filenames, self.dc.copied_target_filenames)
        self.assertListEqual(self.existing_target_filenames, self.dc.existing_target_filenames)
        self.assertTrue(not os.path.isfile(self.report_filename))


    def test_write_report(self):
        self.dc.copy_files("./dir", "./dir2", write_report=True)

        self.assertTrue(os.path.isfile(self.report_filename))
        print(self.dc.load_report())


if __name__ == "__main__":
    unittest.main()
