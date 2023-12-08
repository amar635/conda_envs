
from datetime import datetime, timedelta
from io import BytesIO
from flask import Flask, make_response, render_template, request, redirect, send_from_directory, url_for, current_app as app
import os
from flask_smorest import Blueprint, abort
from gtts import gTTS
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from pathlib import Path

# import pyttsx3

blp = Blueprint("page", "pages", description="html pages for api")

# engine = gTTS.init()

@blp.route("/")
def index():
    return render_template('pdf_to_audio.html')

@blp.route("/",methods=['POST'] )
def upload_file():
    if request.method == 'POST':
        audio_filename = "audio.mp3"
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
            #         validate_pdf(uploaded_file):
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
        else:
            abort(400)
        path_to_save = str(os.path.join(app.config['UPLOAD_FOLDER'],audio_filename))
        # for file in path_to_save:
        #     if file == audio_filename: 
        #         os.remove(file)
        current_directory = os.getcwd()
        # home = str(Path.home())
        pdf_file = request.files['file']
        bytes_file = BytesIO(pdf_file.read())
        pdf_string = ""
        reader = PdfReader(bytes_file)
        number_of_pages = len(reader.pages)
        for number in range(number_of_pages):
            page = reader.pages[number]
            pdf_string += page.extract_text()
        tts = gTTS(pdf_string, lang='en', tld='co.in')
        tts.save('audio.mp3')
        main_file =  open("audio.mp3", "rb").read()
        dest_file = open(path_to_save, 'wb+')
        dest_file.write(main_file)
        dest_file.close()
        return redirect(url_for('.download_file', name=audio_filename))
    # tts.save('audio.mp3')
    # response = make_response(send_from_directory(current_directory,'audio.mp3', as_attachment=True)) 
    # return response

@blp.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
#     tts = gTTS(uploaded_file, lang='en', tld='co.in')
# engine = pyttsx3.init()

# def validate_pdf(pdf_file):
#     isValid=True
#     try:
#         reader = PdfReader(pdf_file)
#         number_of_pages = len(reader.pages)
#         for page in reader.pages:
#             text += page.extract_text()
#     except Exception as exc:
#         # text = fallback_text_extraction("example.pdf")
#         isValid = False
#     return isValid
    

# @blp.route('/')
# def index():
#     return render_template('index.html')

# @blp.route('/', methods=['POST'])
# def upload_file():
#     pass
    # uploaded_file = request.files['file']
    # filename = secure_filename(uploaded_file.filename)
    # audio_filename = "audio.mp3"
    # if filename != '':
    #     file_ext = os.path.splitext(filename)[1]
    #     # if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
    #     #         validate_pdf(uploaded_file):
    #     if file_ext not in app.config['UPLOAD_EXTENSIONS']:
    #         abort(400)
    #     # path_to_save = os.path.join(app.config['UPLOAD_PATH'], filename)
    #     # path_to_save = app.config['UPLOAD_PATH']
    #     current_directory = os.getcwd()
    #     # path_to_save = os.path.join(current_directory,"static/uploads")
    #     # Remove any previously uploaded files
    #     for file in current_directory:
    #             if file == "audio.mp3": 
    #                 os.remove(file)
    #     # Gets string from uploaded PDF
    #     pdf_file = request.files['file']
    #     bytes_file = BytesIO(pdf_file.read())
    #     pdf_string = ""
    #     reader = PdfReader(bytes_file)
    #     number_of_pages = len(reader.pages)
    #     for number in range(number_of_pages):
    #         page = reader.pages[number]
    #         pdf_string += page.extract_text()
        
    #     #convert pdf to audio
    #     engine.say("This is a text message")
    #     engine.save_to_file(pdf_string,os.path.join(current_directory,"audio.mp3"))
    #     # engine.save_to_file(pdf_string, os.path.join(app.config['UPLOAD_PATH'], "converted_to_audio.mp3"))
    #     engine.runAndWait()

    #     #construct response

    #     # response = send_from_directory(os.path.join(current_directory,"uploads"), audio_filename, as_attachment=True)
    #     response = make_response(send_from_directory(current_directory,"audio.mp3", as_attachment=True))   
    #     # now = datetime.now()
    #     # after_20_seconds = now + timedelta(seconds=20)
    #     # response.set_cookie(key="downloadStarted", value="1", expires=after_20_seconds)

    #     return response
    # else:
    #     return render_template('index.html')
# @blp.route('/')
# def index():
#     files = os.listdir(current_app.config['UPLOAD_PATH'])
#     return render_template('index.html', files=files)

# @blp.route('/', methods=['POST'])
# def upload_files():
#     uploaded_file = request.files['file']
#     filename = secure_filename(uploaded_file.filename)
#     if filename != '':
#         file_ext = os.path.splitext(filename)[1]
#         if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
#             # or \
#             #     file_ext != validate_image(uploaded_file.stream):
#             return "Invalid image", 400
#         uploaded_file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
#     return '', 204