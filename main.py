from flask import Flask, request, send_file, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML template con fondo negro
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Transferencia de Archivos</title>
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
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .file-list {
            background-color: #222;
            padding: 20px;
            border-radius: 8px;
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
        a {
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
            border-radius: 4px;
            cursor: pointer;
        }
        input[type="submit"]:hover {
            background-color: #00cc00;
        }
        .status {
            margin-top: 10px;
            padding: 10px;
            border-radius: 4px;
        }
        .success {
            background-color: #004400;
        }
        .error {
            background-color: #440000;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Transferencia de Archivos</h1>
        
        <div class="upload-form">
            <h2>Subir Archivo</h2>
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
            <h2>Archivos Disponibles</h2>
            {% if files %}
                {% for file in files %}
                <div class="file-item">
                    <span>{{ file }}</span>
                    <a href="{{ url_for('download', filename=file) }}">Descargar</a>
                </div>
                {% endfor %}
            {% else %}
                <p>No hay archivos disponibles.</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_TEMPLATE, files=files, message=request.args.get('message'), 
                                error=request.args.get('error'))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return index()
    
    file = request.files['file']
    if file.filename == '':
        return index()
    
    try:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return index()
    except Exception as e:
        return index()

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)
    except Exception as e:
        return index()

if __name__ == '__main__':
    # Ejecutar el servidor en el puerto 5000 y hacer accesible desde cualquier dispositivo en la red
    app.run(host='0.0.0.0', port=5000, debug=True)