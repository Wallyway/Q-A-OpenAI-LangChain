
import streamlit as st
from streamlit_chat import message as st_message

import toml

from qa import QAModel


# Initialize the QAModel and store it in the cache
@st.cache_resource()
def initialize_qamodel():
    return QAModel()


class QAApplication:

    def __init__(self):
        self.qamodel = initialize_qamodel()                                                 # Initialize the QAModel and store it in the cache
    
    def generate_answer(self):
        request = st.session_state.request                                                  # Get the request from the session state

        response = self.qamodel(request=request)                                            # Generate the response from the QAModel

        st.session_state.history.append({"message": request, "is_user": True})              # Append the request to the history
        st.session_state.history.append({"message": response['result'],"is_user": False})   # Append the response to the history

        st.session_state.something = st.session_state.request                               # Store the request in the session state
        st.session_state.input_text = ''                                                    # Clear the input text

    
    def run_app(self):
        st.title("Ask me anything about coffe")                                             # Set the title of the app

        if "history" not in st.session_state:                                               # Initialize the history in the session state
            st.session_state.history = []
        
        if st.button("Clear History"):                                                      # Clear the history
            st.session_state.history = []

        st.text_input("", key="request", on_change=self.generate_answer)                    # Text input for the request

        for i, chat in enumerate(st.session_state.history):                                 # Display the chat history
            st_message(**chat, key=str(i))                                                  # Display the chat message
    
if __name__ == '__main__':
    qa = QAApplication()
    qa.run_app()