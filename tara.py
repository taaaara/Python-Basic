# To run, copy and paste the code below.
# streamlit run tara.py --server.port 8080 --server.address 0.0.0.0

# streamlit official doc link:
# https://docs.streamlit.io/

import streamlit as st

title = "No Hunger"      # "" for variable
st.title(title)

text = """
Help people who are starving. Give them food. The more people you help you get you earn "Thank You Points". 
With that you can buy other foods which will make you more points.
"""
st.write(text)
st.write("")
