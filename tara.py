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
image4_base64 = get_base64_image("4.png")


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
      border: 2px solid transparent;  /* Invisible border */
      background-color: transparent;  /* Transparent background */
      cursor: pointer;
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

    .new-red-box {{
      position: absolute;
      border: 2px solid transparent;  /* Invisible border */
      display: none;
      background-color: transparent;
      cursor: pointer;
    }}

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
    <img id="main-image" src="data:image/png;base64,{image1_base64}" width="600" alt="Main Image" onclick="changeImage()">

    <div id="thank-you-box" style="display: none;">
      <span id="thank-you-points">Thank You Points: 0</span>
    </div>

    <div id="box1" class="clickable-area red-box-2" onclick="increasePoints('box1')"></div>
    <div id="box2" class="clickable-area red-box-2" onclick="increasePoints('box2')"></div>
    <div id="box3" class="clickable-area red-box-2" onclick="increasePoints('box3')"></div>
    <div id="box4" class="clickable-area red-box-2" onclick="increasePoints('box4')"></div>
    <div id="box5" class="clickable-area red-box-2" onclick="increasePoints('box5')"></div>
    <div id="box6" class="clickable-area red-box-2" onclick="increasePoints('box6')"></div>
  </div>

  <script>
    let points = 0;
    let breadClicked = false;
    let currentImage = "1";

    function changeImage() {{
      if (currentImage === "1") {{
        document.getElementById("main-image").src = "data:image/png;base64,{image2_base64}";
        currentImage = "2";

        let redBoxes = document.getElementsByClassName("red-box-2");
        for (let i = 0; i < redBoxes.length; i++) {{
          redBoxes[i].style.display = "block";
        }}

        document.getElementById("thank-you-box").style.display = "block";
      }}
    }}

    function increasePoints(boxId) {{
      if (boxId === "box2") {{
        breadClicked = true;
        return;
      }}

      if (breadClicked && boxId !== "box7") {{
        points++;
        document.getElementById("thank-you-points").textContent = "Thank You Points: " + points;
        breadClicked = false;

        if (points === 20) {{
          document.getElementById("main-image").src = "data:image/png;base64,{image4_base64}";
          currentImage = "4";

          let redBoxes = document.getElementsByClassName("red-box-2");
          for (let i = 0; i < redBoxes.length; i++) {{
            redBoxes[i].style.display = "none";
          }}
        }}
      }}
    }}

    function goToImage3() {{
      document.getElementById("main-image").src = "data:image/png;base64,{image4_base64}";
      currentImage = "4";

      let redBoxes = document.getElementsByClassName("red-box-2");
      for (let i = 0; i < redBoxes.length; i++) {{
        redBoxes[i].style.display = "none";
      }}

      let newBoxes = document.getElementsByClassName("new-red-box");
      for (let i = 0; i < newBoxes.length; i++) {{
        newBoxes[i].style.display = "block";
      }}
    }}

    function clickNewBox(boxId) {{
      // Optional: behavior for boxes in 3.png
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
