"""Agent for working with pandas objects."""
from typing import Any, Dict, List, Optional, Tuple

from langchain.agents.agent import AgentExecutor, BaseSingleActionAgent

from langchain.agents.mrkl.base import ZeroShotAgent

from langchain.agents.types import AgentType
from langchain.tools.base import BaseTool
from langchain.base_language import BaseLanguageModel
from langchain.callbacks.base import BaseCallbackManager
from langchain.chains.llm import LLMChain
from langchain.schema import BasePromptTemplate
from langchain.tools.python.tool import PythonAstREPLTool

from langchain.agents import initialize_agent
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents.chat.base import ChatAgent # AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION
from langchain.agents.conversational_chat.base import ConversationalChatAgent # AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION


from agents.modified_langchain.pandas.prompt import *
from chains.pandas_multi_prompt import PandasMultiPromptChain


valid_types = [
    AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION
]

def _build_multi_prompt(
        dfs: List[Any],
        include_df_content : bool, 
        df_rows: Optional[List[List[int]]] = None,
        tools : Optional[List[BaseTool]] = [], 
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        input_variables : Optional[List[str]] = None,
        number_of_head_rows: int = 5,      
):
    num_dfs = len(dfs)
    if input_variables is None:
        input_variables = ["input", "agent_scratchpad", "num_dfs"]
        if include_df_content:
            input_variables += ["df_content"]

    prompt = ZeroShotAgent.create_prompt(
        tools, prefix=prefix, suffix=suffix, input_variables=input_variables
    )

    partial_prompt = prompt.partial()
    if "df_content" in input_variables:
        if df_rows is None:
            dfs_content = "\n\n".join([d.head(number_of_head_rows).to_markdown() for d in dfs])
        else:
            dfs_content = "\n\n".join([d.iloc[df_rows[i]].to_markdown() for i, d in enumerate(dfs)])


        partial_prompt = partial_prompt.partial(num_dfs=str(num_dfs), dfs_head=dfs_content)
    if "num_dfs" in input_variables:
        partial_prompt = partial_prompt.partial(num_dfs=str(num_dfs))

    return partial_prompt

def _get_multi_prompt_template(
    dfs: List[Any],
    df_rows: Optional[List[List[int]]] = None,
    input_variables: Optional[List[str]] = None,
    include_df_in_prompt: Optional[bool] = True,
    number_of_head_rows: int = 5,
) -> Tuple[BasePromptTemplate, List[PythonAstREPLTool]]:
    num_dfs = len(dfs)
    if df_rows is not None:
        if len(df_rows) != num_dfs:
            raise ValueError(f"Number of row selections does not match number of dfs {len(df_rows)} != num_dfs")

        include_df_content = True
        desc_suffix = DESC_SUFFIX_WITH_MULTI_DF
        code_suffix = CODE_SUFFIX_WITH_MULTI_DF
    elif include_df_in_prompt:
        include_df_content = True
        desc_suffix = DESC_SUFFIX_WITH_MULTI_DF
        code_suffix = CODE_SUFFIX_WITH_MULTI_DF
    else:
        include_df_content = False
        desc_suffix = DESC_SUFFIX_NO_DF
        code_suffix = CODE_SUFFIX_NO_DF

    if input_variables is None:
        input_variables = ["input", "agent_scratchpad", "num_dfs"]
        if include_df_content:
            input_variables += ["df_content"]

    if prefix is None:
        prefix = MULTI_DF_PREFIX

    df_locals = {}
    for i, dataframe in enumerate(dfs):
        df_locals[f"df{i + 1}"] = dataframe
    tools = [PythonAstREPLTool(locals=df_locals)]

    desc_prompt = _build_multi_prompt(
        dfs,
        include_df_content, 
        df_rows,
        tools, 
        prefix = PREFIX,
        suffix = desc_suffix,
        input_variables=input_variables,
        number_of_head_rows = number_of_head_rows,
    )

    code_prompt = _build_multi_prompt(
        dfs,
        include_df_content, 
        df_rows,
        tools, 
        prefix = PREFIX,
        suffix = code_suffix,
        input_variables=input_variables,
        number_of_head_rows = number_of_head_rows,
    )

    prompt_infos = [
    {
        "name": "description", 
        "description": "Good for answering questions with an English description", 
        "prompt_template": desc_prompt
    },
    {
        "name": "code", 
        "description": "Good for answering questions that need code or plots returned", 
        "prompt_template": code_prompt
    }
    ]


    return prompt_infos, tools


