from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import cv2


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



# Ensure the UPLOAD_FOLDER exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def fuse_images(image1_path, image2_path):
    # Load images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)

    # Resize images to have the same dimensions
    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Perform image fusion (averaging in this case)
    fused_image = cv2.addWeighted(img1, 0.5, img2_resized, 0.5, 0)

    return fused_image

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Check if the post request has the file part
    if 'file1' not in request.files or 'file2' not in request.files:
        return redirect(request.url)

    file1 = request.files['file1']
    file2 = request.files['file2']

    # If the user does not select a file, the browser also submits an empty part without a filename
    if file1.filename == '' or file2.filename == '':
        return redirect(request.url)

    # Save the uploaded files
    file1_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
    file2_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)

    file1.save(file1_path)
    file2.save(file2_path)

    # Fuse images
    fused_image = fuse_images(file1_path, file2_path)

    # Save the fused image
    fused_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'fused_image.jpg')
    cv2.imwrite(fused_image_path, fused_image)

    return render_template('result.html', fused_image_path=fused_image_path)


@app.route('/download')
def download():
    fused_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'fused_image.jpg')
    return send_file(fused_image_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
