from typing import List
import logging
from pathlib import Path

from langchain_core.language_models import BaseLLM
from .storage import StorageBase
from .prompts import summary_for_file_prompt, summary_for_directory_prompt
from .directory_list import DirectoryListingGenerator


class SummaryGenerator:
    '''
    Generator generates a summary of path or directory, using given LLM and stores it in the given store.

    It ignores files and directories starting with '.'.
    '''

    def __init__(self, llm: BaseLLM, store: StorageBase, ignore_patterns: List[str]) -> None:
        self.logger = logging.getLogger('.'.join((__name__, self.__class__.__name__)))
        self.store = store
        self.ignore_patterns = ignore_patterns
        self.llm = llm

    def generate(self, pathStr: str) -> None:
        '''
        Generate the summary and store it in the store.
        pathStr: Path to file or directory to generate summary of.
        '''

        path = Path(pathStr)
        if path.is_file():
            self._generate_for_file(path)
        elif path.is_dir():
            self._generate_for_dir(path)
        else:
            raise ValueError(f'Path {pathStr} should be an existing file or directory.')

    def _generate_for_dir(self, rootdir: Path) -> str:
        directory_list_generator = DirectoryListingGenerator(rootdir, self.ignore_patterns)
        submodules: list[tuple[str, str]] = []
        generated_summary = ''
        for dirpath, subdirs, filenames in directory_list_generator.generate():
            for filename in filenames:
                filepath = Path(dirpath, filename)
                submodules.append((str(filepath), self._generate_for_file(filepath)))

            for subdir in subdirs:
                subdirpath = str(Path(dirpath, subdir))
                submodules.append((subdirpath, self.store.get_summary(subdirpath, True)))

            prompt = summary_for_directory_prompt(str(dirpath), submodules)
            generated_summary = self.llm.invoke(prompt).removesuffix('<end_of_turn>')
            self.logger.debug('Generated summary for %s:\n%s\n-----\n', dirpath, generated_summary)
            self.store.store_summary(str(dirpath), generated_summary, True)
        return generated_summary

    def _generate_for_file(self, filepath: Path) -> str:
        contents = filepath.read_text()
        self.logger.debug('Read file %s:\n%s\n-----\n', filepath, contents)
        prompt = summary_for_file_prompt(file_path=str(filepath), file_contents=contents)
        generated_summary = self.llm.invoke(prompt).removesuffix('<end_of_turn>')
        self.logger.debug('Generated summary for %s:\n%s\n-----\n', filepath, generated_summary)
        self.store.store_summary(str(filepath), generated_summary, False)
        return generated_summary
