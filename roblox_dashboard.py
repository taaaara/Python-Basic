import os
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
from dateutil import parser

# Optional: KaggleHub fallback
try:
    import kagglehub
    KAGGLEHUB_AVAILABLE = True
except Exception:
    KAGGLEHUB_AVAILABLE = False

st.set_page_config(page_title="Roblox Games Dashboard", page_icon="🎮", layout="wide")

PREFERRED_CSV_NAME = "roblox_games.csv"

# -------------------------------
# Loading
# -------------------------------
@st.cache_data(show_spinner=True)
def load_dataframe_prefer_local():
    if os.path.exists(PREFERRED_CSV_NAME):
        df = pd.read_csv(PREFERRED_CSV_NAME)
        return df, os.path.abspath(PREFERRED_CSV_NAME)

    if not KAGGLEHUB_AVAILABLE:
        raise FileNotFoundError(
            f"'{PREFERRED_CSV_NAME}' not found and kagglehub unavailable. "
            "Place the CSV in the working folder or install kagglehub."
        )

    path = kagglehub.dataset_download("biggiefats/roblox-games-dataset")
    exact = os.path.join(path, PREFERRED_CSV_NAME)
    if os.path.exists(exact):
        return pd.read_csv(exact), exact

    # Auto-pick a likely CSV
    cands = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.lower().endswith(".csv"):
                full = os.path.join(root, f)
                cands.append((full, os.path.getsize(full)))
    if not cands:
        raise FileNotFoundError("No CSV found under KaggleHub cache path.")

    def score(name, size):
        n = name.lower()
        s = 0
        if "roblox" in n: s += 3
        if "game" in n or "games" in n: s += 2
        if "dataset" in n or "top" in n or "1000" in n: s += 1
        return (s, size)

    cands.sort(key=lambda x: score(os.path.basename(x[0]), x[1]), reverse=True)
    csv_path = cands[0][0]
    return pd.read_csv(csv_path), csv_path

# -------------------------------
# Auto-mapping
# -------------------------------
CANON = {
    "name": ["name", "title", "game", "game_name"],
    "creator": ["creator", "developer", "author", "studio"],
    "genre": ["genre", "genres", "category", "categories", "type"],
    "visits": ["visits", "visit", "plays", "playcount", "total_visits", "placevisits", "visitslifetime"],
    "active": ["active", "playing", "players_active", "current_players", "concurrent"],
    "favorites": ["favorites", "favourites", "favorite_count", "favourites_count"],
    "likes": ["likes", "upvotes", "thumbs_up", "likes_count"],
    "dislikes": ["dislikes", "downvotes", "thumbs_down", "dislikes_count"],
    "rating": ["rating", "like_ratio", "score", "upvote_ratio"],
    "age": ["age", "age_rating", "age_recommendation"],
    "desc": ["description", "desc", "about"],
    "created": ["created", "release_date", "published"],
    "updated": ["updated", "last_update", "last_updated", "updated_at"],
    "id": ["id", "game_id", "place_id"]
}

def find_col(df, keys):
    cols = {c.lower(): c for c in df.columns}
    for k in keys:
        k = k.lower()
        if k in cols:
            return cols[k]
        for lc, orig in cols.items():
            if k in lc:
                return orig
    return None

def build_map(df):
    return {k: find_col(df, v) for k, v in CANON.items()}

def to_datetime_safe(s):
    try:
        return pd.to_datetime(s, errors="coerce", utc=True)
    except Exception:
        try:
            return s.apply(lambda x: parser.parse(str(x)) if pd.notna(x) else pd.NaT)
        except Exception:
            return pd.to_datetime(pd.Series([pd.NaT]*len(s)))

# -------------------------------
# Robust numeric cleaning
# -------------------------------
def parse_number_like(x, is_ratio=False):
    """
    Convert strings like '1,234', '2.5M', '45K', '1,002+', '—', 'N/A', '95%' to float.
    - is_ratio=True: '95%' -> 0.95; plain numbers kept as-is.
    """
    if pd.isna(x):
        return np.nan
    if isinstance(x, (int, float, np.integer, np.floating)):
        return float(x)

    s = str(x).strip()
    if s == "" or s.lower() in {"nan", "none", "null", "n/a", "na", "-", "—"}:
        return np.nan

    # Percent to ratio
    if is_ratio and s.endswith("%"):
        try:
            return float(s[:-1].replace(",", "").strip()) / 100.0
        except Exception:
            return np.nan

    # Remove commas, spaces, plus signs
    s = s.replace(",", "").replace(" ", "").replace("+", "")

    # K/M/B suffix
    mult = 1.0
    if s[-1:].lower() == "k":
        mult = 1e3; s = s[:-1]
    elif s[-1:].lower() == "m":
        mult = 1e6; s = s[:-1]
    elif s[-1:].lower() == "b":
        mult = 1e9; s = s[:-1]

    try:
        return float(s) * mult
    except Exception:
        return np.nan

