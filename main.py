from flask import Flask, render_template, request, send_from_directory
import os
from app import find_matching_images

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        keyword = request.form['keyword']
        matched_word, ratio, animal_list = find_matching_images(keyword)
        return render_template('index.html', keyword=keyword, matched_word=matched_word, ratio=ratio, animal_list=animal_list)
    else:
        return render_template('index.html')

@app.route('/static/images/<path:filename>')
def serve_images(filename):
    root_dir = os.getcwd()
    print(root_dir)
    return send_from_directory(os.path.join(root_dir, 'album').replace('\\', '/'), filename)

if __name__ == "__main__":
    app.run(debug=True)
