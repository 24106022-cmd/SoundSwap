import os
import tempfile
import glob

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp


app = Flask(__name__)
CORS(app)


ALLOWED_FORMATS = {
    "mp3",
    "wav",
    "flac",
    "aac",
    "ogg",
    "m4a",
    "aiff",
    "alac"
}


@app.route("/")
def home():
    return "SoundSwap API is running!"


@app.route("/api/test", methods=["GET"])
def test_api():
    return jsonify({
        "success": True,
        "message": "API is working!"
    })


@app.route("/api/convert-youtube", methods=["POST"])
def convert_youtube():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "error": "No data received"
        }), 400

    url = data.get("url", "").strip()
    audio_format = data.get("format", "mp3").lower()

    if not url:
        return jsonify({
            "success": False,
            "error": "YouTube URL is required"
        }), 400

    if audio_format not in ALLOWED_FORMATS:
        return jsonify({
            "success": False,
            "error": "Unsupported audio format"
        }), 400

    temporary_directory = tempfile.mkdtemp(
        prefix="soundswap_"
    )

    output_template = os.path.join(
        temporary_directory,
        "%(id)s.%(ext)s"
    )

    ydl_options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": "192"
            }
        ]
    }

    try:

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download([url])

        converted_files = glob.glob(
            os.path.join(
                temporary_directory,
                f"*.{audio_format}"
            )
        )

        if not converted_files:
            return jsonify({
                "success": False,
                "error": "Conversion failed"
            }), 500

        output_file = converted_files[0]

        return send_file(
            output_file,
            as_attachment=True,
            download_name=f"audio.{audio_format}"
        )

    except Exception as error:

        print("Conversion error:", error)

        return jsonify({
            "success": False,
            "error": "Unable to convert this URL"
        }), 500


if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )