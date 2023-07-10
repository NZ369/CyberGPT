# flake8: noqa

PREFIX = """
You are working with a pandas dataframe in Python. The name of the dataframe is `df`.
You should use the tools below to answer the question posed of you:"""

MULTI_DF_PREFIX = """
You are working with {num_dfs} pandas dataframes in Python named df1, df2, etc. You 
should use the tools below to answer the question posed of you:"""

SUFFIX_NO_DF = """
Begin!
Question: {input}
{agent_scratchpad}"""

SUFFIX_WITH_DF = """
This is the result of `print(df.head())`:
{df_head}

Begin!
Question: {input}
{agent_scratchpad}"""

SUFFIX_WITH_MULTI_DF = """
This is the result of `print(df.head())` for each dataframe:
{dfs_head}

Begin!
Question: {input}
{agent_scratchpad}"""

PREFIX_FUNCTIONS = """
You are working with a pandas dataframe in Python. The name of the dataframe is `df`."""

MULTI_DF_PREFIX_FUNCTIONS = """
You are working with {num_dfs} pandas dataframes in Python named df1, df2, etc."""

FUNCTIONS_WITH_DF = """
This is the result of `print(df.head())`:
{df_head}"""

FUNCTIONS_WITH_MULTI_DF = """
This is the result of `print(df.head())` for each dataframe:
{dfs_head}"""


# New prompts for prompt switching
CODE_PLOT_SUFFIX_WITH_DF = """
Output only the python code for ploting the result, and not a description.  
The plot should be assigned to a matplotlib variable called 'fig', 
and you should not output 'plt.show()'.  Don't load any new data.  
Include labels on the x and y axes.
This is the result of printing rows from the inital dataframe:
{df_content}

Begin!
Question: {input}
{agent_scratchpad}"""


CODE_TABLE_SUFFIX_WITH_DF = """
Output only the python code, not a description.  Also, display
the results from printing your final pandas dataframe object.
This is the result of printing rows from the inital dataframe:
{df_content}

Begin!
Question: {input}
{agent_scratchpad}"""

DESC_SUFFIX_WITH_DF = """
Return a description of the results, not the intermediate code.
This is the result of printing rows from the inital dataframe:
{df_content}

Begin!
Question: {input}
{agent_scratchpad}"""


DESC_SUFFIX_NO_DF = """
Return a description of the results, not the intermediate code.
Question: {input}
{agent_scratchpad}
"""

CODE_PLOT_SUFFIX_NO_DF = """
Output only the python code for ploting the result, and not a description.  
The plot should be assigned to a matplotlib variable called 'fig', 
and you should not output 'plt.show()'.  Don't load any new data.  
Include labels on the x and y axes.
Question: {input}
{agent_scratchpad}
"""


CODE_TABLE_SUFFIX_NO_DF = """
Output only the python code, not a description.  Also, display
the results from printing your final pandas dataframe object.
Question: {input}
{agent_scratchpad}
"""


CODE_SUFFIX_WITH_MULTI_DF = """
Output only the python code, not a description.
This is the result of printing rows from each dataframe:
{df_content}

Begin!
Question: {input}
{agent_scratchpad}"""

DESC_SUFFIX_WITH_MULTI_DF = """
This is the result of printing rows from each dataframe:
{df_content}

Begin!
Question: {input}
{agent_scratchpad}"""
