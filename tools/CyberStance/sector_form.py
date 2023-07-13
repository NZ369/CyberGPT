from tools.CyberStance.form import Form
from tools.CyberStance.field import Field

import re

def generate_form_selection_field():
    return Field("Select one of the sectors to analyze? (email)",
        lambda user_input: (False, "Invalid option") if len(result := re.findall(r'email', user_input.lower())) != 1 else (True, user_input.lower())
    )


def generate_email_form():
    forms = Form([
        Field("Do you have SPF (Sender Policy Framework) enabled and configured? (yes or no)",
            lambda user_input: (False, "Answer must be yes or no") if len(data := re.findall(r'(yes|no)', user_input.lower())) != 1 else (True, data)
        ),
        Field("Do you have DMARC (Domain Message Authentication Reporting & Conformance) enabled and configured? (yes or no)",
            lambda user_input: (False, "Answer must be yes or no") if len(data := re.findall(r'(yes|no)', user_input.lower())) != 1 else (True, data)
        ),
        Field("Do you have DKIM (DomainKeys Identified Mail) enabled and configured? (yes or no)",
            lambda user_input: (False, "Answer must be yes or no") if len(data := re.findall(r'(yes|no)', user_input.lower())) != 1 else (True, data)
        )
    ])

    return forms

generate_form = {"email": generate_email_form}
# create field for different forms
# create email sector form