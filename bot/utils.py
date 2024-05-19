import os
import random
from pydub import AudioSegment
import speech_recognition
from urllib import request
from PIL import Image, ImageEnhance, ImageFilter



def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)


def oga2wav(filename):
    new_filename = filename.replace('.oga', '.wav')
    audio = AudioSegment.from_file(filename)
    audio.export(new_filename, format='wav')
    return new_filename


def get_speech(filename):
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.WavFile(filename) as fsource:
        wav_audio = recognizer.record(fsource)
    text = recognizer.recognize_google(wav_audio, language='ru')
    remove_file(filename)
    return text


def download_tgfile(bot, file_id):
    file_info = bot.get_file(file_id)
    f_path = file_info.file_path
    if not os.path.exists(f_path):
        downloaded_file = bot.download_file(f_path)
    filename = f'{file_id}{f_path}'.replace('/', '_')
    with open(filename, 'wb') as file:
        file.write(downloaded_file)
    return filename


def get_img():
    filename = 'new_pic.webp'
    if not os.path.exists(filename):
        url = "https://i.pinimg.com/736x/de/7a/42/de7a4282d198c3c28825ff073f43a745.jpg"
        request.urlretrieve(url, filename)
        filename = filename.replace('.jpg', '.webp')
    sticker = open(filename, 'rb')
    return sticker


def transform_image(filename):
    source = Image.open(filename)
    rnd_filter = [ImageFilter.SHARPEN,
                  ImageFilter.FIND_EDGES,
                  ImageFilter.BLUR,
                  ImageFilter.CONTOUR,
                  ImageFilter.DETAIL,
                  ImageFilter.EMBOSS]
    new_img = source.filter(random.choice(rnd_filter))
    new_img = new_img.filter(random.choice(rnd_filter))
    rnd_classes = ['Color',
                   'Contrast',
                   'Brightness',
                   'Sharpness']
    obj = getattr(ImageEnhance, random.choice(rnd_classes))
    new_img = obj(new_img).enhance(random.random() * 2)
    new_img = new_img.convert('RGB')
    new_img.save(filename)
    return filename
