import sys
import logging
import click

from langchain_community.llms.llamafile import Llamafile
from .storage import FileStore
from .constants import IgnoreDirs, IgnoreFiles
from .summary import Generator


logger = logging.getLogger(__name__)

@click.command()
@click.option(
    "--project-path",
    required=True,
    prompt="Path to project root directory",
    help="Path to project root directory",
)
@click.option(
    "--output-path",
    help="Path to output root directory",
    default='.docugen'
)
@click.option("--debug", help="Enable debug logging", is_flag=True)
def main(project_path: str, output_path: str, debug: bool) -> None:
    """
    Main entrypoint of the CLI.
    """

    logging.basicConfig(level=(logging.DEBUG if debug else logging.INFO))
    output_path = output_path.strip() if output_path.strip() else '.docugen'

    logger.debug('args: %s', locals())

    llm = Llamafile()
    store = FileStore(output_path)
    generator = Generator(llm, store, IgnoreDirs, IgnoreFiles)

    logger.debug('Generating documenatation for project path %s in output path %s', project_path, output_path)

    generator.generate(project_path)


if __name__ == '__main__':
    sys.exit(main())
