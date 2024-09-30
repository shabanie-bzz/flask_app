from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database setup function
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  original_url TEXT NOT NULL,
                  short_url TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Helper function to generate short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))

# Home page: URL shortening form
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']

        if not original_url.startswith(('http://', 'https://')):
            flash('Invalid URL. Please include http:// or https://', 'danger')
            return redirect(url_for('index'))

        short_url = generate_short_url()

        # Save the original and short URL in the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
        conn.commit()
        conn.close()

        flash(f'Success! Your short URL is: {request.url_root}{short_url}', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')

# Redirect from short URL to original URL
@app.route('/<short_url>')
def redirect_to_original(short_url):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        flash('Invalid short URL', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
