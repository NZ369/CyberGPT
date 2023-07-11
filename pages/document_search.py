import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from agents.qa_agent import qa_chain
from streamlit_extras.app_logo import add_logo
from PIL import Image

# Define function to get user input
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input(
        "You: ",
        st.session_state["input"],
        key="input",
        
        placeholder="Ask me anything ...",
        
        label_visibility='hidden'
    )
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
    page_icon="📃",
    layout='wide'
)
image = Image.open('assets/logo.png')
st.image(image, width=500)
st.subheader("Cybersecurity Copilot: 📃 Document Search")

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
    add_logo('assets/logo2.png', height=50)
    st.title('CyberGPT')
    st.markdown('''
    ## About
    CyberGPT to query and find documents, technical documents and papers stored in our index database.
    ''')
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
        output = qa_chain.run(question=user_input)
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
        
hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)