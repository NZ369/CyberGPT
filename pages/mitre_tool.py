import streamlit as st
import time
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space
from agents.csv_agent import mitre_csv_agent
from tools.qa_tools import create_qa_retriever

st.set_page_config(page_title="Mitre CSV Demo", page_icon="📈")

st.markdown("# Mitre CSV")
st.sidebar.header("Mitre CSV")
st.write(
    """This page loads informatiom from MITRE ATT&CK for the LLM to query."""
)

# Define function to get user input
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                            placeholder="Ask me anything ...", 
                            label_visibility='hidden')
    return input_text

# Function for starting a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    print("Start a new chat!")
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []



with st.sidebar:
    st.title('CyberGPT')
    st.markdown('''
    ## About
    CyberGPT is a smart AI assistant for cyber security analysts.
    ''')
    st.subheader("Your documents")
    pdf_docs = st.file_uploader("Select your PDFs here", accept_multiple_files=True)
    if st.button("Submit"):
        with st.spinner("Processing"):
            create_qa_retriever(pdf_docs, type="azure", database="FAISS")
        st.success("Embeddings completed.", icon="✅")
    add_vertical_space(2)
    # Add a button to start a new chat
    st.button("New Chat", on_click = new_chat, type='primary')
    add_vertical_space(2)
    st.write('Made with ❤️ by GeekWeek Team 5.2')

# Get the user input
user_input = get_text()

# Processes the user input
if user_input:
    st.session_state.past.append(user_input)
    # Try block handles any error with not parsing LLM output
    try:
        # Calls the base agent
        print("Calling Agent:")
        output = mitre_csv_agent.run(input=user_input)
        print(f"Output: {output}")
        st.session_state.generated.append(output)
    except Exception as e:
        st.session_state.generated.append(str(e))


# Allow to download as well
download_str = []
# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.info(st.session_state["past"][i],icon="🙂")
        st.success(st.session_state["generated"][i], icon="🤖")
        download_str.append("User: "+st.session_state["past"][i])
        download_str.append("AI: "+st.session_state["generated"][i])
    
    # Can throw error - requires fix
    download_str = '\n\n'.join(download_str)
    if download_str:
        st.download_button('Download',download_str)


# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")