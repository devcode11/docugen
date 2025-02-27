from pathlib import Path
from typing import Iterator

class DirectoryListingGenerator:
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


    def generate(self) -> Iterator[tuple[Path, list[Path], list[Path]]]:
        """
        Recursively generates tuples of (directory name, list of subdirectories, list of filenames).

        All subdirectories will be generated before generating a directory.
        So rootdir will be generated last.

        Similar to os.walk() with `topdown` set to False, but supports ignoring sub-directories and files.
        """
        yield from self._generate(self.topdir)

    def _generate(self, currentdir: Path) -> Iterator[tuple[Path, list[Path], list[Path]]]:
        gitignore_patterns = []
        gitignore_file = currentdir / '.gitignore'
        if gitignore_file.is_file():
            gitignore_patterns = [pat.strip() for pat in gitignore_file.read_text().splitlines() if pat.strip()]

        subdirs, files = [], []
        for child in currentdir.iterdir():
            if self._is_ignored(child, gitignore_patterns):
                continue
            if child.is_dir():
                yield from self._generate(child)
                subdirs.append(child)
            if child.is_file():
                files.append(child)

        yield currentdir, subdirs, files

    def _is_ignored(self, path: Path, ignore_patterns: list[str]) -> bool:
        if path.match('.*'):
            return True
        for pat in ignore_patterns:
            if path.match(pat):
                return True
        for pat in self.custom_ignore_patterns:
            if path.match(pat):
                return True
        return False
