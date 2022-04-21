import os, fitz, logging, sys, signal
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from src.api_handling import extract_entity_google, extract_image, clean_content

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

logging.basicConfig(stream=sys.stdout, level=os.environ.get("LOGLEVEL", "INFO"), format='%(message)s')

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf','png'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = app.config['UPLOAD_FOLDER'] + '/' + filename
            entity_data = None
            text_content = None
            if filename.rsplit('.', 1)[1].lower() == 'png':
                raw_content = None
                with open(file_path, 'rb') as f:
                    raw_content = f.read()
                text_content = clean_content(extract_image(raw_content))
            else:
                doc = fitz.open(file_path)  # open pdf document
                pages_content = []
                for page_content in doc:
                    pages_content.append(page_content.get_text())
                text_content = clean_content(" ".join(pages_content))
            entity_data = extract_entity_google(text_content)
            return render_template('index.html', content=entity_data)
        else:
            flash('Allowed PDF or PNG file only')
            return redirect(request.url)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000, debug = True)
