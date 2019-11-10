import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import parser2

from PIL import Image
import pytesseract

UPLOAD_FOLDER = '/home/pi/Documents/CaloReceipt/uploadpics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_period(s):
    s=s[::-1]
    return -s.find('.') - 1

def ocr(file):
    im = Image.open(file)
    text = pytesseract.image_to_string(im, lang = 'eng', config='--psm 6')
    return text
    
def image_ocr(image_path, output_txt_file_name):
  image_text = pytesseract.image_to_string(image_path, lang='eng', config='--psm 6')
  with open(output_txt_file_name, 'w+', encoding='utf-8') as f:
    f.write(image_text)
    

    #out_stream=open(file[:find_period(file)] + ".txt", 'w')
    #out_stream.write(text)
    #out_stream.close()

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return 'error1'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return 'no file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            os.system('page_dewarp-master/page_dewarp.py uploadpics/' + filename)
            
            filename=filename[:find_period(filename)] + '_thresh.png'
            print(filename)
            
            file = open('/home/pi/Documents/CaloReceipt/' + filename)
            print('hihi')
            
            image_ocr('/home/pi/Documents/CaloReceipt/' + filename, 'to_be_parsed.txt')
            
            in_stream=open('to_be_parsed.txt')
            text=in_stream.read()
            in_stream.close()
            
            results = parser2.parser("to_be_parsed.txt")
            html = ""
            for result in results:
                html += result + ":" + str(results[result]) + "\n"
            
            return html
    
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
