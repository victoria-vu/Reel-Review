# Reel Reviews 🎞️

Reel Reviews is a web development application for movie lovers who crave a personalized and interactive cinematic experience. Reel Reviews allows users to search for movies by title, creating a platform where they can not only discover their favorite films but actively participate in movie critiques.

## Table of Contents
1. [Technologies Used](#technologies-used)
2. [How to Run Reel Reviews Locally](#how-to-run-reel-reviews-locally)
3. [Slide Deck](#slide-deck)

## Technologies Used
- Backend: Python, Flask, SQL, PostgresQL, SQLAlchemy
- Frontend: HTML/CSS, Bootstrap, JSON, Jinja2
- APIs: The Movie Database (TMDb) API
- UI Design: Figma
- Data Model: DBDesigner
  
#### Initial Data Model:
<img width="800" alt="Reel Reviews Initial Data Model" src="https://github.com/victoria-vu/Reel-Review/assets/120001666/c4b3b6c1-619c-4536-bd20-ac2bebdc0d7e">

## How to Run Reel Reviews Locally
1. To run Reel Reviews locally, clone this repository:
```
git clone https://github.com/victoria-vu/Reel-Review.git
```
2. Create and activate a virtual environment within your terminal:
```
virtualenv env
source env/bin/activate
```
3. Install the requirements/dependencies:
```
pip3 install -r requirements.txt
```
4. Obtain a TMDb API Key from [TMDb Developer Portal](https://developer.themoviedb.org/reference/intro/getting-started).

5. Create a secrets.sh file and include the following line for the TMDb API Key:
```
export TMDB_API_KEY="[your-key-goes-here]"
```
6. Add the secrets.sh file to .gitignore and load the API key to the shell environment:
```
source secrets.sh
```
7. Set up the database:
```
python3 seed_database.py
```
8. Run the app:
```
python3 server.py
```
9. Navigate to [localhost:5000/](https:localhost:5000/) in your browser to use Reel Reviews! 🎞️


## Slide Deck
<img width="800" alt="Reel Reviews: Homepage" src="https://github.com/victoria-vu/Reel-Review/assets/120001666/6147958e-c961-4112-8653-d072579e400b">
<br>
<br>
<img width="800" alt="Reel Reviews: Log In Page" src="https://github.com/victoria-vu/Reel-Review/assets/120001666/df29d356-f9e8-468b-bca5-da471d4d4204">
<br>
<br>
<img width="800" alt="Reel Reviews: Movie Search Results" src="https://github.com/victoria-vu/Reel-Review/assets/120001666/016ef4e9-a285-4cdf-974a-7b4cd10a84e7">
<br>
<br>
<img width="800" alt="Reel Reviews: The Proposal" src="https://github.com/victoria-vu/Reel-Review/assets/120001666/2f6ec839-47ae-4840-9954-c7edd3e34c43">
<br>
<br>
<img width="800" alt="Reel Reviews: My Reviews Page" src="https://github.com/victoria-vu/Reel-Review/assets/120001666/c2f12eea-0ed2-4985-b298-0e5406586f5d">