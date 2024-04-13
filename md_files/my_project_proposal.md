# Project Proposal | Marvel Comics

## Get Started

### Description

Develop a website exploring Marvel comics and characters using the Marvel API. Implement CRUD for comics, characters, and user profiles. Each user can create a profile, save favorite pages (characters/comics), post and share thoughts, and like/unlike other users' posts.

### Tech Stack

**Back-end**

- Python, Flask
- PostgreSQL, SQLAlchemy
- Render
- Jinja
- RESTful APIs
- Optional: WTForms

**Front-end**

- HTML,CSS
- Javascript

### Type

Website

### Goal

Providing Marvel Fans with a platform to explore Marvel comics and characters. Users can create profiles, save the comics or characters to their favourite page, share thoughts (uploading posts), like/unlike other's posts and write comments.

### Users

Marvels fans are the users of my website. The community will grow big because the platform provide them the opportunity to engage with other fans (uploading posts, like/unlike other's posts and write comments)

### Data

Data and information about comics and characters will be sourced from the Marvel API. The app will implement the database with CRUD operations to manage the data.

## Breaking down my project

1. **Design Database Schema**
   - Determine models and database for comics, characters, users, posts, and comments.
   - [Link](https://github.com/hatchways-community/capstone-project-one-b55fdef6504c42a3b10c778802a027e5/blob/05a58a58e31242ef888d274be718d7206900a84e/Capstone%20Project-%20database%20schema%20.png)
2. **Source the data**
   - Connect to the Marvel API to fetch information about comics, characters, and related content
   - [Link](https://developer.marvel.com/)
3. **User Flows**
   - Users will be able to create their profiles, explore Marvel comics/characters, save favorites, post, like/unlike other's posts and write comments
   - [Link](https://github.com/hatchways-community/capstone-project-one-b55fdef6504c42a3b10c778802a027e5/blob/05a58a58e31242ef888d274be718d7206900a84e/app.py)
4. **Set up backend and database**
   - Configure Flask environment varialbes for development.
   - Set up PostgreSQL database and SQLAlchemy integration
   - [Link](https://github.com/hatchways-community/capstone-project-one-b55fdef6504c42a3b10c778802a027e5/blob/05a58a58e31242ef888d274be718d7206900a84e/models.py)
5. **Set up fontend**
   - Set up frontend framework, connecting it to the backend through simple API calls.
   - [Link](https://github.com/hatchways-community/capstone-project-one-b55fdef6504c42a3b10c778802a027e5)
6. **User Authentication**
   - Implement user authentication (login, logout, signup)
   - [Link](https://github.com/hatchways-community/capstone-project-one-b55fdef6504c42a3b10c778802a027e5/blob/05a58a58e31242ef888d274be718d7206900a84e/app.py)
