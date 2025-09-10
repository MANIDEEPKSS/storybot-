import streamlit as st
import os
from langchain_groq import ChatGroq

# Set up API key (secure input via Streamlit sidebar)
if "GROQ_API_KEY" not in os.environ:
    groq_api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key

# --- MAKE THE CHANGE HERE ---

if "GROQ_API_KEY" in os.environ:
    # UI for user input
    st.title("Custom Story Generator")
    st.markdown("Generate a story tailored to an age group and a moral.")

    user_age = st.text_input("Enter the age group for the story (e.g., 'for children under 10', 'for teenagers', 'for adults'):")
    user_moral = st.text_area("Enter the situation or moral for the story (e.g., 'the importance of sharing', 'overcoming fear', 'a mysterious adventure'):")
    
    # Create a button to trigger the story generation
    if st.button("Generate Story"):
        if user_age and user_moral:
            # Initialize the model
            llm = ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=None,
                timeout=None,
                max_retries=2,
            )

            # Define messages for story generation
            messages = [
                (
                    "system",
                    f"""You are a creative storyteller. Your task is to generate a story that is appropriate for the age group '{user_age}' and is centered around the moral or situation: '{user_moral}'. The story should be engaging and the moral should be clear at the end of the story. Do not add any extra commentary, just provide the story.""",
                ),
                ("human", f"Please write a story based on the given instructions."),
            ]

            # Invoke model and display result
            with st.spinner('Generating your story...'):
                try:
                    response = llm.invoke(messages)
                    st.success("Here is your story:")
                    st.write(response.content)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("Please fill out both the age group and the moral/situation.")
else:
    # This is the line that needs to be visible on the main page.
    st.warning("Please enter your Groq API key in the sidebar.")
    st.info("Expand the sidebar by clicking the '>' arrow on the top-left to enter your key.")