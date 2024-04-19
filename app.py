import os
# The proposed favorite comics feature, although mentioned in the project proposal, was not implemented as it was deemed unnecessary for the project.
from flask import Flask, redirect, render_template, session,flash, request,g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Like, Comment, MarvelCharacters, MarvelComics, ComicsCharacters, FavoriteCharacters
from forms import RegisterForm, LoginForm, EditForm, PostForm
from requests_file import save_some_characters_to_db, get_character, get_character_comics
from better_UI import return_first_15_words
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

# Run this via "python3 -m app" in the command line


def create_app(database_name, testing=False):
    app = Flask(__name__)

    # on Render, set the DATABASE_URL environment variable to the database connection string gotten from ElephantSQL.
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", f"postgresql:///{database_name}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    if testing:
        app.config["WTF_CSRF_ENABLED"] = False
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

    debug = DebugToolbarExtension(app)


    ##############################################################################
    # Authentication: signup, login, logout
    @app.before_request
    def add_user_to_g():
        """If we're logged in, add curr user to Flask global."""

        if 'user_username' in session:
            g.user = User.query.get(session['user_username'])

        else:
            g.user = None

    @app.route('/register', methods=["GET", "POST"])
    def show_register():
        """show register page"""
        default_profile_pic = "https://uxwing.com/wp-content/themes/uxwing/download/peoples-avatars/no-profile-picture-icon.png"

        if 'user_username' in session:
            flash("You are logged in.")
            username = session.get('user_username')
            return redirect(f'/users/{username}')

        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            password= form.password.data
            email= form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            bio = form.bio.data

            if form.image_url.data:
                image_url = form.image_url.data
            else:
                image_url = default_profile_pic

            hashed_password = User.register(password)
            hashed_password = hashed_password.password

            new_user = User(username= username, password=hashed_password, email=email, first_name=first_name, last_name=last_name, bio=bio, image_url=image_url)

            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError:
                form.username.errors.append('Username taken.  Please pick another')

            session['user_username'] = new_user.username
            flash("Welcome! Successfully Created Your Account!", "success")
            return redirect("/")
        else:
            return render_template('register.html', form=form)

    @app.route('/login', methods=["GET", "POST"])
    def show_login():
        """show the users the login page"""
        if 'user_username' in session:
            flash("You are logged in.")
            username = session.get('user_username')
            return redirect(f'/users/{username}')
        
        form = LoginForm()
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user = User.authenticate(username, password)
            if user:
                flash(f"Welcome Back, {user.username}!", "primary")
                session['user_username'] = user.username
                return redirect("/")
            else:
                form.username.errors = ["Invalid username/password."]
        
        return render_template('login.html', form=form)

    @app.route('/logout')
    def logout_user():
        """log out the user"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/')
        session.pop("user_username")
        return redirect('/')


    ##############################################################################
    #app user's routes
    @app.route('/')
    def redirect_to_register():
        """show homepage"""

        if 'user_username' in session:
            if not MarvelCharacters.query.first():
                # If it's empty, save some characters to the database
                save_some_characters_to_db()
            characters = MarvelCharacters.query.all()
            liked_character = FavoriteCharacters.query.filter_by(user_id = g.user.username).all()
            likes = [each_char.character_id for each_char in liked_character]

            return render_template('home.html', characters=characters, short= return_first_15_words,likes= likes)
        else:
            return redirect("/login")
        
    @app.route('/users/<username>')
    def show_users_page(username):
        """show user's page"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        
        user = User.query.filter_by(username = username).first()
        if user ==None:
            flash("Can't find the user.")
            return redirect("/")
        
        authorization= False
        if username == session.get('user_username'):
            authorization = True


        # posts = Post.query.filter_by(user_id = user.username).all()
        posts = Post.query.filter_by(user_id=user.username).order_by(desc(Post.timestamp)).all()
        return render_template("profile-posts.html", user=user, authorization= authorization, posts=posts, in_post_page =True)

    @app.route('/users/<username>/edit', methods=["GET", "POST"])
    def edit_user_info(username):
        """Let the user change their profile information"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        user = User.query.filter_by(username = username).first()
        if user ==None:
            return redirect("/")
        if username != session.get('user_username'):
            return redirect("/")
        
        form = EditForm(obj=user)
        if form.validate_on_submit():
            if User.authenticate(user.username, form.password.data):
                username = form.username.data
                email= form.email.data
                image_url = form.image_url.data
                first_name = form.first_name.data
                last_name = form.last_name.data
                bio= form.bio.data

                user.email = email
                user.username = username
                user.image_url = image_url
                user.first_name = first_name
                user.last_name = last_name
                user.bio = bio
                db.session.commit()

                #updating the session
                session['user_username'] = user.username

                return redirect(f'/users/{username}')
            else:
                flash("Your password is incorrect!", 'danger')
                return redirect('/')

        return render_template('user_edit.html', form = form)

    @app.route('/users/<username>/delete', methods=["POST"])
    def delete_user_from_db(username):
        """"delete a user from the database"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        user = User.query.filter_by(username = username).first()
        if user ==None:
            flash("Access unauthorized.")
            return redirect("/")
        if username != session.get('user_username'):
            flash("Access unauthorized.")
            return redirect("/")
        db.session.delete(user)
        db.session.commit()
        return redirect('/logout')

    ##############################################################################
    #posts routes

    @app.route('/users/<username>/post', methods=["GET", "POST"])
    def user_post(username):
        """show the user post form"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        user = User.query.filter_by(username = username).first()
        if user ==None:
            flash("Access unauthorized.")
            return redirect("/")
        if username != session.get('user_username'):
            flash("Access unauthorized.")
            return redirect("/")
        
        form = PostForm()
        if form.validate_on_submit():
            text = form.text.data
            new_post = Post(text = text, user_id = user.username)
            db.session.add(new_post)
            db.session.commit()
            return redirect(f'/users/{username}')
        else:
            return render_template('user_post.html', form = form)

    @app.route('/posts')
    def show_all_posts():
        """show all the posts"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        
        posts = Post.query.order_by(desc(Post.timestamp)).all()
        likes_count = {post.id: len(post.likes) for post in posts}


        user_liked_post = Like.query.filter_by(user_id = g.user.username).all()
        user_liked_post_list = [each_post.post_id for each_post in user_liked_post]

        return render_template('posts.html', posts=posts, likes = user_liked_post_list, likes_count=likes_count)

    @app.route('/posts/<int:post_id>/details')
    def show_post_detail(post_id):
        """show post details
        allow users to like and comment posts"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        
        liked =False
        liked_post = Like.query.filter_by(user_id = g.user.username, post_id = post_id).first()
        if liked_post != None:
            liked=True

        post = Post.query.filter_by(id = post_id).first()
        return render_template('post_details.html', post=post, liked=liked, likes_count = len(post.likes))
    ##############################################################################
    #app Marvel pages
    @app.route('/characters/<int:character_id>')
    def show_character_page(character_id):
        """Show character's profile page"""

        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        
        liked= False
        liked_character = FavoriteCharacters.query.filter_by(user_id = g.user.username, character_id = character_id).first()
        if liked_character != None:
            liked= True

        character = MarvelCharacters.query.get_or_404(character_id)
        comics = character.comics

        return render_template('character_profile.html', character=character, liked= liked, comics=comics)

    @app.route('/get-character', methods=["POST"])
    def get_Marvel_character():
        """fetch Marvel Character from Marvel API"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')

        request_name = request.form.get("characterName")

        if get_character(request_name) == False:
            flash("We can't find your Marvel character.")
            return redirect("/")
        else:
            id, name, thumbnail, description= get_character(request_name)
            if MarvelCharacters.query.get(id) == None:
                if thumbnail and description:
                    new_ch = MarvelCharacters(id=id, name=name, thumbnail=thumbnail, description=description)
                elif description == "":
                    new_ch = MarvelCharacters(id=id, name=name, thumbnail=thumbnail)
                elif len(thumbnail) > 3:
                    # an Marvel character picture url is longer than 3 characters
                    new_ch = MarvelCharacters(id=id, name=name, description=description)
                else:
                    new_ch = MarvelCharacters(id=id, name=name)
                db.session.add(new_ch)
                db.session.commit()

                if get_character_comics(id) != False:
                    random_comics = get_character_comics(id)
                    for comics_id, comics_title in random_comics.items():
                        comics_in_db = MarvelComics.query.filter_by(id=comics_id).first()
                        if comics_in_db ==None:
                            new_comics = MarvelComics(id = comics_id, title = comics_title)
                            db.session.add(new_comics)
                            db.session.commit()

                        new_comics_character = ComicsCharacters(character_id =id, comics_id = comics_id)
                        db.session.add(new_comics_character)
                        db.session.commit()
            return redirect(f"/characters/{id}")
        
    @app.route('/users/<username>/favorite/characters')
    def show_favorite_characters(username):
        """show user's favorite characters page"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        
        
        liked_character = FavoriteCharacters.query.filter_by(user_id = username).all()
        likes = [each_char.character_id for each_char in liked_character]

        authorization= False
        if username == session.get('user_username'):
            authorization = True

        return render_template('profile-fav.html', liked_characters=liked_character, short= return_first_15_words, likes= likes, user=g.user, authorization=authorization, in_fav_page=True)

    ##############################################################################
    # RESTFUl API routes
    @app.route('/api/characters')
    def api_list_characters():
        """api- list all Marvel characters"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        all_characters = [character.serialize() for character in MarvelCharacters.query.all()]
        return jsonify(characters=all_characters)

    @app.route('/api/characters/<int:id>')
    def api_each_character(id):
        """api- list each Marvel character"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        character = MarvelCharacters.query.get_or_404(id)
        return jsonify(character= character.serialize())

    @app.route('/api/users')
    def api_list_users():
        """api- list all users"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        all_users = [user.serialize() for user in User.query.all()]
        return jsonify(users=all_users)

    @app.route('/api/users/<username>')
    def api_show_a_user(username):
        """api- show a user"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        user = User.query.filter_by(username=username).first()
        return jsonify(user= user.serialize())

    @app.route('/api/users/<username>', methods=["PATCH"])
    def api_updating_a_user(username):
        """api-updating a user"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        if User.authenticate(username, request.json.get('password')):
            user = User.query.filter_by(username=username).first()
            user.username = request.json.get('username', user.username)
            user.email = request.json.get('email', user.email)
            user.image_url = request.json.get('image_url', user.image_url)
            user.first_name = request.json.get('first_name', user.first_name)
            user.last_name = request.json.get('last_name', user.last_name)
            user.bio = request.json.get('bio', user.bio)
            db.session.commit()
            return jsonify(user= user.serialize())
        return jsonify(message= "Wrong Password")

    @app.route('/api/favorite-characters/<int:id>', methods=["DELETE"])
    def api_delete_user_char(id):
        """api- delete user's fav character"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        user_fav_char = FavoriteCharacters.query.filter_by(user_id=g.user.username, character_id = id).first()
        if user_fav_char != None:
            db.session.delete(user_fav_char)
            db.session.commit()
        return jsonify(message= "Deleted!")

    @app.route('/api/favorite-characters/<int:id>', methods=["POST"])
    def api_add_user_char(id):
        """api- add user's fav character"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        user_fav_char = FavoriteCharacters.query.filter_by(user_id=g.user.username, character_id = id).first()
        if user_fav_char == None:
            new_fav_char = FavoriteCharacters(user_id=g.user.username, character_id = id)
            db.session.add(new_fav_char)
            db.session.commit()
            return (jsonify(added= new_fav_char.serialize()),201)
        return (jsonify(added= user_fav_char.serialize()),201)

    @app.route('/api/posts/<int:id>', methods=["DELETE"])
    def api_delete_posts(id):
        """api- delete logged in user's post"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        user_post = Post.query.filter_by(id = id).first()
        if user_post !=None:
            db.session.delete(user_post)
            db.session.commit()
        return jsonify(message= "Deleted!")

    @app.route('/api/posts/<int:id>/like', methods=["POST"])
    def api_like_a_post(id):
        """api- logged in user like a post"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        liked_post = Like.query.filter_by(user_id = g.user.username,post_id = id).first()
        if liked_post == None:
            new_like = Like(user_id = g.user.username, post_id = id)
            db.session.add(new_like)
            db.session.commit()
            return (jsonify(like= new_like.serialize()),201)
        return (jsonify(added= liked_post.serialize()),201)

    @app.route('/api/posts/<int:id>/like', methods=["DELETE"])
    def api_unlike_a_post(id):
        """api- logged in user unlike a post"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        liked_post = Like.query.filter_by(user_id=g.user.username, post_id = id).first()
        if liked_post != None:
            db.session.delete(liked_post)
            db.session.commit()
        return jsonify(message="Deleted!")
    @app.route('/api/posts/<int:id>/comments')
    def api_show_post_comments(id):
        """api- show post comments"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        post = Post.query.filter_by(id = id).first()
        if post != None:
            post_comments = post.comments
            all_comments = [comment.serialize() for comment in post_comments]
            return jsonify(comments= all_comments)
        return jsonify(message= "No post found")
    @app.route('/api/posts/<int:id>/comments', methods= ["POST"])
    def api_add_a_comment(id):
        """api-add a comment to a post"""
        if 'user_username' not in session:
            flash("Access unauthorized.")
            return redirect('/login')
        post = Post.query.filter_by(id = id).first()
        if post != None:
            new_comment= Comment(text = request.json.get("text"), user_id = g.user.username, post_id = id)
            db.session.add(new_comment)
            db.session.commit()
            return (jsonify(comment= new_comment.serialize()),201)
        return (jsonify(message= "No post found"),201)

    return app

if __name__ == '__main__':
    app = create_app('marvel_db')
    connect_db(app)
    app.run(debug=True)