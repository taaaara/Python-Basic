# To run, copy and paste the code below.
# streamlit run tara.py --server.port 8080 --server.address 0.0.0.0

# streamlit official doc link:
# https://docs.streamlit.io/

import streamlit as st

title = "Capybara"      # no "" for variable
st.title(title)        
st.write("")

name = st.text_input("Chat")
st.write(name)
