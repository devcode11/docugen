from pathlib import Path
from typing import Iterator, Any
import subprocess

class DirectoryTreeGenerator:
    """
    Reccursively generate list of files and sub-directories from a root directory
    respecting gitignore as well as custom ignore patterns.

    """

    def __init__(self, topdir: Path, custom_ignore_patterns: list[str] = []) -> None:
        """
        args:
            topdir: Directory tree root
            custom_ignore_patterns: Custom ignore patterns in addition to .gitignore files.
        """
        if not topdir.is_dir():
            raise ValueError('')
        self.topdir = topdir
        self.custom_ignore_patterns = custom_ignore_patterns
        self.files: list[Path] = []

    def walk(self) -> Iterator[tuple[Path, list[Path], list[Path]]]:
        """
        Generates tuples of (dirpath, subdirs, filenames) in a bottom up fashion.
        Based on files known to git, and custome ignore patterns.
        """
        files = self._generate_file_list_with_git()
        dir_tree = _DirTree(self.topdir)
        for file in files:
            dir_tree.add_path(file)

        yield from dir_tree.dfs()

    def _generate_file_list_with_git(self) -> list[Path]:
        git_cmd = 'git ls-files --cached --others --full-name --exclude-standard'
        git_cmd_run = subprocess.run(git_cmd.split(), stdout=subprocess.PIPE, check=True, cwd=self.topdir)
        files = [Path(file) for file in git_cmd_run.stdout.decode().splitlines()]
        files = [file for file in files if not self._is_ignored(file)]
        return files

    def _is_ignored(self, path: Path) -> bool:
        if any(part.startswith('.') for part in path.parts):
            return True
        for pat in self.custom_ignore_patterns:
            if path.match(pat):
                return True
        return False

type _Node = dict[str, Any]

_FILE_MARKER = 'FILE_MARKER'

class _DirTree:
    def __init__(self, root: Path):
        self.root: _Node = dict()
        self.root_path: Path = root

    def add_path(self, path: Path) -> None:
        temp = self.root
        for part in path.parts[:-1]:
            if part not in temp:
                temp[part] = dict()
            temp = temp[part]
        temp[path.parts[-1]] = _FILE_MARKER

    def dfs(self) -> Iterator[tuple[Path, list[Path], list[Path]]]:
        yield from self._dfs(self.root, self.root_path)

    def _dfs(self, curr: _Node, parent: Path) -> Iterator[tuple[Path, list[Path], list[Path]]]:
        files: list[Path] = []
        subdirs: list[Path] = []
        for k, v in curr.items():
            path = Path(parent, k)
            if v == _FILE_MARKER:
                files.append(path)
            else:
                yield from self._dfs(v, path)
                subdirs.append(path)
        yield parent, subdirs, files

