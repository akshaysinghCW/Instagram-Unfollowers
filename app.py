from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup
import os

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = {'html'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_usernames(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    username_elements = soup.find_all('a', {'target': '_blank'})
    usernames = [elem.text for elem in username_elements]

    return usernames

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

        if followers_file and allowed_file(followers_file.filename) and following_file and allowed_file(following_file.filename):
            followers_filename = secure_filename(followers_file.filename)
            following_filename = secure_filename(following_file.filename)

            followers_path = os.path.join(app.config['UPLOAD_FOLDER'], followers_filename)
            following_path = os.path.join(app.config['UPLOAD_FOLDER'], following_filename)

            followers_file.save(followers_path)
            following_file.save(following_path)

            # Process the uploaded files and generate the results (e.g., lists of fans and snakes)
            followers = extract_usernames(followers_path)
            following = extract_usernames(following_path)

            set_followers = set(followers)
            set_following = set(following)

            fans = [x for x in set_followers if x not in set_following]
            snakes = [x for x in set_following if x not in set_followers]

            print("List C (elements who are followers but not following):", fans)
            print("List D (elements who are following but not followers):", snakes)

            # Redirect to a results page or display the results
            return render_template('result.html', fans=fans, snakes=snakes)


    return render_template('result.html', fans=fans, snakes=snakes)


if __name__ == '__main__':
    app.run()
