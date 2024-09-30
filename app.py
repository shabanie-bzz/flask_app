from flask import Flask, render_template, request

app = Flask(__name__)

# Example movie database by genre (you can modify this with your own choices)
movies_by_genre = {
    "action": ["Mad Max: Fury Road", "Die Hard", "John Wick", "The Dark Knight"],
    "comedy": ["The Hangover", "Superbad", "Step Brothers", "Groundhog Day"],
    "drama": ["The Shawshank Redemption", "Forrest Gump", "The Godfather", "12 Angry Men"],
    "horror": ["The Conjuring", "Get Out", "It", "A Nightmare on Elm Street"],
    "sci-fi": ["Inception", "The Matrix", "Interstellar", "Blade Runner 2049"],
    "romance": ["Pride and Prejudice", "La La Land", "The Notebook", "A Star is Born"],
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    genre = request.form['genre'].lower()  # Get genre input from user, make it lowercase
    recommended_movies = movies_by_genre.get(genre, ["No movies found for this genre."])
    return render_template('index.html', genre=genre.capitalize(), movies=recommended_movies)

if __name__ == '__main__':
    app.run(debug=True)
