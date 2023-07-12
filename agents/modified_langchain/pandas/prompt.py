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
CHAT_HISTORY_SUFFIX = """
Begin!
{chat_history}
Question: {input}
{agent_scratchpad}
"""

NO_CHAT_HISTORY_SUFFIX = """
Begin!
Question: {input}
{agent_scratchpad}
"""


CODE_PLOT_SUFFIX_WITH_DF = """
Output ONLY the python code for ploting the result, and NOT a description.  
The plot should be assigned to a matplotlib variable called 'fig', 
and you should not output 'plt.show()'.  Don't use pd.read_csv to load new data,
use only the existing variable 'df'.
This is the result of printing rows from the inital dataframe:
{df_content}

"""


CODE_TABLE_SUFFIX_WITH_DF = """
Store the final result into a table 'df_output', print it without the index, and return what was
printed statement exactly with "```" at the start and at the end of the text.  Don't display
two copies of "```" at the start of the block.
This is the result of printing rows from the inital dataframe:
{df_content}

"""

DESC_SUFFIX_WITH_DF = """
Return a description of the results, not the intermediate code.
This is the result of printing rows from the inital dataframe:
{df_content}

"""


DESC_SUFFIX_NO_DF = """
Return a description of the results, not the intermediate code.

"""

CODE_PLOT_SUFFIX_NO_DF = """
Output only the python code for ploting the result, and not a description.  
The plot should be assigned to a matplotlib variable called 'fig', 
and you should not output 'plt.show()'.  Don't use pd.read_csv to load new data,
use only the existing variable 'df'. 

"""


CODE_TABLE_SUFFIX_NO_DF = """
At the end, print the final table you created.

"""

CODE_SUFFIX_NO_DF = """
Output only the python code, not a description.

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
