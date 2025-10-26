from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import os

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'html'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_usernames(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    title = soup.title.string.lower() if soup.title else ''
    usernames = []

    # Followers: usernames in <a target="_blank">
    if 'followers' in title:
        for a in soup.find_all('a', target='_blank'):
            text = a.get_text(strip=True)
            if text and text.lower() not in ['instagram user', 'deleted account', '']:
                usernames.append(text)

    # Following: usernames in <h2>
    elif 'following' in title:
        for h2 in soup.find_all('h2'):
            text = h2.get_text(strip=True)
            if text and text.lower() not in ['instagram user', 'deleted account', '']:
                usernames.append(text)

    # Clean and deduplicate
    usernames = [u for u in set(usernames) if len(u) > 2 and u.isprintable()]
    return sorted(usernames)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        if 'followers' not in request.files or 'following' not in request.files:
            return redirect(request.url)

        followers_file = request.files['followers']
        following_file = request.files['following']

        if followers_file.filename == '' or following_file.filename == '':
            return redirect(request.url)

        if allowed_file(followers_file.filename) and allowed_file(following_file.filename):
            followers_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(followers_file.filename))
            following_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(following_file.filename))

            followers_file.save(followers_path)
            following_file.save(following_path)

            followers = extract_usernames(followers_path)
            following = extract_usernames(following_path)

            set_followers = set(followers)
            set_following = set(following)

            fans = sorted(set_followers - set_following)
            snakes = sorted(set_following - set_followers)

            return render_template('result.html', fans=fans, snakes=snakes)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
