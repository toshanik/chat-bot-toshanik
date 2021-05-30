import random, vk_api, vk, json, re
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
from pathlib import Path
from io import BytesIO
import requests
from vk_api.upload import VkUpload




def get_data():
    try:
        with open("data.json", "w+") as file:
            # Читаем содержимое файла, обрезаем пробелы в начале и в конце
            # (тогда файл содержащий только пробелы или переносы строк
            #  будет эквивалентен пустому файлу)
            file_content = file.read().strip()

            # Проверяем, пустой ли файл
            if not file_content:
                return None

            # Декодируем json
            data = json.loads(file_content)

            # Проверяем, что считана именно строка:
            if not isinstance(data, str):
                return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:  # Некорректное содержимое файла
        return None
    else:
        return data


def remove_word(word, text):
    index = text.find(word)
    if index == -1:
        return text.strip()
    text1 = text[:index]
    text2 = text[index+word.__len__():]
    text3 = text1+text2
    #text = re.sub(word, '', text)
    return text3.strip()


def messages_send(message, chat_id):
    vk.messages.send(
        key=('5e10586fd85a211cb5e26fe53f5ba3f477caa84d'),  # ВСТАВИТЬ ПАРАМЕТРЫ
        server=('https://lp.vk.com/wh204155469'),
        ts=('1'),
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id
    )
    return

def messages_send_attachment(message, chat_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        key=('5e10586fd85a211cb5e26fe53f5ba3f477caa84d'),  # ВСТАВИТЬ ПАРАМЕТРЫ
        server=('https://lp.vk.com/wh204155469'),
        ts=('1'),
        random_id=get_random_id(),
        message=message,
        chat_id=chat_id,
        attachment=attachment
    )
    return

def get_text(event):
    try:
        return event.object.text.strip()
    except:
        return ""

def add_word(type, spec_word, answer="", ):
    data['values'].append({'question': spec_word.lower(), 'answer': answer, 'type': type})
    path.write_text(json.dumps(data), encoding='utf-8')
    message = f'Добавлена фраза: {spec_word}\nС ответом: {answer}'
    messages_send(message, event.chat_id)
    return

def delete_word(spec_word):
    spec_word=spec_word.lower()
    answer = ''
    check = True
    while check:
        check_check = False
        count = -1
        for value in data['values']:
            count += 1
            if value['question'] == spec_word:
                answer = value['answer']
                data['values'].pop(count)
                check_check = True
                break;
        if not check_check:
            check = False
    path.write_text(json.dumps(data), encoding='utf-8')

    message = f'Удалена фраза: {spec_word}\nС ответом: {answer}'
    messages_send(message, event.chat_id)
    return


def upload_photo(upload, url):
    img = requests.get(url).content
    f = BytesIO(img)

    response = upload.photo_messages(f)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key


def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        chat_id=chat_id,
        attachment=attachment
    )
if __name__ == '__main__':
    vk_session = vk_api.VkApi(token='d46a2fe9935df81a4ab27e37f897fb43bd123237bcab1ec388cfdf72f2f84c87c0148f83f04ec04745860')
    longpoll = VkBotLongPoll(vk_session, 204155469)
    vk = vk_session.get_api()
    Lslongpoll = VkLongPoll(vk_session)
    Lsvk = vk_session.get_api()
    upload = VkUpload(vk)

    key = '5e10586fd85a211cb5e26fe53f5ba3f477caa84d'  # ВСТАВИТЬ ПАРАМЕТРЫ
    server = 'https://lp.vk.com/wh204155469'
    ts = '1'

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('!Справка', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('!Словарь', color=VkKeyboardColor.NEGATIVE)

    print("hello world")

    path = Path('data.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            textNormal = get_text(event)
            textLower = textNormal.lower()
            if (textLower == ""):
                continue
            if '!добавить' in textLower:
                if event.from_chat:
                    answer = ""
                    spec_word = remove_word('!добавить', textNormal)
                    spec_word = remove_word('!Добавить', spec_word)


                    if spec_word.find("{") > 0 and spec_word.find("}") > 0:
                        answer = spec_word[spec_word.find("{"): spec_word.find("}") + 1]
                        spec_word = remove_word(answer, spec_word).lower()

                        used = False
                        for item in data['values']:
                            if (item['question'] == spec_word):
                                used =True
                                break;
                        if (used):
                            delete_word(spec_word)
                        add_word('text', spec_word, answer[1:-1])

                    if (answer == ""):
                        try:
                            for item in event.object['attachments']:
                                if 'photo' in item:
                                    url = item['photo']['sizes'][-1]['url']
                                used = False
                                for item in data['values']:
                                    if (item['question'] == spec_word):
                                        used = True
                                        break;
                                if (used):
                                    delete_word(spec_word)
                                add_word('photo', spec_word, url)
                                break;
                        except:
                            messages_send("#2 Не удалось получить фото в сообщении", event.chat_id)
            if '!клавиатура' == event.object.text.lower().strip():
                if event.from_chat:
                    vk.messages.send(
                        keyboard=keyboard.get_keyboard(),
                        key=('5e10586fd85a211cb5e26fe53f5ba3f477caa84d'),  # ВСТАВИТЬ ПАРАМЕТРЫ
                        server=('https://lp.vk.com/wh204155469'),
                        ts=('1'),
                        random_id=get_random_id(),
                        message='Держи',
                        chat_id=event.chat_id
                    )
            if '!справка' in textLower:
                if event.from_chat:
                    messages_send('Доступные команды \n!Добавить \n!Клавиатура \n!Справка \n!Словарь \n!Удалить', event.chat_id)
            if '!словарь' in textLower:
                if event.from_chat:
                    text = ""
                    for item in data['values']:
                        text += item['question']+" -> "+item['answer']+"\n"
                    messages_send(text, event.chat_id)
            if '!удалить' in textLower:
                if event.from_chat:
                    spec_word = remove_word('!удалить', textLower)
                    if spec_word == "":
                        messages_send("Добавьте фразу     (Например: \"!Удалить да\")", event.chat_id)
                    else:
                        delete_word(spec_word)
            for item in data['values']:
                if (item['question'] == textLower):
                    if item['type'] == 'text':
                        messages_send(item['answer'], event.chat_id)
                        break;
                    elif item['type'] == 'photo':
                        messages_send_attachment("", event.chat_id,*upload_photo(upload, item['answer']))
                        #send_photo(vk, event.chat_id, *upload_photo(upload, item['answer']))
                        #if(item['answer'] != ""): messages_send(item['answer'], event.chat_id)

    '''
    for event in Lslongpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            vars1 = ['Привет', 'Ку', 'Хай', 'Хеллоу']
            if event.text in vars1:
                if event.from_user:
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        message = 'Привет)',
                        random_id = get_random_id()
                        )
            vars2 = ['Клавиатура', 'клавиатура']
            if event.text in vars2:
                if event.from_user:
                    Lsvk.messages.send(
                        user_id = event.user_id,
                        random_id = get_random_id(),
                        keyboard = keyboard.get_keyboard(),
                        message = 'Держи'
                        )
    '''
