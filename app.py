from flask import Flask, render_template, request, redirect, url_for, session
from user import User

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Secret key for session management

# Example movie database by genre
movies_by_genre = {
    "action": ["Mad Max: Fury Road", "Die Hard", "John Wick", "The Dark Knight"],
    "comedy": ["The Hangover", "Superbad", "Step Brothers", "Groundhog Day"],
    "drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather", "12 Angry Men"],
    "horror": ["The Conjuring", "Get Out", "It", "A Nightmare on Elm Street"],
    "sci-fi": ["Inception", "The Matrix", "Interstellar", "Blade Runner 2049"],
    "romance": ["Pride and Prejudice", "La La Land", "The Notebook", "A Star is Born"],
}

# Dummy user data (you can replace it with a database in the future)
users = [
    User(username="admin", password="123"),
    User(username="user", password="123")
]


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    genre = request.form['genre'].lower()
    recommended_movies = movies_by_genre.get(genre, ["No movies found for this genre."])
    return render_template('index.html', genre=genre.capitalize(), movies=recommended_movies)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate login credentials
        user = User.authenticate(users, username, password)
        if user:
            session['logged_in'] = True
            session['username'] = user.username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear session data to log out the user
    return redirect(url_for('login'))  # Redirect to the login page after logging out



if __name__ == '__main__':
    app.run(debug=True)
