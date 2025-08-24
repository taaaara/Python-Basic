import re
from urllib.parse import urlparse
import streamlit as st

st.set_page_config(page_title="My Roblox Links Dashboard", page_icon="🎮", layout="wide")
st.title("🎮 My Roblox Links Dashboard")

LINKS = [
    "https://www.roblox.com/ko/games/79546208627805/99-Nights-in-the-Forest",
    "https://www.roblox.com/ko/games/126884695634066/Grow-a-Garden",
    "https://www.roblox.com/ko/games/17625359962/RIVALS",
    "https://www.roblox.com/ko/games/6445435958/잼못타",
    "https://www.roblox.com/ko/games/109983668079237/Steal-a-Brainrot",
    "https://www.roblox.com/ko/games/6737970321/Livetopia-RP",
    "https://www.roblox.com/ko/games/6104994594/Pilfering-Pirates"
]

def extract_name(url: str) -> str:
    try:
        path = urlparse(url).path.strip("/")
        parts = path.split("/")
        if len(parts) >= 3 and parts[0].lower() == "games":
            return parts[2].replace("-", " ")
        return parts[-1].replace("-", " ") if parts else url
    except Exception:
        return url

# Initialize favorites state
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

# Pink aesthetic theme
st.markdown("""
<style>
.game-card {
    display:flex;flex-direction:column;
    justify-content:center;align-items:center;
    width:100%;height:220px;
    border:2px solid #f8bbd0; 
    border-radius:16px;
    box-shadow:2px 2px 8px rgba(255,182,193,0.4);
    background: #ffe4ec;
    transition: all 0.3s ease;
    padding: 10px;
    margin-bottom:10px;
}
.game-card:hover {
    transform: scale(1.05);
    box-shadow:4px 4px 14px rgba(255,105,180,0.6);
    border-color:#f48fb1;
}
.game-button {
    padding:6px 14px;
    border-radius:8px;
    background-color:#fce4ec;
    color:#d81b60 !important;
    text-decoration:none !important;
    font-weight:bold;
    border: 2px solid #f8bbd0;
    display:inline-block;
}
.game-button:hover {
    background-color:#f8bbd0;
    color:#ad1457 !important;
}
.fav-btn {
    font-size:20px;
    border:none;
    background:none;
    cursor:pointer;
    margin-top:8px;
}
</style>
""", unsafe_allow_html=True)

# ---- Favorites Section ----
favorite_games = [link for link in LINKS if st.session_state.favorites.get(extract_name(link), False)]
if favorite_games:
    st.subheader("❤️ Favorites")
    cols_per_row = 3
    for i in range(0, len(favorite_games), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, link in zip(cols, favorite_games[i:i+cols_per_row]):
            name = extract_name(link)
            with col:
                st.markdown(f"""
                <div class="game-card">
                    <div style="font-size:16px;font-weight:bold;color:#333;margin-bottom:8px;">
                        {name}
                    </div>
                    <a href="{link}" target="_blank" class="game-button">Open Game</a>
                </div>
                """, unsafe_allow_html=True)
                # Favorite heart toggle
                fav_state = st.session_state.favorites[name]
                heart_symbol = "♥" if fav_state else "♡"
                if st.button(heart_symbol, key=f"fav_{name}"):
                    st.session_state.favorites[name] = not st.session_state.favorites[name]

# ---- Display All Games ----
st.subheader("All Games")
if not LINKS:
    st.info("Add Roblox game links to the LINKS list at the top of the code.")
else:
    cols_per_row = 3
    for i in range(0, len(LINKS), cols_per_row):
        cols = st.columns(cols_per_row)
        for col, link in zip(cols, LINKS[i:i+cols_per_row]):
            name = extract_name(link)
            # Skip favorites (already shown)
            if st.session_state.favorites.get(name, False):
                continue
            if name not in st.session_state.favorites:
                st.session_state.favorites[name] = False

            with col:
                st.markdown(f"""
                <div class="game-card">
                    <div style="font-size:16px;font-weight:bold;color:#333;margin-bottom:8px;">
                        {name}
                    </div>
                    <a href="{link}" target="_blank" class="game-button">Open Game</a>
                </div>
                """, unsafe_allow_html=True)
                # Favorite heart toggle
                fav_state = st.session_state.favorites[name]
                heart_symbol = "♥" if fav_state else "♡"
                if st.button(heart_symbol, key=f"fav_{name}"):
                    st.session_state.favorites[name] = not st.session_state.favorites[name]
