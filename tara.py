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
image3_base64 = get_base64_image("3.png")


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
    #red-box {{
      top: 100px;
      left: 175px;
      width: 235px;
      height: 115px;
    }}
    .red-box-2 {{
      display: none;
    }}
    #box1 {{ top: 30px; left: 65px; width: 70px; height: 90px; }}
    #box2 {{ top: 5px; left: 235px; width: 70px; height: 75px; }}
    #box3 {{ top: 45px; left: 475px; width: 80px; height: 80px; }}
    #box4 {{ top: 175px; left: 25px; width: 80px; height: 80px; }}
    #box5 {{ top: 200px; left: 450px; width: 80px; height: 100px; }}
    #box6 {{ top: 150px; left: 270px; width: 45px; height: 80px; }}
    #box7 {{ top: 300px; left: 0px; width: 120px; height: 30px; }}
    #thank-you-box {{
      position: absolute;
      top: 10px;
      right: 10px;
      background-color: pink;
      padding: 8px 12px;
      font-weight: bold;
      border-radius: 10px;
      font-family: Arial, sans-serif;
    }}
  </style>
</head>
<body>
  <div class="container">
    <img id="main-image" src="data:image/png;base64,{image1_base64}" width="600" alt="Clickable Image">
    
    <div id="thank-you-box" style="display: none;">
      <span id="thank-you-points">Thank You Points: 0</span>
    </div>

    <div id="red-box" class="clickable-area" onclick="changeImage()"></div>

    <div id="box1" class="clickable-area red-box-2" onclick="increasePoints('box1')"></div>
    <div id="box2" class="clickable-area red-box-2" onclick="increasePoints('box2')"></div>
    <div id="box3" class="clickable-area red-box-2" onclick="increasePoints('box3')"></div>
    <div id="box4" class="clickable-area red-box-2" onclick="increasePoints('box4')"></div>
    <div id="box5" class="clickable-area red-box-2" onclick="increasePoints('box5')"></div>
    <div id="box6" class="clickable-area red-box-2" onclick="increasePoints('box6')"></div>
    <div id="box7" class="clickable-area red-box-2" onclick="goToImage3()"></div>
  </div>

  <script>
    let points = 0;
    let breadClickedFirst = false;

    function changeImage() {{
      document.getElementById("main-image").src = "data:image/png;base64,{image2_base64}";
      document.getElementById("red-box").style.display = "none";

      const boxes = document.getElementsByClassName('red-box-2');
      for (let i = 0; i < boxes.length; i++) {{
        boxes[i].style.display = 'block';
      }}

      document.getElementById("thank-you-box").style.display = "block";
    }}

    function increasePoints(boxId) {{
      if (boxId === 'box2') {{
        breadClickedFirst = true;
        return;
      }}
      if (breadClickedFirst && boxId !== 'box7') {{
        points++;
        document.getElementById("thank-you-points").textContent = "Thank You Points: " + points;
        breadClickedFirst = false;
      }}
    }}

    function goToImage3() {{
      document.getElementById("main-image").src = "data:image/png;base64,{image3_base64}";
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
