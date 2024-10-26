import os
import json

import streamlit as st
from groq import Groq


# streamlit page configuration
st.set_page_config(
    page_title="LLAMA Legal Assistant",
    page_icon="🦙",
    layout="centered"
)

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))

GROQ_API_KEY = config_data["GROQ_API_KEY"]

# save the api key to environment variable
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

client = Groq()

# initialize the chat history as streamlit session state of not present already
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# streamlit page title
st.title("🦙 LLAMA Legal Assistant")

st.markdown("""
            
• Step 1 - File an FIR at the nearest Police Station within 24 hours\n

• Step 2 - get a medical examination done, as the sample of the accused may be present in the body of the victim and after 24 hours may not be traceable. \n

• Step 3 - Get legal help, in order to file a case against the perpetrator/s a lawyer is required to fulfill all the legal formalities (give the copy of the FIR to the lawyer, a copy of the FIR will be given by the police station free of charge) \n
• Step 4 - The pre-trial stage takes about 2-3 months to complete. The case is then listed before the court for presentation of evidence, witnesses, and arguments for a judicial determination of the facts, and whether the offence is made out. The victim is likely to be examined and cross examined (questioned) as part of the trial along with the other witnesses.\n
Ask any questions you have about the process or the IPC sections. Dont worry about the language barrier, I am here to help you. We are here for you.\n
""")

# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message:
user_prompt = st.chat_input("Ask LLAMA...")

if user_prompt:

    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sens user's message to the LLM and get a response
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        *st.session_state.chat_history
    ]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )

    assistant_response = response.choices[0].message.content
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    # display the LLM's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)