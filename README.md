# Blender Add-on Explorer

Blender Add-on Explorer is a Streamlit web app that helps Blender learners and developers discover high-quality add-ons from GitHub. It focuses on add-ons tagged with the `blender-addon` topic and makes it easy to filter by stars, last update date, and programming language.

## Features

- Search GitHub for repositories tagged as Blender add-ons.
- Filter by minimum stars, sort order (Stars, Last Updated, Forks), and recent updates.
- Explore add-ons in an interactive table with rank, description, and direct links.
- See a language breakdown chart for the add-ons currently in view.
- View a simple map of cities associated with Blender HQ and major community events.

## Getting Started

### Prerequisites

- Python 3.9 or later
- pip (Python package manager)

### Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
pip install streamlit pandas requests
```

### Running the app

From the project root, run:

```bash
streamlit run app.py
```

Then open the local URL that Streamlit prints in your terminal (usually `http://localhost:8501`).

## How to Use

1. Set filters in the sidebar:
    - Enter an optional keyword.
    - Choose a minimum star count.
    - Pick sort order (Stars, Last Updated, Forks).
    - Decide whether to only show add-ons updated in the last 12 months.
    - Optionally filter by programming language.

2. Click **“Search GitHub for Blender add-ons…”** to load and update the results.

3. Browse the **Add-on Catalog** table:
    - Each row shows the repository name, description, stars, forks, language, last updated, and GitHub URL.
    - The rank index helps compare add-ons at a glance.

4. Scroll down to see:
    - **Languages used by add-ons** – a summary of the top 3 languages plus “Other”.
    - **Blender Developers and Community Events** – a small map highlighting cities tied to Blender HQ and conference locations.

## Project Motivation

This app was built for an HCI course project to practice:

- Working with public APIs and real data (GitHub).
- Designing clear layouts and interactions with Streamlit.
- Supporting Blender learners who want to find well-maintained, popular add-ons while understanding the language ecosystem around Blender development.

## Future Improvements

- Integrate additional data sources for real community analytics (e.g., event APIs, community platforms).
- Add more filters (e.g., add-on categories, license types).
- Improve accessibility further (keyboard navigation, color contrast tweaks, alt text for charts).

