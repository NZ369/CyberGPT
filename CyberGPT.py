import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from tools.ip_report_tool import ip_report_tool
from tools.qa_tools import create_qa_retriever
from agents.base_agent import base_agent
from tools.borealis_tools import borealis_processing
from tools.opencti_tools import openCTI_search_processing
from streamlit_extras.app_logo import add_logo
#from utilities.plotting import check_if_display_plot
from PIL import Image

# Define function to get user input
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_area("You: ", st.session_state["input"], key="input",
                            placeholder="Ask me anything ...", 
                            label_visibility='hidden', height=100)
    return input_text

# Function for starting a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        save.append("User:" + st.session_state["past"][i])
        save.append("Bot:" + st.session_state["generated"][i])        
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    
# Set Streamlit page configuration
st.set_page_config(
    page_title="CyberGPT",
    page_icon="🤖",
    layout='wide'
)
image = Image.open('assets/logo.png')
st.image(image, width=500)
st.subheader("Cybersecurity Copilot")

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

# Set up sidebar with various options
with st.sidebar:
    add_logo("assets/logo2.png", height=50)
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

def process_user_input(user_input):
    if (("ip scan" and "borealis") in user_input):
        borealis_response = borealis_processing(user_input)
        if borealis_response == None:
            # Calls the base agent
            output = base_agent.run(input=user_input)
            st.session_state.generated.append(output)
        else:
            try:
                openCTI_response = openCTI_search_processing(user_input)
                response = borealis_response + "\n\n OpenCTI Scan Report \n" + openCTI_response
            except:
                print("OpenCTI not accessible outside CSE networks.")
                response = borealis_response
            st.session_state.generated.append(response)
    elif ("associated ips" in user_input or "ips associated" in user_input):
        try:
            openCTI_response = openCTI_search_processing(user_input)
            if openCTI_response == None:
                # Calls the base agent
                output = base_agent.run(input=user_input)
                st.session_state.generated.append(output)
            else:
                response = openCTI_response
                st.session_state.generated.append(response)
        except:
            output = base_agent.run(input=user_input)
            st.session_state.generated.append(output)
            print("OpenCTI not accessible outside CSE networks.")
    elif ("ip report" in user_input):
        try:
            output = ip_report_tool(user_input)
            st.session_state.generated.append(output)
        except:
            print("IP report tool failed")
    else:
        output = base_agent.run(input=user_input)
        # print(base_agent.memory.json)
        st.session_state.generated.append(output)

# Get the user input
user_input = get_text()

# Processes the user input
if user_input:
    st.session_state.past.append(user_input)
    # Try block handles any error with not parsing LLM output
    try:
        process_user_input(user_input)
    except Exception as e:
        st.session_state.generated.append(str(e))

# Allow to download as well
download_str = []
# Display the conversation history using an expander, and allow the user to download it
for i in range(len(st.session_state['generated'])-1, -1, -1):
    st.info(st.session_state["past"][i],icon="🙂")
    st.success(st.session_state["generated"][i], icon="🤖")
    #check_if_display_plot(st.session_state["generated"][i], i)
    download_str.append("User: "+st.session_state["past"][i])
    download_str.append("AI: "+st.session_state["generated"][i])
    
# Can throw error - requires fix
download_str = '\n\n'.join(download_str)
if download_str:
    st.download_button('Download',download_str)
        
hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)