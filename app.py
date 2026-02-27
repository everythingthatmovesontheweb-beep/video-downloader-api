from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import yt_dlp
import os
import glob
import uuid

app = Flask(__name__)
# מאפשר לאתר שלך לתקשר עם השרת
CORS(app) 

@app.route('/api/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "לא התקבל קישור"}), 400

    # מחיקת קבצים ישנים ושאריות שבורות
    for f in glob.glob("*.mp4") + glob.glob("*.m4a") + glob.glob("*.webm") + glob.glob("*.part"):
        try:
            os.remove(f)
        except:
            pass

    # יצירת שם קובץ ייחודי
    unique_id = str(uuid.uuid4())[:8]
    output_template = f"video_{unique_id}.%(ext)s"
    
    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best',
        'outtmpl': output_template,
        'merge_output_format': 'mp4',
        'noplaylist': True,
        # === הפתרון ליוטיוב: מתחזים לאפליקציית אנדרואיד! ===
        'extractor_args': {'youtube': ['player_client=android']},
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            mp4_filename = base + ".mp4"
            
            if not os.path.exists(mp4_filename):
                mp4_filename = filename
                
        # שליחת הקובץ המוכן
        return send_file(mp4_filename, as_attachment=True)
        
    except Exception as e:
        print(f"Error: {str(e)}") # מדפיס את השגיאה ללוגים של Render
        return jsonify({"error": str(e)}), 500

# הפעלת השרת
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
