import xml.etree.ElementTree as XmlElementTree
import httplib2
import urllib.request
import urllib.parse
import uuid
import time
import pyaudio
import wave
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

YANDEX_ASR_HOST = 'asr.yandex.net'
YANDEX_ASR_PATH = '/asr_xml'
CHUNK_SIZE = 1024 ** 2
RATE = 16000
PCM_CHUNK = 1024
THRESHOLD_AFTER_ACTIVATION = 200
THRESHOLD = 200
FORMAT = pyaudio.paInt16  # глубина звука = 16 бит = 2 байта
CHANNELS = 1  # моно
CHUNK = 4000  # кол-во фреймов за один "запрос" к микрофону - тк читаем по кусочкам
RECORD_SECONDS = 5  # длительность записи

KEY = "50c28e18-444d-4011-aeca-1ebaad3020ca"

launch_time = time.time()

def log(s):
    elapsed = time.time() - launch_time
    print(("[%02d:%02d] " % (int(elapsed//60), int(elapsed%60))) + str(s))

def read_chunks(chunk_size, byte_data):
    while True:
        chunk = byte_data[:chunk_size]
        byte_data = byte_data[chunk_size:]

        yield chunk

        if not byte_data:
            break


def record_to_text(data, request_id=uuid.uuid4().hex, topic='notes', lang='ru-RU',
                   key=KEY):

    log("Считывание блока байтов")
    chunks = read_chunks(CHUNK_SIZE, data)

    log("Установление соединения")
    connection = httplib2.HTTPConnectionWithTimeout(YANDEX_ASR_HOST)

    url = YANDEX_ASR_PATH + '?uuid=%s&key=%s&topic=%s&lang=%s' % (
        request_id,
        key,
        topic,
        lang
    )

    log("Запрос к Yandex API")
    connection.connect()
    connection.putrequest('POST', url)
    connection.putheader('Transfer-Encoding', 'chunked')
    connection.putheader('Content-Type', 'audio/x-pcm;bit=16;rate=16000')
    connection.endheaders()

    log("Отправка записи")
    for chunk in chunks:
        connection.send(('%s\r\n' % hex(len(chunk))[2:]).encode())
        connection.send(chunk)
        connection.send('\r\n'.encode())

    connection.send('0\r\n\r\n'.encode())
    response = connection.getresponse()

    log("Обработка ответа сервера")
    if response.code == 200:
        response_text = response.read()
        xml = XmlElementTree.fromstring(response_text)

        if int(xml.attrib['success']) == 1:
            max_confidence = - float("inf")
            text = ''

            for child in xml:
                if float(child.attrib['confidence']) > max_confidence:
                    text = child.text
                    max_confidence = float(child.attrib['confidence'])

            if max_confidence != - float("inf"):
                return text
            else:
                raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
        else:
            raise SpeechException('No text found.\n\nResponse:\n%s' % (response_text))
    else:
        raise SpeechException('Unknown error.\nCode: %s\n\n%s' % (response.code, response.read()))

def text_to_record(text):
    '''
    https://tts.voicetech.yandex.net/generate?
          text=<текст для озвучивания>
        & format=<формат аудио файла>
        & lang=<язык>
        & speaker=<голос>
        & key=<API‑ключ>

        & [emotion=<эмоциональная окраска голоса>]
        & [speed=<скорость речи>]
    '''
    log("Преобразование текста в речь")
    filename = 'audio.wav'
    url = 'https://tts.voicetech.yandex.net/generate?text={text}&format=wav&lang=ru-RU&speaker=jane&key={key}'.format(
        text=urllib.parse.quote(text),
        key=KEY)
    urllib.request.urlretrieve(url, filename)
    return filename

class SpeechException(Exception):
    pass

def record(time):
    audio = pyaudio.PyAudio()

    # открываем поток для чтения данных с устройства записи по умолчанию
    # и задаем параметры
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    result = b''  # список байтовых строк

    # для каждого "запроса"
    for i in range(0, RATE // CHUNK * time):  # RATE // CHUNK - кол-во запросов в секунду
        data = stream.read(CHUNK)  # читаем строку из байт длиной CHUNK * FORMAT = 4000*2 байт
        result += data  # добавляем строку в список

    print("end recording")
    return result

def play(filename):
    file = wave.open(filename)
    data = file.readframes(file.getnframes())
    audio = pyaudio.PyAudio()

    # открываем поток для записи на устройство вывода - динамик - с такими же параметрами
    out_stream = audio.open(format=FORMAT, channels=CHANNELS,
                            rate=file.getframerate(), output=True)
    out_stream.write(data)
    out_stream.close()

def listen(time):
    data = record(time)
    return record_to_text(data)

def say(text):
    play(text_to_record(text))

