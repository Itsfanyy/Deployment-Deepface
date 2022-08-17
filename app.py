from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2
from deepface import DeepFace
from PIL import Image



UPLOAD_FOLDER = './static/upload/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'jpg',"jpeg"}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        file = request.files["gambar"]
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #image = cv2.imread(file)
            image = Image.open(file)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = 'static/upload'+filename
            prediction = DeepFace.analyze(image)
            print(prediction)       
            predicted_emotion = prediction["dominant_emotion"]
            return render_template("result.html", predicted_image=image_path, predicted_emotion=predicted_emotion)
    else:
        return "use post method"

if __name__ == "__main__":
    app.run(debug=True)