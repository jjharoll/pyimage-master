import os
import pytesseract
from flask import Flask, flash, request, render_template, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png', 'bmp','tif','tiff'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'topsecret'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file')
        file = request.files['file']

        if file.filename == '':
            flash('no selected file')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            flash(pytesseract.image_to_string(path))
            return render_template('index.html', path=url_for('get_image', filename=filename))

    return render_template('index.html')

@app.route('/files/<path:filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)