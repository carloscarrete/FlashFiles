from flask import Flask, request, send_file, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set up the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML TEMPLATE
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    title>File Upload</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #000;
            color: #fff;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        .upload-form {
            background-color: #222;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }
        .file-list{
            background-color: #222;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            margin-bottom: 20px;
        }
        h1, h2 {
            color: #fff;
        }
        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #444;
        }
        .file-item:last-child {
            border-bottom: none;
        }
         a{
            color: #00ff00;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
         input[type="file"] {
            margin: 10px 0;
        }
        input[type="submit"] {
            background-color: #00ff00;
            color: #000;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
         input[type="submit"]:hover {
            background-color: #00cc00;
        }
        .status {
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }
        .success {
            background-color: #00ff00;
            color: #000;
        }
        .error {
            background-color: #ff0000;
            color: #fff;
        }
    }
    </style>
</head>
<body>
    <div class="container">
        <h1>File Transfer</h1>   

        <div class="upload-form">
            <h2>Upload File</h2>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <br>
                <input type="submit" value="Subir">
            </form>
             {% if message %}
            <div class="status {% if error %}error{% else %}success{% endif %}">
                {{ message }}
            </div>
            {% endif %}
        </div>

        <div class="file-list">
            <h2>File List</h2>
            {% if files %}
                {% for file in files %}
                <div class="file-item">
                    <span>{{ file }}</span>
                    <a href="{{ url_for('download', filename=file) }}">Descargar</a>
                </div> 
                {% endfor %}
            {% else %}
                <p>No files uploaded yet.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

# Route to handle file upload
@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_TEMPLATE, files=files, message=request.args.get('message'), 
                                error=request.args.get('error'))

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)
    except Exception as e:
        return index()

if __name__ == '__main__':
    # Ejecutar el servidor en el puerto 5000 y hacer accesible desde cualquier dispositivo en la red
    app.run(host='0.0.0.0', port=5000, debug=True)