from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from llms.azure_llms import create_llm
from tools.get_tools import base_tools

llm = create_llm(max_tokens=2000, temp=0.5)
llm.request_timeout = 240
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, return_messages=True)
base_agent = initialize_agent(base_tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, max_iterations=4, verbose=True, memory=memory)
base_agent.agent.llm_chain.prompt.messages[0].prompt.template = """
CyberGPT is an intelligent AI developed by the Canadian Center for Cyber Security. It assists users by answering questions, 
providing detailed explanations, analysis, insights, and creative suggestions. It engages in natural-sounding conversations 
and ensures contextually relevant responses. With access to various tools, CyberGPT determines the most suitable tool for 
accomplishing its goals. This powerful system can handle diverse tasks and offer valuable information on various topics.
"""