def clean_numeric_series(series, is_ratio=False):
    return series.apply(lambda v: parse_number_like(v, is_ratio=is_ratio))

def safe_series(df, col, default=0.0):
    return df[col].astype(float).fillna(default) if (col and col in df.columns) else pd.Series([default]*len(df))

# Helpers to pick a usable numeric column (has finite values)
def pick_numeric_column(fdf, candidates):
    for c in candidates:
        if c and c in fdf.columns:
            s = pd.to_numeric(fdf[c], errors="coerce")
            if np.isfinite(s).sum() > 0:
                return c
    return None

def finite_min_max(series, fallback=(0.0, 1.0)):
    s = pd.to_numeric(series, errors="coerce")
    s = s[np.isfinite(s)]
    if len(s) == 0:
        return fallback
    return float(np.floor(s.min())), float(np.ceil(max(s.max(), 1.0)))

# -------------------------------
# Load data
# -------------------------------
try:
    df_raw, src_path = load_dataframe_prefer_local()
    st.success(f"✅ Dataset loaded — Source: {src_path}")
except Exception as e:
    st.error(f"Failed to load dataset: {e}")
    st.stop()

df = df_raw.copy()
colmap = build_map(df)

# -------------------------------
# Preprocess
# -------------------------------
# Name
name_col = colmap["name"] or df.columns[0]
df.rename(columns={name_col: "_name"}, inplace=True)

# Datetime
for key in ["created", "updated"]:
    c = colmap[key]
    if c and c in df.columns:
        df[c] = to_datetime_safe(df[c])

# Genre list (with fallback)
genre_col = colmap["genre"]
if genre_col and genre_col in df.columns:
    df["_genre_list"] = (
        df[genre_col].astype(str)
        .str.replace(r"\[|\]|'", "", regex=True)
        .str.replace(";", ",")
        .str.split(",")
        .apply(lambda xs: [x.strip() for x in xs if x and x.strip().lower() not in ["nan", "none", ""]])
    )
else:
    df["_genre_list"] = [[] for _ in range(len(df))]
if df["_genre_list"].apply(len).sum() == 0:
    df["_genre_list"] = [["(Unknown)"] for _ in range(len(df))]

# Numeric columns — CLEAN with parser
NUM_KEYS = ["visits", "active", "favorites", "likes", "dislikes"]
for key in NUM_KEYS:
    c = colmap[key]
    if c and c in df.columns:
        df[c] = clean_numeric_series(df[c], is_ratio=False)

# Rating — CLEAN (handle percentages like "95%") or derive
if colmap["rating"] and colmap["rating"] in df.columns:
    df["_rating"] = clean_numeric_series(df[colmap["rating"]], is_ratio=True)
else:
    if colmap["likes"] and colmap["dislikes"]:
        likes = df[colmap["likes"]] if colmap["likes"] in df.columns else pd.Series([np.nan]*len(df))
        dislikes = df[colmap["dislikes"]] if colmap["dislikes"] in df.columns else pd.Series([np.nan]*len(df))
        df["_rating"] = np.where((likes + dislikes) > 0, likes / (likes + dislikes), np.nan)
    else:
        df["_rating"] = np.nan

# -------------------------------
# Sidebar filters
# -------------------------------
st.sidebar.title("🔎 Filters")

# Genres (exclude "(Unknown)" by default if real values exist)
all_genres = sorted({g for lst in df["_genre_list"] for g in lst}) or ["(Unknown)"]
real_genres = [g for g in all_genres if g != "(Unknown)"]
default_genres = real_genres if len(real_genres) > 0 else all_genres
sel_genres = st.sidebar.multiselect("Genres", options=all_genres, default=default_genres)

# Creators (default ALL)
creator_col = colmap["creator"]
if creator_col and creator_col in df.columns:
    creators = sorted(df[creator_col].astype(str).fillna("Unknown").unique().tolist())
    sel_creators = st.sidebar.multiselect("Creators", options=creators, default=creators)
else:
    sel_creators = []

