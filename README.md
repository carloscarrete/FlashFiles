
# FlashFiles

FlashFiles is a simple and fast local file transfer application built with Flask. It allows users to easily upload, download, and share files within a local network. Whether you're sharing documents, videos, or photos, FlashFiles makes the process smooth and efficient.

## Features

- **Simple and Clean Interface**: Upload and download files with ease through a web-based interface.
- **Local Network Transfer**: Fast file transfers over your local network (no USB needed).
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **No Installation Required**: Just run the server and access it from any browser on your network.
  
## Installation

### Requirements:
- Python 3.x
- Flask
- Werkzeug

### Steps:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/FlashFiles.git
   cd FlashFiles
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask server:
   ```bash
   python main.py
   ```

4. Open your browser and go to `http://<your-ip>:5000` to access the app.

## How It Works

FlashFiles works by allowing users to upload files to a local server and download them from any device connected to the same network. Once the server is running, simply visit the page on your browser to begin the transfer process.

1. **Upload Files**: Choose a file from your device and upload it to the server.
2. **Download Files**: View a list of available files and download them directly from the server.

## Example Usage

Once the server is up and running, open your browser and go to:
```
http://<your-ip>:5000
```

From there, you can:
- Upload files to the server.
- View a list of available files to download.
- Access your files from any device in your network.

## Future Improvements

- Add file compression to optimize transfer speeds.
- Allow multiple file uploads at once.
- Add support for user authentication to secure file access.
- Integrate real-time notifications for file uploads.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
