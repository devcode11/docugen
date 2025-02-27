def summary_for_file_prompt(file_path: str, file_contents: str) -> str:
    """
    Get a formatted prompt to generate a summary for a code file.

    file_path: path of the file to generate summary of.
    file_contents: Code contents of the file to generate summary from.
    """
    _summary_for_file_prompt = '''\
INSTRUCTIONS:
* You are an expert software engineer, having good understanding of various programming languages and software design.
* You are given a file path and the code contents of the file.
* Generate a detailed summary in 100 words for the purpose of the code in the file.
* Use markdown to generate results.

<file_path>
{file_path}
</file_path>

<file_contents_start>
{file_contents}
</file_contents_end>
'''
    return _summary_for_file_prompt.format(file_path = file_path, file_contents = file_contents)

def summary_for_directory_prompt(module_path: str, submodules: list[tuple[str, str]]) -> str:
    """
    Get a prompt to generate summary for a module with submodules.

    module_path: Path of the parent module, to generate summary of.
    submodules: List of tuples, with each tuple containing submodule path and summary of the submodule.
    """
    _summary_for_directory_prompt = '''\
INSTRUCTIONS:
* You are an expert software engineer, having good understanding of various programming languages and software design.
* You are given the name of a parent module, with a list of sub-modules and a summary of what each sub-module does.
* Generate a detailed summary in 100 words for the purpose of the parent module, based on the summaries of submodules.
* Use markdown to generate results.

<parent_module_path>
{parent_module_path}
</parent_module_path>

<submodules>
{submodules_summary}
</submodules>
'''
    _submodule_summary_prompt_part = '''\
<submodule_path>{submodule_path}</submodule_path>
<submodule_summary>
{submodule_summary}
</submodule_summary>
'''
    submodules_summary = '\n'.join(
        _submodule_summary_prompt_part.format(submodule_path=sub[0], submodule_summary=sub[1])
        for sub in submodules)
    return _summary_for_directory_prompt.format(parent_module_path=module_path, submodules_summary=submodules_summary)
