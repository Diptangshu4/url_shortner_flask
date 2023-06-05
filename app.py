from flask import Flask, render_template, request, redirect
import sqlite3
import string
import random

app = Flask(__name__)

# Database initialization
conn = sqlite3.connect('urls.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, long_url TEXT, short_url TEXT)''')

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# URL shortening route
@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['long_url']
    short_url = generate_short_url()
    cursor.execute('''INSERT INTO urls (long_url, short_url) VALUES (?, ?)''', (long_url, short_url))
    conn.commit()
    return render_template('shorten.html', short_url=short_url)

# URL redirection route
@app.route('/<short_url>')
def redirect_to_url(short_url):
    cursor.execute('''SELECT long_url FROM urls WHERE short_url = ?''', (short_url,))
    long_url = cursor.fetchone()
    if long_url:
        return redirect(long_url[0])
    else:
        return "URL not found!"

# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(characters, k=6))
    cursor.execute('''SELECT id FROM urls WHERE short_url = ?''', (short_url,))
    result = cursor.fetchone()
    if result:
        return generate_short_url()
    else:
        return short_url

if __name__ == '__main__':
    app.run(debug=True)