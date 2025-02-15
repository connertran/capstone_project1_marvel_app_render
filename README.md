# Marvel App

I have broken down the Marvel App Project into easy-to-follow steps. Here’s a quick overview of what I did for each step of my Marvel project.

1. Step One: Initial Project Ideas: I’ll pick up to 3 project ideas to propose to my mentor and the Springboard community. I’ll also explore some potential APIs.
2. Step Two: Project Proposal: For this step, I’ll write a proposal for the site I want to build. This will help my mentor better understand my chosen capstone project idea.
3. Step Three: Schema Design and API Selection: After my mentor approves of my capstone project proposal, I’ll figure out the database design of my application and which API I’ll be using.
4. Step Four: Coding User Flows: Once I’ve figured out what I’m building, I’ll write the code to implement it. It’s important to think about what I want a user’s experience to be like as they navigate my site.
5. Step Five: Polishing My Application: Once I have the core functionality implemented, I’ll focus on additional UI enhancements and styling for my application.
6. Step Six: Documenting and Submission: I’ve done a lot of work so now it’s time to show my mentor my progress! Create a README in markdown, make sure my GitHub is organized, and submit my finalized project.

## Database Design:

![Database schema](Capstone-Project-database-schema.png)

## Overview

This application harnesses the power of the Marvel API to retrieve information about Marvel characters and the comics they appear in. It offers a platform where users can create personal accounts to access various features.

### Features

- Account Creation: Users can sign up to create their own accounts, enabling a personalized experience.
- Login/Logout Functionality: Secure login/logout mechanisms ensure that user sessions are individually managed and protected.
- Search Functionality: With an integrated search bar, users can easily find any Marvel character they are interested in.
- Social Interaction: The app allows users to express their thoughts and engage with the community through posting. Posts can be liked and commented on by others, fostering a vibrant and interactive environment.

This project aims to provide Marvel enthusiasts with a comprehensive tool to explore their favorite characters and comics, while also offering a platform for community interaction and sharing.

### User Flow

- Users can log in or sign up (if they haven't) for the app.
- On the homepage, users can see brief information about different characters.
- To view details of a character, users can click on individual Marvel characters.
- Users can add Marvel characters to their favorite list.
- Users can update their bio information on their personal page.
- Users can post and share their opinions.
- In the News page, users can view others' posts, like them, and leave comments.

## Tech Stack

**Back-end**

- Python, Flask
- PostgreSQL, SQLAlchemy
- Render
- Jinja
- RESTful APIs
- WTForms

**Front-end**

- HTML,CSS
- Javascript, Jquery
- AJAX (axios)

## Improvements in the Future
- Even though I finished this project, I noticed there are still improvements to be made. In the future, I plan to refactor the code in the main application file (app.py) by using Flask Blueprints.

## Marvel's API link

[Here is the link to my API.](https://developer.marvel.com/docs)

To utilize the Marvel API for fetching data, you need to follow a few essential steps to gain access:

- Login Requirement: Initially, you must log in to obtain a public key and a private key, which are crucial for making requests to the Marvel API.

- Hash Generation: To ensure secure API calls, Marvel requires a hashed value in each request. To generate this hash:

  - Visit MD5 Hash Generator.
  - Create an MD5 hash using a combination of secret_text, private_key, and public_key.
  - The secret_text is created by you, as the API user. It can be any arbitrary value.

- This hash, along with your public and private keys, will be used in all API requests to authenticate and pull data securely from Marvel's servers.

## How to set up and run the project

1. Obtain your API public key and private key from the Marvel API.
2. Create a `secret_info.py` file. Inside this file, include the following information:

   - `api_public_key`
   - `api_private_key`
   - `ts` (timestamp) or `secret_text`
   - `hashVal` (generated hash using your secret text, private key, and public key)
     Refer to the [Marvel's API link](https://developer.marvel.com/docs) section for more information about these values.

3. In the terminal, navigate to the project folder and set up the virtual environment using the command: `python3 -m venv venv`  
   Activate the virtual environment: `source venv/bin/activate`

4. Install all the packages from the `requirements.txt` file by running the command: `pip install -r requirements.txt`

5. Create two PostgreSQL databases for the project: one for the app (`marvel_db`) and one for app testing (`marvel_test`).

#### Running the Project

1. In the terminal, navigate to the project folder and run the command: `python3 -m app`
2. Open a web browser and enter the following URL: http://127.0.0.1:5000/

### Testing

For testing, it is recommended to run individual test files due to the size of the app. Running individual test files makes it easier to identify and fix bugs rather than running all the tests at once, which may take a long time due to the duration of login and API data fetching.

To run tests, execute the following command in the terminal: `python -m unittest [FILE NAME].py`

- Replace `[FILE NAME]` with the name of the specific test file you want to run.

## Deployed URL on Render

I'm sorry, but the deployed link may stop working. I recommend cloning the projects to your local computer using Git.

[Deployed link.](https://capstone-project1-render.onrender.com)
