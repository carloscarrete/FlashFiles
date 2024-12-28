from flask import Flask, request, send_file, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# HTML template con barra de progreso
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
        /* Estilos para la barra de progreso */
        .progress-container {
            display: none;
            margin-top: 20px;
        }
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #333;
            border-radius: 10px;
            overflow: hidden;
        }
        .progress {
            width: 0%;
            height: 100%;
            background-color: #00ff00;
            transition: width 0.3s ease;
        }
        .progress-text {
            text-align: center;
            margin-top: 5px;
            color: #00ff00;
        }
        .upload-status {
            text-align: center;
            margin-top: 10px;
            font-weight: bold;
        }
        /* Estilos para drag and drop */
        .drop-zone {
            width: 100%;
            height: 150px;
            border: 2px dashed #00ff00;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 20px;
            transition: border-color 0.3s ease;
        }
        .drop-zone.dragover {
            border-color: #00cc00;
            background-color: rgba(0, 255, 0, 0.1);
        }
        .drop-zone-text {
            text-align: center;
            color: #00ff00;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Transferencia de Archivos</h1>
        
        <div class="upload-form">
            <h2>Subir Archivo</h2>
            <!-- Zona de drag and drop -->
            <div class="drop-zone" id="dropZone">
                <div class="drop-zone-text">
                    Arrastra y suelta archivos aquí<br>
                    o<br>
                    haz clic para seleccionar
                </div>
            </div>

            <form id="uploadForm" enctype="multipart/form-data">
                <input type="file" name="file" required id="fileInput" style="display: none;">
                <input type="submit" value="Subir">
            </form>
            
            <!-- Contenedor de la barra de progreso -->
            <div class="progress-container" id="progressContainer">
                <div class="progress-bar">
                    <div class="progress" id="progressBar"></div>
                </div>
                <div class="progress-text" id="progressText">0%</div>
                <div class="upload-status" id="uploadStatus"></div>
            </div>
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

    <script>
        const dropZone = document.getElementById('dropZone');
        const fileInput = document.getElementById('fileInput');
        const uploadForm = document.getElementById('uploadForm');
        const progressContainer = document.getElementById('progressContainer');
        const progressBar = document.getElementById('progressBar');
        const progressText = document.getElementById('progressText');
        const uploadStatus = document.getElementById('uploadStatus');

        // Función para manejar la subida de archivos
        function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            progressContainer.style.display = 'block';
            uploadStatus.textContent = 'Iniciando carga...';
            
            const xhr = new XMLHttpRequest();
            
            xhr.upload.onprogress = function(e) {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    progressBar.style.width = percentComplete + '%';
                    progressText.textContent = percentComplete.toFixed(1) + '%';
                    
                    if (percentComplete < 100) {
                        uploadStatus.textContent = 'Subiendo archivo...';
                    } else {
                        uploadStatus.textContent = 'Procesando...';
                    }
                }
            };
            
            xhr.onload = function() {
                if (xhr.status === 200) {
                    uploadStatus.textContent = '¡Archivo subido exitosamente!';
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    uploadStatus.textContent = 'Error al subir el archivo';
                }
            };
            
            xhr.onerror = function() {
                uploadStatus.textContent = 'Error de conexión';
            };
            
            xhr.open('POST', '/upload', true);
            xhr.send(formData);
        }

        // Event listeners para drag and drop
        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                uploadFile(e.dataTransfer.files[0]);
            }
        });

        // Click en la zona de drop para abrir el selector de archivos
        dropZone.addEventListener('click', () => {
            fileInput.click();
        });

        // Cuando se selecciona un archivo mediante el input
        fileInput.addEventListener('change', () => {
            if (fileInput.files.length) {
                uploadFile(fileInput.files[0]);
            }
        });

        // Prevenir el envío del formulario por defecto
        uploadForm.onsubmit = function(e) {
            e.preventDefault();
            if (fileInput.files.length) {
                uploadFile(fileInput.files[0]);
            }
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template_string(HTML_TEMPLATE, files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    try:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return 'File uploaded successfully'
    except Exception as e:
        return str(e), 500

@app.route('/download/<filename>')
def download(filename):
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)
    except Exception as e:
        return str(e), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)