from flask import Flask, render_template, request, send_from_directory
# from flask_sqlalchemy import SQLAlchemy
# from io import BytesIO
import os 
import face_physio as fp

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# db = SQLAlchemy(app)

# class FileContents(db.Model) :
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(300))
#     data = db.Column(db.LargeBinary)

# rename picture
# def rename(target) :
#     i = 0 
#     os.chdir(target)
#     for file in os.listdir() :
#         i+=1
    # i = str(i)
    # for file in os.listdir() :
    #     src = file 
    #     if src == filename :
    #         dst = "images"+i+".jpg"
    #         os.rename(src, dst)
    # data = [i, dst]
    # return i

# write file result
def write_file(target, result_text, image_name) :
    i = 0
    for file in os.listdir() :
        i+=1
    i = str(i+1)
    f = open(target+"\\result"+i+".txt", "w", encoding="utf-8")
    f.write(result_text+"\n"+"images_name : "+image_name)
    f.close()

# route index
@app.route('/')
@app.route('/index')
def index() :
    return render_template('index.html')

# route upload
@app.route('/upload', methods=['POST'])
def upload() :

    target_images = os.path.join(APP_ROOT,'upload_images') # folder path
    target_file = os.path.join(APP_ROOT, 'result_text') # folder path
    if not os.path.isdir(target_images) :
        os.mkdir(target_images)    # create folder if not exits
    if not os.path.isdir(target_file) :
        os.mkdir(target_file)   # create folder if not exits
    if request.method == 'POST' :
        file = request.files['images']
        filename = file.filename
        destination = "\\".join([target_images, filename])
        file.save(destination)  # save file to folder
        result = fp.facephysio(destination) # send images to facephysio
        # n = rename(filename, target_images) # rename image
        write_file(target_file, str(result), filename)   # write file keep result

        # newfile = FileContents(name=file.filename, data=file.read())  # Save to DB
        # db.session.add(newfile)
        # db.session.commit()
    # return send_from_directory("upload_images", filename, as_attachment=True)

    return render_template('show.html', image_name=filename, data=result)

@app.route('/upload/<filename>')
def send_image(filename) :
    return send_from_directory("upload_images", filename)

# @app.route('/download')
# def download() :
#     file_images = FileContents.query.filter_by(id=1).first()
#     return send_file(BytesIO(file_images.data), attachment_filename='images.jpg', as_attachment=True)

if __name__ == '__main__' :
    app.run(host="0.0.0.0",port=80)