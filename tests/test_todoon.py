import os
import unittest

import todo_or_not.todo_check as td


class TestTodoon(unittest.TestCase):

    def setUp(self):
        os.environ["DEBUG"] = 'True'

        self.other_files_list = [
            os.path.join("tests", "resources", "a.txt"),
            os.path.join("tests", "resources", "b.txt"),
            os.path.join("tests", "resources", "c.txt")
        ]

        self.specific_files_list = [
            os.path.join("tests", "resources", "a.txt"),
            os.path.join("tests", "resources", "b.txt"),
            os.path.join("tests", "resources", "c.txt"),
            os.path.join("tests", "resources", "specific_files")
        ]

    def test_todoon_standard_succeeds_with_no_todos(self):
        safe_dir = os.path.join("tests", "resources", "no_todos")
        old_dir = os.getcwd()
        os.chdir(safe_dir)

        td.todoon(verbose=True, print_mode=True)

        os.chdir(old_dir)

    def test_todoon_standard_fails_when_finds_todos(self):
        with self.assertRaises(SystemExit) as context:
            td.todoon(verbose=True)

        self.assertEqual(context.exception.code, 1)

    def test_todoon_silent_pushes_environment_variables(self):
        # Set up
        safe_dir = os.path.join("tests", "resources", "specific_files")
        old_dir = os.getcwd()
        os.chdir(safe_dir)

        td.todoon(verbose=True, silent=True)

        TODOON_STATUS = os.environ.get("TODOON_STATUS")
        TODOON_PROGRESS = os.environ.get("TODOON_PROGRESS")
        TODOON_FILES_SCANNED = os.environ.get("TODOON_FILES_SCANNED")
        TODOON_TODOS_FOUND = os.environ.get("TODOON_TODOS_FOUND")
        TODOON_FIXMES_FOUND = os.environ.get("TODOON_FIXMES_FOUND")
        TODOON_ENCODING_ERRORS = os.environ.get("TODOON_ENCODING_ERRORS")
        TODOON_ISSUES_GENERATED = os.environ.get("TODOON_ISSUES_GENERATED")
        TODOON_DUPLICATE_ISSUES_AVOIDED = os.environ.get("TODOON_DUPLICATE_ISSUES_AVOIDED")

        assert TODOON_STATUS == "finished"
        assert TODOON_PROGRESS == "100.0"
        assert int(TODOON_FILES_SCANNED) == 2
        assert int(TODOON_TODOS_FOUND) == 2
        assert int(TODOON_FIXMES_FOUND) == 0
        assert int(TODOON_ENCODING_ERRORS) == 0
        assert TODOON_ISSUES_GENERATED == "0"
        assert TODOON_DUPLICATE_ISSUES_AVOIDED == "0"

        # Tear down
        os.chdir(old_dir)

    def test_todoon_standard_fails_without_todo_ignore(self):
        with open(".todo-ignore", "r") as _before:
            before = _before.read()
        os.remove(".todo-ignore")

        with self.assertRaises(SystemExit) as context:
            td.todoon()

        self.assertEqual(context.exception.code, 1)

        with open(".todo-ignore", "x") as _after:
            _after.write(before)

    def test_todoon_silent_passes(self):
        td.todoon(verbose=True, silent=True)

    def test_todoon_with_print_and_fail_on_closed_duplicate(self):
        td.todoon(verbose=True, silent=True, fail_closed_duplicates=True)

    def test_todoon_runs_when_forced(self):
        with open(".todo-ignore", "r") as _before:
            before = _before.read()

        os.remove(".todo-ignore")

        td.todoon(verbose=True, silent=True, force=True)

        with open(".todo-ignore", "x") as _after:
            _after.write(before)

    def test_todoon_takes_individual_targets(self):
        td.todoon(verbose=True, silent=True, files=self.specific_files_list)

        self.assertEqual(os.environ.get("TODOON_FILES_SCANNED"), '6')

    def test_todoignore_uses_wildcards(self):
        # Set up
        safe_dir = os.path.join("tests", "resources", "wildcard_test")
        old_dir = os.getcwd()
        os.chdir(safe_dir)

        # Run util
        td.todoon()

        # Check results
        files_scanned = os.environ["TODOON_FILES_SCANNED"]

        self.assertEqual(files_scanned, '8')

        # Tear down
        os.chdir(old_dir)

    def test_issue_mode(self):
        # Set up to check todoon
        os.environ["GITHUB_REPOSITORY"] = "Start-Out/todo-or-not"
        os.environ["GITHUB_REF_NAME"] = "branch"
        os.environ["GITHUB_TRIGGERING_ACTOR"] = "pytest"
        os.environ["MAXIMUM_ISSUES_GENERATED"] = "1"

        # Set up
        safe_dir = os.path.join("tests", "resources", "no_todos")
        old_dir = os.getcwd()
        rel = os.path.relpath(safe_dir)
        os.chdir(rel)

        td.todoon(print_mode=False, silent=True)

        # Tear down
        del os.environ["GITHUB_REPOSITORY"]
        del os.environ["GITHUB_REF_NAME"]
        del os.environ["GITHUB_TRIGGERING_ACTOR"]
        del os.environ["MAXIMUM_ISSUES_GENERATED"]
        os.chdir(old_dir)

    def test_issue_mode_exceed_maximum_issues(self):
        # Set up to check todoon
        os.environ["GITHUB_REPOSITORY"] = "Start-Out/todo-or-not"
        os.environ["GITHUB_REF_NAME"] = "branch"
        os.environ["GITHUB_TRIGGERING_ACTOR"] = "pytest"
        os.environ["MAXIMUM_ISSUES_GENERATED"] = "1"

        # Set up
        safe_dir = os.path.join("tests", "resources", "specific_files")
        old_dir = os.getcwd()
        rel = os.path.relpath(safe_dir)
        os.chdir(rel)

        with self.assertRaises(SystemExit) as context:
            td.todoon(print_mode=False, silent=True)

        # Tear down
        del os.environ["GITHUB_REPOSITORY"]
        del os.environ["GITHUB_REF_NAME"]
        del os.environ["GITHUB_TRIGGERING_ACTOR"]
        del os.environ["MAXIMUM_ISSUES_GENERATED"]
        os.chdir(old_dir)

    def test_issue_mode_with_fail_on_closed(self):
        td.todoon(print_mode=False, fail_closed_duplicates=True, silent=True)

    def test_issue_collection_live(self):
        # Set up to check todoon
        os.environ["DEBUG"] = 'False'
        os.environ["GITHUB_REPOSITORY"] = "Start-Out/todo-or-not"
        os.environ["GITHUB_REF_NAME"] = "branch"
        os.environ["GITHUB_TRIGGERING_ACTOR"] = "pytest"

        # Set up
        safe_dir = os.path.join("tests", "resources", "no_todos")
        old_dir = os.getcwd()
        rel = os.path.relpath(safe_dir)
        os.chdir(rel)

        td.todoon(print_mode=False, silent=True)

        # Tear down env variables
        os.environ["DEBUG"] = 'True'
        del os.environ["GITHUB_REPOSITORY"]
        del os.environ["GITHUB_REF_NAME"]
        del os.environ["GITHUB_TRIGGERING_ACTOR"]

        # Tear down
        os.chdir(old_dir)

    def test_environment_variables(self):

        # Set up
        safe_dir = os.path.join("tests", "resources", "no_todos")
        old_dir = os.getcwd()
        rel = os.path.relpath(safe_dir)
        os.chdir(rel)

        # Set up to check todoon
        os.environ["DEBUG"] = 'False'
        os.environ["MAXIMUM_ISSUES_GENERATED"] = "invalid"
        os.environ["PERTINENT_LINE_LIMIT"] = "invalid"

        td.todoon(print_mode=False, silent=True)

        assert td.get_max_issues() == 8
        assert td.get_pertinent_line_limit() == 8

        # Tear down env variables
        os.environ["DEBUG"] = 'True'

        del os.environ["MAXIMUM_ISSUES_GENERATED"]
        del os.environ["PERTINENT_LINE_LIMIT"]

        os.chdir(old_dir)


if __name__ == '__main__':
    unittest.main()
