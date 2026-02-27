# משתמשים במערכת הפעלה קלה עם פייתון
FROM python:3.10-slim

# התקנת FFmpeg ו-Nodejs שחובה בשביל yt-dlp
RUN apt-get update && apt-get install -y ffmpeg nodejs && rm -rf /var/lib/apt/lists/*

# הגדרת תיקיית העבודה
WORKDIR /app

# העתקת קובץ הדרישות והתקנת הספריות
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# העתקת קוד השרת שלנו
COPY app.py .

# פקודת ההפעלה של השרת
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--timeout", "120", "app:app"]
