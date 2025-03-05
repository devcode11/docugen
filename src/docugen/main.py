import sys
import logging
import click

from langchain_community.llms.llamafile import Llamafile
from langchain_ollama import OllamaLLM
from langchain_core.language_models import BaseLLM
from .storage import FileStore
from .constants import IgnorePatterns
from .summary import SummaryGenerator


def get_llm_tool(llm_tool: str) -> BaseLLM:
    if llm_tool == 'llamafile':
        return Llamafile()
    elif llm_tool.startswith('ollama='):
        return OllamaLLM(model=llm_tool.removeprefix('ollama='))
    raise ValueError(f'LLM tool {llm_tool} is not supported')

logger = logging.getLogger(__name__)

@click.command(help='Generate project documentation using LLMs')
@click.option(
    "--project-path",
    required=True,
    prompt="Path to project root directory",
    help="Path to project root directory",
)
@click.option(
    "--output-path",
    help="Path to output root directory",
    default='.docugen',
    show_default=True
)
@click.option(
    "--llm-tool",
    help="""\
\b
Supported LLM tools - llamafile, ollama
Syntax:
* --llm-tool llamafile
* --llm-tool ollama=<model-name>
""",
    default='llamafile',
    show_default=True
)
@click.option("--debug", help="Enable debug logging", is_flag=True)
def main(project_path: str, output_path: str, llm_tool: str, debug: bool) -> None:
    """
    Main entrypoint of the CLI.
    """

    logging.basicConfig(level=(logging.DEBUG if debug else logging.INFO))
    output_path = output_path.strip() if output_path.strip() else '.docugen'

    logger.debug('args: %s', locals())

    llm = get_llm_tool(llm_tool)
    store = FileStore(output_path)
    generator = SummaryGenerator(llm, store, IgnorePatterns)

    logger.debug('Generating documenatation for project path %s in output path %s', project_path, output_path)

    generator.generate(project_path)


if __name__ == '__main__':
    sys.exit(main())
