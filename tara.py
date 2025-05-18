# To run, copy and paste the code below.
# streamlit run tara.py --server.port 8080 --server.address 0.0.0.0

# streamlit official doc link:
# https://docs.streamlit.io/

import streamlit as st
import base64

# Function to convert an image file to a base64 encoded string.
def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Encode both images to base64
image1_base64 = get_base64_image("1.png")
image2_base64 = get_base64_image("2.png")


# HTML code that swaps the image when the red box is clicked
html_code = f"""
<!DOCTYPE html>
<html>
<head>
  <style>
    .container {{
      position: relative;
      display: inline-block;
    }}
    .clickable-area {{
      position: absolute;
      border: 2px solid red;
      cursor: pointer;
    }}
    /* Style for the single box on 1.png */
    #red-box {{
      top: 100px;
      left: 175px;
      width: 235px;
      height: 115px;
    }}
    /* Styles for the 7 boxes on 2.png */
    .red-box-2 {{
      display: none; /* Hidden initially */
    }}
    /* Example positions for 7 boxes on 2.png */
    #box1 {{ top: 30px; left: 65px; width: 70px; height: 90px; }}
    #box2 {{ top: 50px; left: 200px; width: 80px; height: 80px; }}
    #box3 {{ top: 50px; left: 475px; width: 80px; height: 80px; }}
    #box4 {{ top: 160px; left: 50px; width: 80px; height: 80px; }}
    #box5 {{ top: 160px; left: 150px; width: 80px; height: 80px; }}
    #box6 {{ top: 160px; left: 250px; width: 80px; height: 80px; }}
    #box7 {{ top: 270px; left: 150px; width: 80px; height: 80px; }}
  </style>
</head>
<body>
  <div class="container">
    <img id="main-image" src="data:image/png;base64,{image1_base64}" width="600" alt="Clickable Image">

    <!-- Single box on 1.png -->
    <div id="red-box" class="clickable-area" onclick="changeImage()"></div>

    <!-- Seven boxes on 2.png, hidden initially -->
    <div id="box1" class="clickable-area red-box-2" onclick="alert('Box 1 clicked!')"></div>
    <div id="box2" class="clickable-area red-box-2" onclick="alert('Box 2 clicked!')"></div>
    <div id="box3" class="clickable-area red-box-2" onclick="alert('Box 3 clicked!')"></div>
    <div id="box4" class="clickable-area red-box-2" onclick="alert('Box 4 clicked!')"></div>
    <div id="box5" class="clickable-area red-box-2" onclick="alert('Box 5 clicked!')"></div>
    <div id="box6" class="clickable-area red-box-2" onclick="alert('Box 6 clicked!')"></div>
    <div id="box7" class="clickable-area red-box-2" onclick="alert('Box 7 clicked!')"></div>
  </div>

  <script>
    function changeImage() {{
      // Change the image to 2.png
      document.getElementById("main-image").src = "data:image/png;base64,{image2_base64}";
      // Hide the single red box
      document.getElementById("red-box").style.display = "none";
      // Show all seven boxes
      const boxes = document.getElementsByClassName('red-box-2');
      for(let i=0; i < boxes.length; i++) {{
        boxes[i].style.display = 'block';
      }}
    }}
  </script>
</body>
</html>
"""


title = "No Hunger"      # "" for variable
st.title(title)

text = """
Help people who are starving. Give them food. The more people you help you get you earn "Thank You Points". 
With that you can buy other foods which will make you more points.
"""
st.write(text)
st.write("")


st.components.v1.html(html_code, height=700)
