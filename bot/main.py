import telebot
from config import bot_token
import utils


tbot = telebot.TeleBot(token=bot_token)


@tbot.message_handler(commands=['start'])
def start_bot(message):
    user = message.from_user.username  
    tbot.send_message(message.chat.id, 
                      f"Привет {user}, я бот перевода голоса в текст")


@tbot.message_handler(content_types=['voice'])
def transfer_voice(message):
    filename = utils.download_tgfile(tbot, message.voice.file_id)
    convert_ogga = utils.oga2wav(filename)
    text = utils.get_speech(convert_ogga)
    utils.remove_file(filename)
    tbot.send_message(message.chat.id, text)


@tbot.message_handler(content_types=['sticker'])
def send_sticker(message):
    img = utils.get_img()
    tbot.send_sticker(message.chat.id, img)
    img.close()


@tbot.message_handler(content_types=['photo'])
def reply_photo(message):
    file_id = message.photo[-1].file_id
    filename = utils.download_tgfile(tbot, file_id)
    filename = utils.transform_image(filename)
    img = open(filename, 'rb')
    tbot.send_photo(message.chat.id, img)
    img.close()
    utils.remove_file(filename)


if __name__ == '__main__':
    tbot.polling()
