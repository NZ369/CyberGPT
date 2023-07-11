from tools.CyberStance.form import Form
from tools.CyberStance.field import Field

# TODO replace all the lambdas with LLM fun time tool to convert user inputs into something
form = Form([
    Field(
        "What is the size of your organization? (How many employees)",
        lambda x: x in ["Small", "Medium", "Large"], # number extractor -> map number to string (<50: small, 50-500: medium, >500: large)
        None
    ),
    Field(
        "Do you have a dedicated cyber security team or personnel?",
        lambda x: x in ["Yes", "No"], # simple convert yes or no
        None
    ),
    Field(
        "What is their IT/Computer expertise level? Please use one of the following options:",
        lambda x: x in ["Little to no experience", "Moderate experience", "High experience"], # simple convert options
        None
    ),
    Field(
        "What industry sector does your organization fall under? Please use one of the following options:", lambda x: x in ["Consumer Products", "Manufacturing", "Service Providers", "Technologies"], # Simple map to closet
        None
    ),
    Field(
        "Does your organization follow any industry standards or frameworks? Select all that apply:",
        lambda x: x in ["ISO", "NIST", "ISM", "ITSG", "CIS", "OTHER"], # Simple map to closet
        None
    )
])