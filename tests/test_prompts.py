from unittest import TestCase
from docugen import prompts

class FilePromptTests(TestCase):
    def setUp(self):
        self.file_path = 'abc/def/file1.py'
        self.file_contents = 'This is file1 contents'

    def test_prompt_contains_file_path(self):
        prompt = prompts.summary_for_file_prompt(file_path=self.file_path, file_contents=self.file_contents)
        self.assertRegex(prompt, fr'\b{self.file_path}\b')

    def test_prompt_contains_file_contents(self):
        prompt = prompts.summary_for_file_prompt(file_path=self.file_path, file_contents=self.file_contents)
        self.assertRegex(prompt, fr'\b{self.file_contents}\b')


class DirectoryPromptTests(TestCase):
    def setUp(self):
        self.dir_path = 'abc/def/dir1'
        self.submodules = []
        for i in range(5):
            self.submodules.append((f'{self.dir_path}/file{i}.py', f'Summary of file{i}'))
        for i in range(5, 10):
            self.submodules.append((f'{self.dir_path}/subdir{i}', f'Summary of subdir{i}'))

    def test_prompt_contains_directory_path(self):
        prompt = prompts.summary_for_directory_prompt(module_path=self.dir_path, submodules=self.submodules)
        self.assertRegex(prompt, fr'\b{self.dir_path}\b')

    def test_prompt_contains_submodules_paths(self):
        prompt = prompts.summary_for_directory_prompt(module_path=self.dir_path, submodules=self.submodules)
        for m in self.submodules:
            self.assertRegex(prompt, fr'\b{m[0]}\b')

    def test_prompt_contains_submodules_summaries(self):
        prompt = prompts.summary_for_directory_prompt(module_path=self.dir_path, submodules=self.submodules)
        for m in self.submodules:
            self.assertRegex(prompt, fr'\b{m[1]}\b')
