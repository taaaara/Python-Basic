# To run, copy and paste the code below.
# streamlit run tara.py --server.port 8080 --server.address 0.0.0.0

# streamlit official doc link:
# https://docs.streamlit.io/

import streamlit as st

st.title("")
st.write("")




st.markdown("""
    <style>
        /* Garden-inspired Title */
        .garden-title {
            font-family: 'Georgia', serif;
            font-size: 48px;
            color: #4CAF50; /* Garden green color */
            text-align: center;
            font-weight: bold;
            text-shadow: 3px 3px 10px rgba(0,0,0,0.4);
            margin-bottom: 20px;
        }

        /* General body styling with a nature feel */
        body {
            background-color: #f0f4f1; /* Light greenish background */
            color: #333; /* Dark grey for contrast */
            font-family: 'Times New Roman', serif;
        }

        /* Additional garden-themed text styling */
        .garden-text {
            font-size: 18px;
            line-height: 1.8;
            color: #2E8B57; /* Darker green color for text */
            text-align: justify;
            padding: 20px;
        }

        /* Button styling to match garden theme */
        .stButton>button {
            background-color: #98FB98; /* Light green */
            color: #006400; /* Dark green */
            font-size: 18px;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
        }

        .stButton>button:hover {
            background-color: #32CD32; /* Brighter green on hover */
            color: white;
        }

        /* Adding a gentle image background */
        .background {
            background-image: url('https://www.w3schools.com/w3images/forest.jpg'); /* Garden-inspired background image */
            background-size: cover;
            background-position: center;
            padding: 30px;
        }
    </style>
    <div class="background">
        <h1 class="garden-title">The Forgotten Garden</h1>
    </div>
""", unsafe_allow_html=True)





text = """
The sun was low in the sky casting long shadows over the forgotten garden. Vines twisted up the crumbling stone walls and flowers bloomed in wild disarray their colors muted by the weight of years. The air was thick with the scent of damp earth and growing things, a peaceful silence stretching through the tangled paths.

A figure moved slowly through the overgrowth, each step measured, as if searching for something long lost. The ground was uneven, covered in thick moss and fallen leaves. She paused at an old wooden bench, its paint chipped and faded, almost blending into the natural world around it. Her fingers brushed over the worn surface, a quiet reverence in the motion.

Beneath the bench, a small patch of wildflowers swayed gently in the breeze. Their petals, once vibrant, had faded to soft pastels. She knelt down, her hand moving to gently lift one of the flowers. It was delicate, but still strong, still growing. For a moment, the world seemed to hold its breath.

Then, just as quietly as she had arrived, she stood and turned back toward the path. The garden was left as it was, forgotten by most but still alive, still waiting, like a memory that refused to fade.
"""

# Display text using Streamlit
st.write(text)





