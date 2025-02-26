from typing import List
import logging
import pathlib

from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import BaseLLM
from .storage import StorageBase
from .prompts import summary_for_file_prompt


class Generator:
    '''
    Generator generates a summary of path or directory, using given LLM and stores it in the given store.

    It ignores files and directories starting with '.'.
    '''

    def __init__(self, llm: BaseLLM, store: StorageBase, ignore_dirs: List[str], ignore_files: List[str]) -> None:
        self.logger = logging.getLogger('.'.join((__name__, self.__class__.__name__)))
        self.store = store
        self.ignore_dirs = ignore_dirs
        self.ignore_files = ignore_files

        prompt = PromptTemplate.from_template(summary_for_file_prompt)
        self.chain = prompt | llm

    def generate(self, pathStr: str) -> None:
        '''
        Generate the summary and store it in the store.
        pathStr: Path to file or directory to generate summary of.
        '''

        path = pathlib.Path(pathStr)
        if path.is_file():
            self._generate_for_file(path)
        elif path.is_dir():
            self._generate_for_dir(path)
        else:
            raise ValueError(f'Path {pathStr} should be an existing file or directory.')

    def _generate_for_dir(self, rootdir: pathlib.Path) -> None:
        for dirpath, subdirs, filenames in rootdir.walk():
            subdirs[:] = [d for d in subdirs if not (d.startswith('.') or d in self.ignore_dirs)]
            for filename in filenames:
                if filename.startswith('.') or filename in self.ignore_files:
                    continue
                self._generate_for_file(pathlib.Path(dirpath, filename))

    def _generate_for_file(self, filepath: pathlib.Path) -> None:
        contents = filepath.read_text()
        self.logger.debug('Read file %s =>\n%s\n-----', filepath, contents)
        generated_summary = self.chain.invoke({'file_path': filepath, 'file_contents': contents}).removesuffix('<end_of_turn>')
        self.logger.debug('Generated summary for %s =>\n%s\n-----', filepath, generated_summary)
        self.store.store_summary(str(filepath), generated_summary)
