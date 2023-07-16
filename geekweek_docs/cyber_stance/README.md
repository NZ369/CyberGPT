# Cyber Stance
## Challenges
- We used Streamlit as a UI framework to build a web application for collecting user inputs. Streamlit has some advantages, such as speed and simplicity, but it also has some drawbacks. One of the main challenges we faced was the lack of support for dynamic conditional UI. This means that Streamlit can execute conditional blocks when the page is first loaded, but it cannot update them when the state changes.
- As a result, we found that Streamlit was suitable for creating UIs that resemble chat logs, but not for more complex and interactive forms.

## What We Achieved
- We created a simple UI and backend to gather user inputs in the form of a chat conversation. The user inputs are then used to compare their data to the latest standards and generate a report.

## Future Improvements
- A chat-style form is not ideal for collecting user inputs, as it does not allow the user to go back and edit their responses. It also does not provide any feedback or guidance on how to fill out the form correctly. Therefore, it is worth looking into other frameworks, such as React, that can create dynamic and responsive forms.
- There is value in looking into an AI assistant that can help answer questions related to each form field, provide clarification or suggestions, and update responses as needed. This would require using an LLM to generate natural language responses and interact with the user. The LLM tokens would only be used when necessary, as the assistant would only respond to user queries or requests.