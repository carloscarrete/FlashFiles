from flask import Flask, request, send_file, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set up the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML TEMPLATE
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>File Upload</title>
</head>
<body>
    <h1>Upload a File</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
</body>
</html>
"""

# Route to handle file upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return render_template_string(html_template)
    return render_template_string(html_template)


if __name__ == '__main__':
    # Ejecutar el servidor en el puerto 5000 y hacer accesible desde cualquier dispositivo en la red
    app.run(host='0.0.0.0', port=5000, debug=True)