# Age ratings (exclude "Unknown" by default if real values exist)
age_col = colmap["age"]
if age_col and age_col in df.columns:
    ages = sorted(df[age_col].astype(str).fillna("Unknown").unique().tolist())
    real_ages = [a for a in ages if a.lower() not in {"unknown", ""}]
    default_ages = real_ages if len(real_ages) > 0 else ages
    sel_ages = st.sidebar.multiselect("Age ratings", options=ages, default=default_ages)
else:
    sel_ages = []

# Ranges (finite-only guards)
vmin, vmax = finite_min_max(df[colmap["visits"]]) if colmap["visits"] and colmap["visits"] in df.columns else (0.0, 1.0)
amin, amax = finite_min_max(df[colmap["active"]]) if colmap["active"] and colmap["active"] in df.columns else (0.0, 1.0)
rmin, rmax = finite_min_max(df["_rating"], fallback=(0.0, 1.0))
vr = st.sidebar.slider("Visits range", min_value=vmin, max_value=vmax, value=(vmin, vmax))
ar = st.sidebar.slider("Active players range", min_value=amin, max_value=amax, value=(amin, amax))
rr = st.sidebar.slider("Rating (0–1)", 0.0, 1.0, value=(max(0.0, rmin), min(1.0, rmax)))

# Dates
date_col = (colmap["updated"] if (colmap["updated"] and colmap["updated"] in df.columns) else colmap["created"])
if date_col and date_col in df.columns and pd.api.types.is_datetime64_any_dtype(df[date_col]):
    min_d = pd.to_datetime(df[date_col]).min().date()
    max_d = pd.to_datetime(df[date_col]).max().date()
    dr = st.sidebar.date_input("Date range", (min_d, max_d), min_value=min_d, max_value=max_d)
else:
    dr = None

search_text = st.sidebar.text_input("Search (game/creator, substring)", "")

# -------------------------------
# Apply filters
# -------------------------------
mask = pd.Series([True]*len(df))
if sel_genres:
    mask &= df["_genre_list"].apply(lambda lst: any(g in lst for g in sel_genres))
if sel_creators and (creator_col and creator_col in df.columns):
    mask &= df[creator_col].astype(str).isin(sel_creators)
if sel_ages and (age_col and age_col in df.columns):
    mask &= df[age_col].astype(str).isin(sel_ages)
if colmap["visits"] and colmap["visits"] in df.columns:
    mask &= df[colmap["visits"]].fillna(0).between(vr[0], vr[1])
if colmap["active"] and colmap["active"] in df.columns:
    mask &= df[colmap["active"]].fillna(0).between(ar[0], ar[1])
mask &= df["_rating"].fillna(0).between(rr[0], rr[1])

if dr and isinstance(dr, tuple) and len(dr) == 2 and (date_col and date_col in df.columns):
    start_d = pd.to_datetime(dr[0])
    end_d = pd.to_datetime(dr[1]) + pd.Timedelta(days=1)
    mask &= (df[date_col] >= start_d) & (df[date_col] < end_d)

if search_text.strip():
    s = search_text.lower().strip()
    name_hit = df["_name"].astype(str).str.lower().str.contains(s)
    if creator_col and creator_col in df.columns:
        creator_hit = df[creator_col].astype(str).str.lower().str.contains(s)
        mask &= (name_hit | creator_hit)
    else:
        mask &= name_hit

fdf = df.loc[mask].copy()
using_fallback_data = False

# If no rows after filtering, auto-fallback to full data so charts still show
if len(fdf) == 0:
    using_fallback_data = True
    st.warning("No rows match the current filters. Charts below use the **unfiltered dataset** for visibility.")
    fdf = df.copy()

# -------------------------------
# KPIs
# -------------------------------
st.title("🎮 Roblox Games Dashboard")
st.caption("Source: ./roblox_games.csv (preferred). Falls back to KaggleHub if missing.")

def fmt_int_maybe(x):
    return f"{int(x):,}" if pd.notna(x) and np.isfinite(x) else "N/A"

def fmt_float_maybe(x, ndigits=2):
    return f"{round(float(x), ndigits):.{ndigits}f}" if pd.notna(x) and np.isfinite(x) else "N/A"

shown_count   = len(fdf) if not using_fallback_data else len(df)
total_visits  = (fdf[colmap["visits"]].sum() if colmap["visits"] and colmap["visits"] in fdf.columns else np.nan)
avg_rating    = fdf["_rating"].mean()
median_active = (fdf[colmap["active"]].median() if colmap["active"] and colmap["active"] in fdf.columns else np.nan)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Games shown", f"{shown_count:,}")
c2.metric("Total visits", fmt_int_maybe(total_visits))
c3.metric("Avg rating (0–1)", fmt_float_maybe(avg_rating, 2))
c4.metric("Median active players", fmt_int_maybe(median_active))

