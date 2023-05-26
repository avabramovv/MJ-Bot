from pylatex.utils import NoEscape

def is_forbiden_name(bot, message):
    if not(message.text.isalnum() and message.text.isascii()):
        bot.send_message(message.chat.id,
         'В названии файла допустими только латинские символы и цифры.')

        return True
    
    if message.text == 'abramov1' or message.text == 'example':
        bot.send_message(message.chat.id, 'Это название недоступно, попробуй другое.')

        return True
    
def to_figures(document, *args):
    document.append(NoEscape('{'))
    for arg in args:
        document.append(arg)
    document.append(NoEscape('}'))

def myLabel(write2, marker):
    write2.append(NoEscape(r'\label{'f'{marker.prefix}:{marker.name}''}'))

def myRef(write2, marker):
    write2.append(NoEscape(r'\ref{'f'{marker.prefix}:{marker.name}''}'))