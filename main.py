
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import yt_dlp
import os

TOKEN = "7653810312:AAFYhXT7mg614Mk35GQo_Z3m-i0tze_ZOBQ"

# إعداد اللوجات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# دالة لتحميل الصوت من يوتيوب
def download_audio(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            return 'song.mp3', info.get('title')
        except Exception as e:
            print(e)
            return None, None

# الدالة التي تتعامل مع الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    file_path, title = download_audio(query)

    if file_path:
        with open(file_path, 'rb') as audio:
            await update.message.reply_audio(audio=audio, title=title)
        os.remove(file_path)
    else:
        await update.message.reply_text("ما گدرت ألكي الأغنية، جرّب اسم ثاني.")

# الدالة الرئيسية لتشغيل البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل اسم أغنية وأنا أرجعلكيها بصيغة MP3 بدون أي حقوق.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("البوت يعمل...")
    app.run_polling()
