"""
tests for the python file
"""
import os
import subprocess
import sys
import tempfile
import unittest

# import custom python packages


class TestCli(unittest.TestCase):
    """
    tests for the CLI of the python file
    """

    def test_top_parser_help(self):
        """
        tests, if help of top parser can be called
        """

        result = os.system("python -m wahoomc -h")

        self.assertEqual(result, 0)

    def test_cli_help(self):
        """
        tests, if CLI help can be called
        """

        result = os.system("python -m wahoomc cli -h")

        self.assertEqual(result, 0)

    def test_gui_help(self):
        """
        tests, if GUI help can be called
        """

        result = os.system("python -m wahoomc gui -h")

        self.assertEqual(result, 0)

    def test_setup_skipped_before_argparse_exits(self):
        """
        --help and a missing sub-command exit before any user directory
        is created or anything is downloaded
        """
        for arguments, expected_returncode in ((['-h'], 0), ([], 2)):
            with tempfile.TemporaryDirectory() as home_dir:
                result = subprocess.run(
                    [sys.executable, '-m', 'wahoomc'] + arguments,
                    env=dict(os.environ, HOME=home_dir), capture_output=True,
                    check=False)

                self.assertEqual(expected_returncode, result.returncode)
                self.assertEqual([], os.listdir(home_dir))


if __name__ == '__main__':
    unittest.main()
