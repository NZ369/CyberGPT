import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

from streamlit_extras.app_logo import add_logo

from PIL import Image

from tools.CyberStance.profile_form import generate_new_profile_form

from enum import Enum

class PageComponent(Enum):
    PROFILE_GENERATION = 1
    FORM_SELECTION = 2
    DOCUMENT_QUERY = 3

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
        
        placeholder="",
        
        label_visibility='hidden'
    )
    return input_text

# Set Streamlit page configuration
st.set_page_config(
    page_title="CyberGPT",
    page_icon="🔎",
    layout='wide'
)
image = Image.open('assets/logo.png')
st.image(image, width=500)
st.subheader("Cybersecurity Copilot: Cyber Stance")

# Initialize session states
# AI stuff
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

# Form stuff
if "user_profile" not in st.session_state:
    st.session_state["user_profile"] = generate_new_profile_form()
if "visible_components" not in st.session_state:
    st.session_state["visible_components"] = set([PageComponent.PROFILE_GENERATION])


# Set up sidebar with various options
with st.sidebar:
    add_logo('assets/logo2.png', height=50)
    st.title('CyberGPT')
    st.markdown('''
    ## About
    Place holder description
    ''')
    
    # Swapping profiles

    add_vertical_space(2)
    st.write('Made with ❤️ by GeekWeek Team 5.2 & Cyber Stance Team 4.4')

# Get the user input

# Name forum
if PageComponent.PROFILE_GENERATION in st.session_state["visible_components"]:
    st.write("# User Profile")
    st.session_state["visible_components"].add(PageComponent.FORM_SELECTION)

    # Add next section once form is completed
    if st.session_state["user_profile"].completed() and not PageComponent.FORM_SELECTION in st.session_state["visible_components"]:
        st.session_state["visible_components"].add(PageComponent.FORM_SELECTION)

if PageComponent.FORM_SELECTION in st.session_state["visible_components"]:
    st.write("# Select Form")

if PageComponent.DOCUMENT_QUERY in st.session_state["visible_components"]:
    user_input = get_text()


# Processes the user input
#if user_input:
#    st.session_state.past.append(user_input)
    # Try block handles any error with not parsing LLM output
#    try:
#        # Calls the base agent
#        output = qa_chain.run(question=user_input)
#        st.session_state.generated.append(output)
#    except Exception as e:
#        st.session_state.generated.append(str(e))

# Allow to download as well
#download_str = []
# Display the conversation history using an expander, and allow the user to download it
#with st.expander("Conversation", expanded=True):
#    for i in range(len(st.session_state['generated'])-1, -1, -1):
#        st.info(st.session_state["past"][i],icon="🙂")
#        st.success(st.session_state["generated"][i], icon="🤖")
#        download_str.append("User: "+st.session_state["past"][i])
#        download_str.append("AI: "+st.session_state["generated"][i])
    
    # Can throw error - requires fix
#    download_str = '\n\n'.join(download_str)
#    if download_str:
#        st.download_button('Download',download_str)

hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)