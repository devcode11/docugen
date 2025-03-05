# Docugen
Generate documentation of a project using LLMs

# How it works
- It is a CLI application which takes a project root directory as input.
- It then traverses the root directory and subdirectories, and generates a summary of each file using LLM.
  - To generate summary of file, it passes file path and file contents to the LLM.
- It also generates a summary for each directory, using the summaries of direct children of the directory.
  - It passes a list of sub-directory / file paths and their generated summaries to the LLM.
- It excludes any files ignored by git.
- It also ignores some extra files, like LICENSE, uv.lock, etc. while generating summaries.

## LLM support
- It currently supports [llamafile](https://github.com/Mozilla-Ocho/llamafile) and [Ollama](https://github.com/ollama/ollama) for LLM options.

## Extra requirements
- It assumes the project directory to be a git repository, and requires git command to be available.

# Usage

```bash
$ uv run docugen --help
Usage: docugen [OPTIONS]

  Generate project documentation using LLMs

Options:
  --project-path TEXT  Path to project root directory  [required]
  --output-path TEXT   Path to output root directory  [default: .docugen]
  --llm-tool TEXT      Supported LLM tools - llamafile, ollama
                       Syntax:
                       * --llm-tool llamafile
                       * --llm-tool ollama=<model-name>  [default: llamafile]
  --debug              Enable debug logging
  --help               Show this message and exit.
```

## Example
```bash
uv run docugen --project-path .
```
