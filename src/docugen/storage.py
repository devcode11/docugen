import pathlib
import logging
from abc import ABC, abstractmethod

class StorageBase(ABC):

    @abstractmethod
    def store_summary(self, path: str, summary: str, is_dir: bool) -> None:
        pass

    @abstractmethod
    def get_summary(self, path: str, is_dir: bool) -> str:
        pass


class FileStore(StorageBase):
    '''
    Store summaries in a hierarchical file structure. It uses special file `dir_file_name` to store summaries for directories.
    '''

    def __init__(self, rootdir: str, dir_file_name: str = '_dir_summary.md') -> None:
        '''
        args:
            rootdir:
                Root directory where generated summaries should be stored.
                If the directory does not exist, it will be created.
            dir_file_name:
                Special file used to store summaries for directories themselves.
                Each directory would contain one such file, with the overall summary for the directory.
        '''

        self.logger = logging.getLogger('.'.join((__name__, self.__class__.__name__)))
        rootdir = rootdir.strip()
        if not rootdir:
            raise ValueError('rootdir must be a directory path')
        root_path = pathlib.Path(rootdir)

        if not root_path.exists():
            self.logger.debug('Creating root directory %s', root_path)
            root_path.mkdir(parents = True, exist_ok = True)

        if not root_path.is_dir():
            raise ValueError(f'Could not find or create directory rootdir: {rootdir}')

        self.rootdir = root_path
        self.dir_file_name = dir_file_name

    def store_summary(self, path: str, summary: str, is_dir: bool) -> None:
        '''
        Store given summary text for this path.
        args:
            path: Path of the file or directory relative to root.
            summary: Summary to store.
            is_dir: Whether the given path is file or directory.
        '''
        path_obj = self._resolve_summary_file_path(path, is_dir)
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        path_obj.write_text(summary)

    def get_summary(self, path: str, is_dir: bool) -> str:
        '''
        Fetch stored summary text for this path.

        args:
            path: Path of the file or directory relative to root.
        '''
        path_obj = self._resolve_summary_file_path(path, is_dir)
        return path_obj.read_text()

    def _resolve_summary_file_path(self, path: str, is_dir: bool) -> pathlib.Path:
        if is_dir:
            return pathlib.Path(self.rootdir, path, self.dir_file_name)
        return pathlib.Path(self.rootdir, path)
