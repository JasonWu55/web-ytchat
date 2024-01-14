from flask import Flask, render_template, jsonify
import pytchat
from flask_apscheduler import APScheduler
import time
from googletrans import Translator
import translators as ts

translator = Translator()

app = Flask(__name__)
scheduler = APScheduler()

# Limit for the number of chat messages
MAX_CHAT_MESSAGES = 50

# Keep track of chat messages
chat_messages = []
video_id = None
status = True

def get_chat_messages():
    global chat_messages
    global video_id
    global status

    chat = pytchat.create(video_id=video_id, interruptable=False)
    try:
        for message in chat.get().sync_items():
            if (message.author.channelId == "UC4bGS1gjJ_A78tJvr6I0PRQ"):
                    continue
            lang = translator.detect(message.message)
            if (lang.lang != 'th'):
                if (lang.lang == 'zh-TW'):
                    l='zh-Hant'
                elif (lang.lang == 'zh-CN'):
                    l='zh-Hans'
                else:
                    l=lang.lang
                trans = ts.translate_text(message.message, translator='bing', 
                                        from_language=l, to_language='th')
                c = trans
            else:
                c = message.message
            timestamped_message = {
                'datetime': message.datetime,
                'author': message.author.name,
                'message': c,
                'avator': message.author.imageUrl
            }
            chat_messages.append(timestamped_message)

            # Limit the chat messages array to the last 50 messages
            if len(chat_messages) > MAX_CHAT_MESSAGES:
                chat_messages = chat_messages[-MAX_CHAT_MESSAGES:]
    except:
        pass

        #time.sleep(1)  # Add a slight delay to avoid excessive updates

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_video_id/<string:input_video_id>')
def set_video_id(input_video_id):
    global video_id
    global chat_messages

    video_id = input_video_id
    chat_messages = []  # Clear existing messages

    # Clear the chat messages array to start fresh
    chat_messages.clear()

    return f"Video ID set to: {video_id}"

@app.route('/get_chat_messages')
def get_chat_messages_route():
    global status
    if (status!=True):
        exit(1)
    return jsonify(chat_messages)

@app.route('/stop')
def stop():
    global status
    status = False

if __name__ == '__main__':
    video_id = input("Enter the video ID: ")
    scheduler.add_job(id='get_chat_messages', func=get_chat_messages, trigger='interval'
                      , seconds=5)
    scheduler.start()
    app.run(host='0.0.0.0', port=5000)
