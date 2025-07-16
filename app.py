from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'format': 'bestvideo+bestaudio/best'
        }
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return f"Error al descargar: {e}"

if __name__ == '__main__':
    # ✅ Cambios para Render
    port = int(os.environ.get('PORT', 5000))  # Render asigna dinámicamente el puerto
    app.run(host='0.0.0.0', port=port, debug=True)
