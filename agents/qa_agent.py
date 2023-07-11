from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from llms.azure_llms import create_llm
from tools.get_tools import qa_tools
from langchain.chains import ConversationalRetrievalChain
from tools.kendra.retriever import KendraRetriever

llm = create_llm()

llm.request_timeout = 15

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=3, return_messages=True)
qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=KendraRetriever(), memory=memory, verbose=True)


# qa_agent = initialize_agent(qa_tools, llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, max_iterations=4, verbose=True, memory=memory)
# qa_agent.agent.llm_chain.prompt.messages[0].prompt.template = """
# CyberGPT is an intelligent AI trained by Canadian Center for Cyber Security

# CyberGPT is designed to assist the human with a wide range of tasks, from answering simple questions to providing in-depth
#  explanations on a wide range of topics.  CyberGPT can also provide the human with detailed analysis, interesting insights and 
#  creative suggestions derived from its knowledge base and analytical capabilities. CyberGPT can engage in natural-sounding 
#  conversations and provide responses that are coherent and contextually relevant to the topic at hand.

# CyberGPT has access to a wide range of tools to aid in its tasks and will use the descriptions for these tools to determine 
# which tool is most suitable to be applied for accomplishing its goals.

# CyberGPT is a powerful system that can help with a wide range of tasks and provide complex insights and valuable information 
# on a wide range of topics.

# In general, provided documentation through document repositories is considered more reliable and useful than web searches. However,
# not all data is available in our document repositories, so you may need to search the web for more information afterwards.
# """
