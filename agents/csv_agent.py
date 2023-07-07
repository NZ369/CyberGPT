import os
import boto3
import pandas as pd
from llms.azure_llms import create_llm
from langchain.agents import create_csv_agent
from langchain.agents.agent_types import AgentType
from chains.pandas_multi_prompt import PandasMultiPromptChain

llm = create_llm(temp=0)



print("Creating CSV Agent.")
combined_data = os.path.join("data", "combined.csv")


CODE_SUFFIX_WITH_DF = """
You should return python code, not a description.
This is the result of printing rows from the dataframe:
{df_content}

Begin!
Question: {input}
{agent_scratchpad}"""



DESC_SUFFIX_WITH_DF = """
This is the result of printing rows from the dataframe:
{df_content}

Begin!
Question: {input}
{agent_scratchpad}"""


# mitre_dir = "../data"
# mitre_data = [os.path.join(mitre_dir, fn) for fn in ["software.csv", "groups.csv", "mitigations.csv"]]
# if not os.path.exists(combined_data):
#     combined_df = None
#     keys = ['TID', 'Technique Name']
#     for fp in mitre_data:
#         next_df = pd.read_csv(fp)
#         if combined_df is not None:
#             combined_df = combined_df.merge(
#                 next_df,
#                 on=['TID', 'Technique Name'],
#                 how='outer'
#             )
#         else:
#             combined_df = next_df
    
#     combined_df.to_csv(combined_data)


# Waiting on Secret Key info for Amazon.
def download_files(bucket_name="team5.2-mitre", data_dir="data", files=[]):
    s3_client = boto3.client('s3')
    os.makedirs(data_dir, exist_ok=True)
    for fn in files:
        fp = os.path.join(data_dir, fn)
        if not os.path.exists(fp):
            print(f"Downloading {fn}")
            s3_client.download_file(bucket_name, fn, fp)

download_files(files=["combined.csv"])


def get_mitre_agent():
    df = pd.read_csv(combined_data)
    # Use a selection of different rows from the data in the prompt
    # instead of just the header (has lots of repetition).
    df_content = str(df.iloc[[0,2000,4000,89000,123000]].to_markdown())

    desc_csv_agent = create_csv_agent(
        llm,
        combined_data,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        suffix = DESC_SUFFIX_WITH_DF,
        include_df_in_prompt = None,
        input_variables = ["df_content", "input", "agent_scratchpad"]

    )

    code_csv_agent = create_csv_agent(
        llm,
        combined_data,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        suffix = CODE_SUFFIX_WITH_DF,
        include_df_in_prompt = None,
        input_variables = ["df_content", "input", "agent_scratchpad"]

    )




    desc_csv_agent.agent.llm_chain.prompt = desc_csv_agent.agent.llm_chain.prompt.partial(df_content=df_content)
    code_csv_agent.agent.llm_chain.prompt = code_csv_agent.agent.llm_chain.prompt.partial(df_content=df_content)

    prompt_infos = [
    {
        "name": "description", 
        "description": "Good for answering questions with an English description", 
        "prompt_template": desc_csv_agent.agent.llm_chain.prompt.template
    },
    {
        "name": "code", 
        "description": "Good for answering questions that need code or plots returned", 
        "prompt_template": code_csv_agent.agent.llm_chain.prompt.template
    }
    ]



    # Try to force the underlying LLM agent into a MultiPromptChain
    desc_csv_agent.agent.llm_chain = PandasMultiPromptChain.from_prompts(
        llm = desc_csv_agent.agent.llm_chain.llm,
        prompt_infos = prompt_infos,
        df_content = df_content,
        input_variables = ["df_content", "input", "agent_scratchpad"],
        verbose=True
    ) 

    return desc_csv_agent

mitre_csv_agent = get_mitre_agent()

import pdb
pdb.set_trace()
mitre_csv_agent.run("What Techniques does FlawedAmmyy use?")

print("Finished Creating CSV Agent.")

