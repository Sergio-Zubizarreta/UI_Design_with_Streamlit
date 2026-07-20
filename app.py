import streamlit as st
import pandas as pd
import requests

# ---------------------------
# Page config
# ---------------------------
st.set_page_config(
    page_title="Blender Add-on Explorer",
    layout="wide",
)

st.title("Blender Add-on Explorer")
st.write(
    "Browse curated Blender add-ons from GitHub using interactive filters. "
    "Results are based on repositories tagged with the GitHub topic `blender-addon`."
)

# ---------------------------
# Session state: track if user has searched
# ---------------------------
if "has_searched" not in st.session_state:
    st.session_state.has_searched = False

# ---------------------------
# Sidebar controls
# ---------------------------
with st.sidebar:
    st.header("Search & Filters")

    keyword = st.text_input("Keyword")

    min_stars = st.slider("Minimum stars", 0, 5000, 50)

    sort_by = st.radio("Sort by", ["Stars", "Last Updated", "Forks"])

    only_recent = st.checkbox(
        "Only show add-ons updated in the last 12 months",
        value=True,
    )

    language_filter = st.multiselect(
        "Programming language",
        options=["Python", "C++", "None", "Other"],
        default=[],
        help="Choose one or more languages used by the add-ons.",
        key="language_filter",
    )

search_button = st.button("Search GitHub for Blender add-ons…")

# When the button is clicked, remember that a search has occurred
if search_button:
    st.session_state.has_searched = True

# ---------------------------
# Helper: build GitHub query URL
# ---------------------------
def build_github_url(keyword: str, sort_by: str, per_page: int) -> str:
    base_query = "topic:blender-addon"
    if keyword:
        base_query += f"+{keyword}"

    sort_param = "stars"
    if sort_by == "Last Updated":
        sort_param = "updated"
    elif sort_by == "Forks":
        sort_param = "forks"

    url = (
        "https://api.github.com/search/repositories"
        f"?q={base_query}"
        f"&sort={sort_param}"
        "&order=desc"
        f"&per_page={per_page}"
    )
    return url


# ---------------------------
# Main logic: call GitHub and return DataFrame
# ---------------------------
def fetch_repos(keyword: str, sort_by: str, per_page: int = 50) -> pd.DataFrame:
    url = build_github_url(keyword, sort_by, per_page)
    try:
        response = requests.get(url)
        if response.status_code != 200:
            st.error(
                f"GitHub API returned status {response.status_code}. "
                "You may have hit a rate limit or used an invalid query."
            )
            return pd.DataFrame()

        data = response.json().get("items", [])

        rows = []
        for item in data:
            rows.append(
                {
                    "Name": item.get("full_name"),
                    "Description": item.get("description"),
                    "Stars": item.get("stargazers_count", 0),
                    "Forks": item.get("forks_count", 0),
                    "Language": item.get("language") or "None",
                    "Last Updated": item.get("updated_at"),
                    "URL": item.get("html_url"),
                }
            )

        df = pd.DataFrame(rows)

        df = df[df["Stars"] >= min_stars]

        return df

    except Exception as e:
        st.exception(e)
        return pd.DataFrame()


# ------------------------------
# Show either initial message or results
# ------------------------------
if not st.session_state.has_searched:
    # No search yet in this session
    st.info(
        "Set your filters in the sidebar, then click "
        "'Search GitHub for Blender add-ons…' to load data from GitHub."
    )

else:
    # We are in “results mode”: use current filters every rerun
    st.info("Searching GitHub for Blender add-ons...")

    repos_df = fetch_repos(keyword=keyword, sort_by=sort_by, per_page=50)

    if repos_df.empty:
        st.warning(
            "No repositories were found. "
            "Try lowering the minimum stars or changing the keyword."
        )
    else:
        filtered_df = repos_df.copy()

        # Checkbox: only show add-ons updated in the last 12 months
        if only_recent:
            one_year_ago = pd.Timestamp.utcnow() - pd.Timedelta(days=365)
            filtered_df["Last Updated"] = pd.to_datetime(
                filtered_df["Last Updated"], utc=True
            )
            filtered_df = filtered_df[filtered_df["Last Updated"] >= one_year_ago]

        # Multiselect: filter by programming language
        if language_filter:
            filtered_df = filtered_df[filtered_df["Language"].isin(language_filter)]

        if filtered_df.empty:
            st.warning(
                "No repositories matched your filters. "
                "Try changing the recency or language filters."
            )
        else:
            # Rank index
            filtered_df = filtered_df.reset_index(drop=True)
            filtered_df.index = filtered_df.index + 1
            filtered_df.index.name = "Rank"

            # Description header hint
            filtered_df.rename(
                columns={"Description": "Description (double-click cell to expand)"},
                inplace=True,
            )

            st.success(f"Found {len(filtered_df)} repositories after filtering.")

            # Interactive table
            st.subheader("Add-on Catalog (GitHub)")
            st.dataframe(
                filtered_df,
                use_container_width=True,
            )

            # -------- Languages used by add-ons (top 3 + other) --------
            st.subheader("Languages used by add-ons")

            language_counts = filtered_df["Language"].value_counts()
            total = int(language_counts.sum())
            percentages = (language_counts / total * 100).round(1)

            sorted_pct = percentages.sort_values(ascending=False)
            top3 = sorted_pct.head(3)
            other_pct = 100 - float(top3.sum())

            summary_df = top3.to_frame(name="Percent")
            summary_df.index.name = "Language"
            if other_pct > 0:
                summary_df.loc["Other"] = other_pct

            col_text, col_chart, col_spacer = st.columns([1.5, 2.5, 1])

            with col_text:
                lines = [f"- Total add-ons in view: **{total}**"]
                for lang, pct in top3.items():
                    lines.append(f"- {lang} share: **{pct}%**")
                if other_pct > 0:
                    lines.append(f"- Other languages combined: **{other_pct:.1f}%**")
                st.markdown("\n".join(lines))

            with col_chart:
                st.bar_chart(summary_df)

            # -------- Map: Blender Developers and Community Events --------
            st.subheader("Blender Developers and Community Events")

            map_data = pd.DataFrame(
                {
                    "lat": [52.37, 52.37, 30.27],   # Amsterdam, Amsterdam, Austin
                    "lon": [4.90, 4.89, -97.74],
                }
            )

            st.map(map_data)

            st.caption(
                "This map highlights cities associated with Blender HQ and major community events, "
                "such as conferences in Amsterdam and North America."
            )

            # Placeholder for future charts / maps
            st.subheader("Next steps")
            st.write(
                "- Create charts using the Stars and Forks columns.\n"
                "- Add more event locations or user data based on usability testing.\n"
                "- Refine filters and layout based on feedback from Blender learners."
            )