def _build_prompt(
        df: Any,
        include_df_content : bool, 
        df_rows: Optional[List[int]] = None,
        tools : Optional[List[BaseTool]] = [], 
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        input_variables : Optional[List[str]] = None,
        number_of_head_rows: int = 5,
        use_memory: bool = False
    ):
    if input_variables is None:
        input_variables = ["input", "agent_scratchpad"]
        if include_df_content:
            input_variables += ["df_content"]

    # CC : This should allow the prompt to access the past conversations.
    if use_memory:
        input_variables += ["chat_history"]


    prompt = ZeroShotAgent.create_prompt(
        tools, prefix=prefix, suffix=suffix, input_variables=input_variables
    )

    partial_prompt = prompt.partial()
    if "df_content" in input_variables:
        if df_rows is None:
            partial_prompt = partial_prompt.partial(
                df_content=str(df.head(number_of_head_rows).to_markdown())
            )
        else:
            partial_prompt = partial_prompt.partial(
                df_content=str(df.iloc[df_rows].to_markdown())
            )

    return partial_prompt
            

def _get_single_prompt_template(
    df: Any,
    df_rows: Optional[List[List[int]]] = None,
    input_variables: Optional[List[str]] = None,
    include_df_in_prompt: Optional[bool] = True,
    number_of_head_rows: int = 5,
    use_memory: bool = False
) -> Tuple[BasePromptTemplate, List[PythonAstREPLTool]]:
    
    routes = {
        "description" : "Good for answering general or math questions when the user doesn't specify a table or plot as output.",
        "code_table" : "Good for answering questions about tables when we want to display results as a table", 
        "code_plot" : "Good for answering questions about tables when we want to display code, plots, and graphs"
    }

    suffix_dict = {}

    if use_memory:
        final_suffix = CHAT_HISTORY_SUFFIX
    else:
        final_suffix = NO_CHAT_HISTORY_SUFFIX


    if df_rows is not None:
        if len(df_rows) != 1:
            raise ValueError(f"Number of row selections does not match number of dfs {len(df_rows)} != 1")
        
        df_rows = df_rows[0]

        include_df_content = True
        suffix_dict["description"] = DESC_SUFFIX_WITH_DF + final_suffix
        suffix_dict["code_table"] = CODE_TABLE_SUFFIX_WITH_DF + final_suffix
        suffix_dict["code_plot"] = CODE_PLOT_SUFFIX_WITH_DF + final_suffix
    elif include_df_in_prompt:
        include_df_content = True
        suffix_dict["description"] = DESC_SUFFIX_WITH_DF + final_suffix
        suffix_dict["code_table"] = CODE_TABLE_SUFFIX_WITH_DF + final_suffix
        suffix_dict["code_plot"] = CODE_PLOT_SUFFIX_WITH_DF + final_suffix
    else:
        include_df_content = False
        suffix_dict["description"] = DESC_SUFFIX_NO_DF + final_suffix
        suffix_dict["code_table"] = CODE_TABLE_SUFFIX_NO_DF + final_suffix
        suffix_dict["code_plot"] = CODE_PLOT_SUFFIX_NO_DF + final_suffix

    tools = [PythonAstREPLTool(locals={"df": df})]

    prompt_infos = []
    for name, description in routes.items():
        prompt_template = _build_prompt(
            df,
            include_df_content, 
            df_rows,
            tools, 
            prefix = PREFIX,
            suffix = suffix_dict[name],
            input_variables=input_variables,
            number_of_head_rows = number_of_head_rows,
            use_memory = use_memory
        )
        next_route = {
            "name" : name,
            "description" : description,
            "prompt_template": prompt_template
        }
        prompt_infos.append(next_route)

    return prompt_infos, tools


