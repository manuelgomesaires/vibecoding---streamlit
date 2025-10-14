import streamlit as st

st.set_page_config(page_title="Hello World")

st.title("Hello World")
name = st.text_input("What's your name?", "")
if name:
  st.write(f"Hello, {name}!")
