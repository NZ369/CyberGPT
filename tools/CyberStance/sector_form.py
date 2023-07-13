from tools.CyberStance.form import Form
from tools.CyberStance.field import Field

import re

def generate_form_selection_field():
    return Field("Select one of the sectors to analyze? (email)",
        lambda user_input: (False, "Invalid option") if len(result := re.findall(r'email', user_input.lower())) != 1 else (True, user_input.lower())
    )

# create field for different forms
# create email sector form