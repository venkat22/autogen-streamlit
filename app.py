import os

import streamlit as st
import asyncio
from autogen import AssistantAgent, UserProxyAgent
from dotenv import load_dotenv

load_dotenv()

st.write("""# AutoGen Chat Agents""")
print(os.environ.get("api_key"))


class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)

    # for message in st.session_state["messages"]:
    #    st.markdown(message)


user_input = st.chat_input("Type something...")
if user_input:
    llm_config = [{
        "model": "jdcraig",
        "api_key": os.environ.get("api_key"),
        "base_url": "https://xxxxx.openai.azure.com/",
        "api_type": "azure",
        "api_version": "2023-07-01-preview"
    }
    ]

    # create an AssistantAgent instance named "assistant"
    assistant = TrackableAssistantAgent(
        name="assistant", llm_config={"config_list": llm_config})

    # create a UserProxyAgent instance named "user"
    user_proxy = TrackableUserProxyAgent(
        name="user", human_input_mode="NEVER", llm_config={"config_list": llm_config})

    # Create an event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)


    # Define an asynchronous function
    async def initiate_chat():
        await user_proxy.a_initiate_chat(
            assistant,
            message=user_input,
        )


    # Run the asynchronous function within the event loop
    loop.run_until_complete(initiate_chat())
