import telebot
import texCompiler
import shutil

from telebot import types

def is_forbiden_name(name, message):
    if not(name.isalnum() and name.isascii()):
        bot.send_message(message.from_user.id,
         'В названии файла допустими только латинские символы и цифры.')

        return True
    
    if name == 'abramov1' or name == 'example':
        bot.send_message(message.from_user.id, 'Это название недоступно, попробуй другое.')

        return True

bot = telebot.TeleBot('YOUR TOKEN')
print('Telebot started.\nPress Ctr-C to terminate the proccess\n')

usr = texCompiler.UserInfo()
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/example':
        bot.send_message(message.from_user.id, 'Пример файла.')
        bot.send_document(message.from_user.id, open(r'files/dir-example/example.pdf', 'rb'))
    elif message.text == '/start':
        bot.send_message(message.from_user.id, 'Напиши /example, чтобы получить пример файла.')
        bot.send_message(message.from_user.id, 'Напиши /file, чтобы создать собственный файл.')
    elif message.text == '/file':
        bot.send_message(message.from_user.id, 'Напиши имя.')
        bot.register_next_step_handler(message, get_firstName)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start, чтобы начать.')


def get_firstName(message): #получаем фамилию
    usr.firstName = message.text
    bot.send_message(message.from_user.id, 'Напиши фамилию.')
    bot.register_next_step_handler(message, get_secondName)

def get_secondName(message):
    usr.secondName = message.text
    bot.send_message(message.from_user.id, 'Напиши дату.')
    bot.send_message(message.from_user.id, 'Если требуется сегодняшняя дата,\nнапиши /today.')
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    if message.text == r'/today':
        usr.date = r'\today'
    else:
        usr.date = message.text
    bot.send_message(message.from_user.id, 'Напиши заголовок.')
    bot.register_next_step_handler(message, get_title)

def get_title(message):
    usr.title = message.text
    bot.send_message(message.from_user.id, 'Введи текст.')
    bot.register_next_step_handler(message, get_text)

def get_text(message):
    print(47, message.text)
    usr.text = message.text
    bot.send_message(message.from_user.id, 'Напиши название файла.')
    print(50, message.text)
    bot.register_next_step_handler(message, check_name)

def check_name(message):
    if is_forbiden_name(message.text, message):
        bot.send_message(message.from_user.id, 'Напиши название файла.')
        bot.register_next_step_handler(message, check_name)
    else:
        get_name(message)
        

def get_name(message):
    usr.name = message.text
    bot.send_message(message.from_user.id, 'Спасибо, ожидай файл!')

    texCompiler.build_tex(usr)
    texCompiler.compile_tex(usr.name)

    bot.send_message(message.from_user.id, 'Твой файл!')
    bot.send_document(message.from_user.id, open(f'files/dir-{usr.name}/{usr.name}.pdf', 'rb'))

    shutil.rmtree(f'files/dir-{usr.name}/')
    

bot.polling(none_stop=True, interval=0)
        