st.divider()

# -------------------------------
# Tabs
# -------------------------------
t_over, t_genre, t_creator, t_rating, t_time, t_table = st.tabs(
    ["Overview", "Genres", "Creators", "Rating & Popularity", "Timeline", "Table"]
)

# ===== Overview =====
with t_over:
    lc, rc = st.columns((2, 1), gap="large")

    # Pick a usable ranking metric with finite values
    rank_col = pick_numeric_column(
        fdf, [colmap.get("visits"), colmap.get("favorites"), colmap.get("likes"), colmap.get("active")]
    )

    if rank_col and len(fdf) > 0:
        nmax = int(min(30, max(1, len(fdf))))
        topn = st.slider("Top N (by ranking metric)", 1, nmax, min(10, nmax))
        top_df = fdf.sort_values(rank_col, ascending=False).head(topn)
        fig = px.bar(top_df, x=rank_col, y="_name", orientation="h",
                     title=f"Top {topn} (metric: {rank_col})",
                     labels={rank_col: rank_col, "_name": "Game"})
        fig.update_yaxes(categoryorder="total ascending")
        lc.plotly_chart(fig, use_container_width=True)
    else:
        lc.info("No numeric metric available to render the ranking chart.")

    # Scatter x-axis: strongest fallback among finite columns
    x_col = pick_numeric_column(
        fdf, [colmap.get("visits"), rank_col, colmap.get("favorites"), colmap.get("active"), colmap.get("likes")]
    )
    if x_col and len(fdf) > 0:
        size_col = pick_numeric_column(fdf, [colmap.get("favorites")])
        scatter = px.scatter(
            fdf, x=x_col, y="_rating",
            size=size_col if size_col else None,
            hover_name="_name",
            title=f"{x_col} vs rating" + (" (bubble = favorites)" if size_col else ""),
            labels={x_col: x_col, "_rating": "Rating (0–1)"}
        )
        rc.plotly_chart(scatter, use_container_width=True)
    else:
        rc.info("No numeric metric available for scatter plot.")

# ===== Genres =====
with t_genre:
    exploded = fdf.explode("_genre_list")
    if len(exploded) == 0:
        st.info("No data to display. Adjust filters.")
    else:
        visits_col = pick_numeric_column(exploded, [colmap.get("visits")])
        if visits_col:
            gsum = (exploded.groupby("_genre_list", as_index=False)
                    .agg(games=("_name","nunique"),
                         visits=(visits_col,"sum"),
                         avg_rating=("_rating","mean")))
        else:
            gsum = (exploded.groupby("_genre_list", as_index=False)
                    .agg(games=("_name","nunique"),
                         visits=("_name","count"),
                         avg_rating=("_rating","mean")))
        gsum = gsum.dropna(subset=["_genre_list"]).rename(columns={"_genre_list":"genre"})
        gsum = gsum.sort_values("visits", ascending=False)

        c1, c2 = st.columns(2)
        c1.dataframe(gsum.head(30), use_container_width=True, height=380)
        if len(gsum):
            bar = alt.Chart(gsum.head(20)).mark_bar().encode(
                x=alt.X("visits:Q", title="Visits"),
                y=alt.Y("genre:N", sort="-x", title="Genre"),
                tooltip=["genre", "games", "visits", "avg_rating"]
            ).properties(title="Top 20 genres by visits", height=380)
            c2.altair_chart(bar, use_container_width=True)