def _get_prompt_template_and_tools(
    df: Any,
    df_rows: Optional[List[List[int]]] = None,
    input_variables: Optional[List[str]] = None,
    include_df_in_prompt: Optional[bool] = True,
    number_of_head_rows: int = 5,
    use_memory: bool = False,
) -> Tuple[BasePromptTemplate, List[PythonAstREPLTool]]:
    try:
        import pandas as pd
    except ImportError:
        raise ValueError(
            "pandas package not found, please install with `pip install pandas`"
        )

    if include_df_in_prompt is not None and df_rows is not None:
        raise ValueError("If suffix is specified, include_df_in_prompt should not be.")

    if isinstance(df, list):
        for item in df:
            if not isinstance(item, pd.DataFrame):
                raise ValueError(f"Expected pandas object, got {type(df)}")
        if use_memory:
            raise ValueError("Multi csv prompt templates don't currently support memory.")
        return _get_multi_prompt_template(
            df,
            df_rows = df_rows,
            input_variables=input_variables,
            include_df_in_prompt=include_df_in_prompt,
            number_of_head_rows=number_of_head_rows,
        )
    else:
        if not isinstance(df, pd.DataFrame):
            raise ValueError(f"Expected pandas object, got {type(df)}")
        return _get_single_prompt_template(
            df,
            df_rows = df_rows,
            input_variables=input_variables,
            include_df_in_prompt=include_df_in_prompt,
            number_of_head_rows=number_of_head_rows,
            use_memory = use_memory
        )

def create_pandas_dataframe_agent(
    llm: BaseLanguageModel,
    df: Any,
    agent_type: AgentType = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callback_manager: Optional[BaseCallbackManager] = None,
    df_rows: Optional[List[List[int]]] = None,
    input_variables: Optional[List[str]] = None,
    verbose: bool = False,
    return_intermediate_steps: bool = False,
    max_iterations: Optional[int] = 15,
    max_execution_time: Optional[float] = None,
    early_stopping_method: str = "force",
    agent_executor_kwargs: Optional[Dict[str, Any]] = None,
    include_df_in_prompt: Optional[bool] = True,
    number_of_head_rows: int = 5,
    use_memory : bool = False,
    **kwargs: Dict[str, Any],
) -> AgentExecutor:
    """Construct a pandas agent from an LLM and dataframe."""
    agent: BaseSingleActionAgent


    if agent_type == AgentType.ZERO_SHOT_REACT_DESCRIPTION:
        _prompt_infos, tools = _get_prompt_template_and_tools(
            df,
            df_rows,
            input_variables=input_variables,
            include_df_in_prompt=include_df_in_prompt,
            number_of_head_rows=number_of_head_rows,
            use_memory = use_memory
        )
        
        tool_names = [tool.name for tool in tools]

        for i in range(0, len(_prompt_infos)):
            prompt = _prompt_infos[i]['prompt_template']


            llm_chain = LLMChain(
                llm=llm,
                prompt=prompt,
                callback_manager=callback_manager,
            )
            agent = ZeroShotAgent(
                llm_chain=llm_chain,
                allowed_tools=tool_names,
                callback_manager=callback_manager,
                **kwargs,
            )

            if use_memory:
                memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, return_messages=True)
                _prompt_infos[i]['agent_chain'] = AgentExecutor.from_agent_and_tools(
                    agent=agent,
                    tools=tools,
                    callback_manager=callback_manager,
                    verbose=verbose,
                    return_intermediate_steps=return_intermediate_steps,
                    max_iterations=max_iterations,
                    max_execution_time=max_execution_time,
                    early_stopping_method=early_stopping_method,
                    memory=memory,
                    **kwargs,
                )
            else:
                _prompt_infos[i]['agent_chain'] = AgentExecutor.from_agent_and_tools(
                    agent=agent,
                    tools=tools,
                    callback_manager=callback_manager,
                    verbose=verbose,
                    return_intermediate_steps=return_intermediate_steps,
                    max_iterations=max_iterations,
                    max_execution_time=max_execution_time,
                    early_stopping_method=early_stopping_method,
                    **kwargs,
                )
        llm_chain = PandasMultiPromptChain.from_prompts(
            llm, 
            _prompt_infos, 
            callback_manager=callback_manager,
            default_chain=_prompt_infos[0]['agent_chain'], # Use the description chain as the default.
            verbose=verbose
            )    
    else:
        raise ValueError(f"Agent type {agent_type} not supported at the moment.")
    
    # import pdb
    # pdb.set_trace()
    return llm_chain
