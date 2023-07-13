from tools.CyberStance.tool import CyberStance

import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.app_logo import add_logo
from PIL import Image

from enum import Enum

from tools.CyberStance.profile_form import generate_new_profile_form

from tools.CyberStance.sector_form import generate_form_selection_field, generate_form

from tools.CyberStance.field import Field
from tools.CyberStance.form import Form

import random

class PageState(Enum):
    PROFILE_GENERATION = 1
    FORM_SELECTION = 2
    FORM_GENERATION = 3
    DOCUMENT_QUERY = 4

# Define function to get user input
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    input_text = st.text_input("You: ", st.session_state["input"], key="input",
                            label_visibility='hidden')
    
    return input_text

# Function for starting a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    st.session_state[LOG] = []
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

# CONST
POSITIVE_COMMENTS = [
    "Great answer, thank you!",
    "Very helpful and informative!",
    "I appreciate your insight!",
    "You nailed it, well done!",
    "That's a brilliant solution!",
    "You explained it very clearly!",
    "I learned something new today!",
    "You have a great point!",
    "That's exactly what I needed!",
    "You are awesome, thanks!"
]
NEGATIVE_COMMENTS = [
    "Wow, you're so smart. Not.",
    "Did you even read the question?",
    "That's a nice try, but no.",
    "You must be fun at parties.",
    "Are you always this clueless?",
    "Do you hear yourself talking?",
    "Bless your heart, honey.",
    "That's cute, but wrong.",
    "You're kidding, right?",
    "You're hilarious, but no."
]

# Initialize session states
# Page states
LOG = "log"
if LOG not in st.session_state:
    st.session_state[LOG] = []
STATE = "state"
if STATE not in st.session_state:
    st.session_state[STATE] = None

# Query States
PROFILE = "profile"
if PROFILE not in st.session_state:
    st.session_state[PROFILE] = generate_new_profile_form()

SECTOR_FORM = "sector"
if SECTOR_FORM not in st.session_state:
    st.session_state[SECTOR_FORM] = {"selected":generate_form_selection_field(), "form": None}

if "input" not in st.session_state:
    st.session_state["input"] = ""

def add_log(id: str, msg: str):
    st.session_state["log"].append({"id": id, "msg": msg})

def change_states(next_state, callback = None):
    if next_state.name == PageState.PROFILE_GENERATION.name:
        current_question = st.session_state[PROFILE].first_unanswered()
        add_log("🤖", f"{random.choice(POSITIVE_COMMENTS)} We will now be generating your companies profile\n\n{current_question.question}")

    elif next_state.name == PageState.FORM_SELECTION.name:
        current_question = st.session_state[SECTOR_FORM]["selected"].question
        add_log("🤖", f"{random.choice(POSITIVE_COMMENTS)}\n\n{current_question}")

    elif next_state.name ==  PageState.FORM_GENERATION.name:
        form_name = st.session_state[SECTOR_FORM]["selected"].value

        st.session_state[SECTOR_FORM]["form"] = generate_form[form_name]()

        current_question = st.session_state[SECTOR_FORM]["form"].first_unanswered()

        add_log("🤖", f"{random.choice(POSITIVE_COMMENTS)}\n\nWe are ready to start analyzing your company's {form_name} policy\n\n{current_question.question}")

    elif next_state.name ==  PageState.DOCUMENT_QUERY.name:
        add_log("🤖", f"Big man! We got a report just for you")
    
    st.session_state[STATE] = next_state
    print("new states")
    print(st.session_state[STATE])
    
    
    if callback is not None:
        callback()

def fill_in_form(form: Form, next_state: PageState):
    if form.completed():
        change_states(next_state)

    current_question = form.first_unanswered()
    
    if current_question == None:
        change_states(next_state)
        return
    
    cond, msg = current_question.input_parser(user_input)

    if not cond:
        add_log("🤖", f"{random.choice(NEGATIVE_COMMENTS)}\n\nThats not what I want, {msg}.\n\n{current_question.question}")
    else:
        if form.completed():
            change_states(next_state)
        else:
            next_question = form.first_unanswered()
            add_log("🤖", f"{random.choice(POSITIVE_COMMENTS)}\n\n{next_question.question}")

def process_user_input(user_input):
    if st.session_state[STATE] is None:
        change_states(PageState.PROFILE_GENERATION)
        return

    if st.session_state[STATE].name == PageState.PROFILE_GENERATION.name:
        fill_in_form(st.session_state[PROFILE], PageState.FORM_SELECTION)
                
    elif st.session_state[STATE].name is PageState.FORM_SELECTION.name:
        current_question = st.session_state[SECTOR_FORM]["selected"]
        
        cond, msg = current_question.input_parser(user_input)

        if current_question.is_valid():
            change_states(PageState.FORM_GENERATION)
            return
        
        if not cond:
            add_log("🤖", f"{random.choice(NEGATIVE_COMMENTS)}\n\nThats not what I want, {msg}.\n\n{current_question.question}")
        
    elif st.session_state[STATE].name is PageState.FORM_GENERATION.name:
        fill_in_form(st.session_state[SECTOR_FORM]["form"], PageState.DOCUMENT_QUERY)
    elif st.session_state[STATE].name is PageState.DOCUMENT_QUERY.name:
        pass

if "THE TOOL" not in st.session_state:
    st.session_state["THE TOOL"] = CyberStance()

    add_log("🤖", f'''
Hello!!
  
press Type "{"show me the sh-money".upper()}" to begin
''')


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



# Get the user input
user_input = get_text()

# Processes the user input
if user_input:
    add_log("🙂", user_input)
    # Try block handles any error with not parsing LLM output
    try:
        process_user_input(user_input)
    except Exception as e:
        add_log("🤖", str(e))

# Display the conversation history using an expander, and allow the user to download it
for i in range(len(st.session_state['log'])):
    log_val =  st.session_state["log"][::-1][i]

    if log_val["id"] == "🤖":
        st.success(log_val["msg"], icon=log_val["id"])
    elif log_val["id"] == "🙂":
        st.info(log_val["msg"], icon=log_val["id"])
        

    
hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)