# ===== Creators =====
with t_creator:
    if creator_col and creator_col in fdf.columns and len(fdf) > 0:
        visits_col = pick_numeric_column(fdf, [colmap.get("visits")])
        if visits_col:
            csum = (fdf.groupby(creator_col, as_index=False)
                    .agg(games=("_name","nunique"),
                         visits=(visits_col,"sum"),
                         avg_rating=("_rating","mean"),
                         favs=(colmap["favorites"],"sum") if (colmap["favorites"] and colmap["favorites"] in fdf.columns) else ("_name","count")))
        else:
            csum = (fdf.groupby(creator_col, as_index=False)
                    .agg(games=("_name","nunique"),
                         visits=("_name","count"),
                         avg_rating=("_rating","mean"),
                         favs=(colmap["favorites"],"sum") if (colmap["favorites"] and colmap["favorites"] in fdf.columns) else ("_name","count")))
        csum = csum.sort_values("visits", ascending=False)
        st.dataframe(csum.head(100), use_container_width=True, height=420)

        pick = st.multiselect("Compare creators (up to ~5 recommended)",
                              csum[creator_col].head(20).tolist(),
                              default=csum[creator_col].head(3).tolist())
        if pick:
            comp_base = fdf[fdf[creator_col].isin(pick)]
            if visits_col:
                comp = (comp_base.groupby([creator_col])
                        .agg(visits=(visits_col, "sum"),
                             avg_rating=("_rating","mean"),
                             games=("_name","nunique"))
                        .reset_index())
            else:
                comp = (comp_base.groupby([creator_col])
                        .agg(visits=("_name","count"),
                             avg_rating=("_rating","mean"),
                             games=("_name","nunique"))
                        .reset_index())
            figc = px.bar(comp, x="visits", y=creator_col, color=creator_col,
                          title="Visits by selected creators", orientation="h",
                          labels={"visits":"Visits"})
            st.plotly_chart(figc, use_container_width=True)
    else:
        st.info("No creator column found or no data to display.")

# ===== Rating & Popularity =====
with t_rating:
    left, right = st.columns(2)
    if len(fdf) > 0:
        hist = px.histogram(fdf, x="_rating", nbins=30, title="Rating distribution (0–1)", labels={"_rating":"Rating"})
        left.plotly_chart(hist, use_container_width=True)

        fav_col = pick_numeric_column(fdf, [colmap.get("favorites")])
        vis_col = pick_numeric_column(fdf, [colmap.get("visits")])
        if fav_col and vis_col:
            sc2 = px.scatter(fdf, x=fav_col, y=vis_col, hover_name="_name",
                             title="Favorites vs visits",
                             labels={fav_col:"Favorites", vis_col:"Visits"})
            right.plotly_chart(sc2, use_container_width=True)
        else:
            right.info("Favorites/visits columns are missing for the scatter plot.")
    else:
        left.info("No data to display. Adjust filters.")

# ===== Timeline =====
with t_time:
    date_col_valid = (colmap["updated"] if (colmap["updated"] and colmap["updated"] in fdf.columns) else colmap["created"])
    if date_col_valid and date_col_valid in fdf.columns and pd.api.types.is_datetime64_any_dtype(fdf[date_col_valid]) and len(fdf) > 0:
        vis_col = pick_numeric_column(fdf, [colmap.get("visits")])
        td = (fdf.set_index(date_col_valid)
              .sort_index()
              .resample("W")
              .agg(visits=(vis_col,"sum") if vis_col else ("_name","count"),
                   avg_rating=("_rating","mean"))
              .reset_index())
        if len(td) > 0:
            figt = px.line(td, x=date_col_valid, y=["visits","avg_rating"],
                           title="Weekly visits / average rating",
                           labels={"value":"Value","variable":"Metric"})
            figt.update_traces(mode="lines+markers")
            st.plotly_chart(figt, use_container_width=True)
        else:
            st.info("Not enough data points to draw a timeline.")
    else:
        st.info("No valid updated/created datetime column for timeline or no data to display.")

# ===== Table =====
with t_table:
    show_cols = ["_name"]
    for key in ["creator","genre","visits","active","favorites","likes","dislikes","rating","age","created","updated","id","desc"]:
        c = colmap[key]
        if c and c not in show_cols and c in fdf.columns:
            show_cols.append(c)
    show_cols = [c for c in show_cols if c in fdf.columns]

    if len(fdf) > 0 and len(show_cols) > 0:
        sort_col = colmap["visits"] if (colmap["visits"] and colmap["visits"] in fdf.columns) else "_name"
        st.dataframe(
            fdf[show_cols].sort_values(sort_col, ascending=False),
            use_container_width=True, height=420
        )
        st.download_button(
            "⬇️ Download filtered table (CSV)",
            fdf[show_cols].to_csv(index=False).encode("utf-8-sig"),
            file_name="roblox_filtered.csv",
            mime="text/csv"
        )
    else:
        st.info("No rows/columns to display. Adjust filters or check column mappings.")

# ===== Debug =====
with st.expander("🔧 Debug info"):
    st.write("Columns:", list(df.columns))
    st.write("Auto mapping:", colmap)
    st.write("Dtypes:", df.dtypes.astype(str).to_dict())
    st.dataframe(df.head(10), use_container_width=True)