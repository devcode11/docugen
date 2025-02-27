from pathlib import Path
import subprocess

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


    def generate_files(self) -> list[Path]:
        """
        Generate a list of files (without directories) in the tree rooted at `topdir`.
        It takes .gitignore files and `custom_ignore_patterns` into account, and skips files matching these patterns.

        Behind the scenes, it uses git to generate this list.
        """
        self._generated_files = self._generate_file_list_with_git()
        return self._generated_files

    def generate_dirs(self) -> list[Path]:
        """
        Generate a list of directories and subdirectories in the tree rooted at `topdir`, based on the generated files earlier.
        It takes .gitignore files and `custom_ignore_patterns` into account, and skips files matching these patterns.

        If files has not been generated earlier using `generate_files`, it returns an empty list.
        """
        if not self._generated_files:
            return []
        self._generated_dirs = self._generate_dirs_from_file_list()
        return self._generated_dirs

    def _generate_file_list_with_git(self) -> list[Path]:
        git_cmd = 'git ls-files --cached --others --full-name --exclude-standard'
        git_cmd_run = subprocess.run(git_cmd.split(), stdout=subprocess.PIPE, check=True, cwd=self.topdir)
        files = [Path(file) for file in git_cmd_run.stdout.decode().splitlines()]
        files = [file for file in files if not self._is_ignored(file)]
        return files

    def _generate_dirs_from_file_list(self) -> list[Path]:
        subdirs = list(set([p.parent for p in self._generated_files if not self._is_ignored(p.parent)]))
        subdirs.sort(key=lambda p: str(p).count('/'), reverse=True)
        return subdirs

    def _is_ignored(self, path: Path) -> bool:
        if path.match('.*'):
            return True
        for pat in self.custom_ignore_patterns:
            if path.match(pat):
                return True
        return False
