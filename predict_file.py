import os, sys
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import flash
from flask import send_from_directory

from keras.models import Sequential, load_model
import keras
import numpy as np
from PIL import  Image

classes = ['monkey', 'boar', 'crow']
num_classes = len(classes)
image_size = 50

UPLOAD_FOLDER = '/work/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "super secret key"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            model = load_model('./animal_cnn_aug.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            x = []
            x.append(data)
            x = np.array(x)

            result = model.predict([x])[0]
            predicted = result.argmax()
            percentage = int (result[predicted] * 100)
            return '{} ({} %)'.format(classes[predicted], percentage)
            # return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Upload new Picture and Predict</title>
    </head>
    <body>
    <h1>Upload new Picture and Predict </h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)