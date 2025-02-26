summary_for_file_prompt = '''
INSTRUCTIONS:
* You are a smart software engineer, having good understanding of various programming languages and software design.
* You are given a file path and the code contents of the file. The file is part of a larger project.
* Generate a summary in 50-100 words for the code in the file. Use markdown to display result.

<file_path>
{file_path}
</file_path>

<file_contents_start>
{file_contents}
</file_contents_end>

Here is the summary in markdown, in bullet points -
'''
