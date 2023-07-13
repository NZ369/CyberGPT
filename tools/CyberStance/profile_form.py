from tools.CyberStance.form import Form
from tools.CyberStance.field import Field

import re

from llms.azure_llms import create_llm

from langchain import PromptTemplate, LLMChain

from typing import Tuple, List

import streamlit as st

#SASS_FLAG = True
'''
def prompt_llm(query:str) -> str:
    llm = create_llm()

    llm_chain = LLMChain(llm=llm,prompt=PromptTemplate.from_template("{query}"))

    print(query)

    return llm_chain(query)["text"]

def options_input_extractor(user_input: str, targets: List[str]) -> Tuple[bool, str]:
    result = prompt_llm(f"Convert query into one of the following N\A,{','.join(targets)}. query: {user_input}")
'''
def generate_new_profile_form():
    forms = Form([
        Field("What is the size of your organization? (How many employees)",
            lambda user_input: (False, "No numbers detected") if len(nums := re.findall(r'\d+', user_input)) != 1 else (True, "Small") if int(nums[0]) < 50 else (True, "Medium") if int(nums[0]) < 500 else (True, "Large")
        ),
        Field("Do you have a dedicated cyber security team or personnel? (yes or no)",
            lambda user_input: (False, "Answer must be yes or no") if len(data := re.findall(r'(yes|no)', user_input.lower())) != 1 else (True, data[0].capitalize())
        ),
        Field("What is their IT/Computer expertise level? Please use one of the following options (little to no experience or moderate experience or high experience)",
            lambda user_input: (False, "Invalid option") if len(data := re.findall(r'(little to no experience|moderate experience|high experience)', user_input.lower())) != 1 else (True, data[0])
        ),
        Field("What industry sector does your organization fall under? Please use one of the following options(Consumer Products|Manufacturing|Service Providers|Technologies)",
            lambda user_input: (False, "Invalid option") if len(data := re.findall(r'(Consumer Products|Manufacturing|Service Providers|Technologies)', user_input)) != 1 else (True, data[0])
        ),
        Field("Does your organization follow any industry standards or frameworks? Select all that apply(ISO|NIST|ISM|ITSG|CIS|OTHER)",
            lambda user_input: (False, "Invalid option") if len(data := re.findall(r'(ISO|NIST|ISM|ITSG|CIS|OTHER)', user_input.upper())) == 0 else (True, ",".join(data))
        )
    ])
    
    return forms
