import telebot
from telebot import types

from texhandler import *

from pylatex import Document

from entities_handler import ent2latex, only_quots

import shutil

bot = telebot.TeleBot('6120587308:AAGy1kJpZM3v9JFwqMaJhI1NUjuxRTTeUdo')
print('Bot started.\nPress Ctr-C to terminate the proccess\n')

users = {}

def start_reply_kb():
    reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_yes = types.KeyboardButton(text='Да')
    btn_no = types.KeyboardButton(text='Нет')

    reply_kb.add(btn_yes, btn_no)

    return reply_kb

def type_reply_kb():
    reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_issl = types.KeyboardButton(text='Исследовательский')
    btn_prog = types.KeyboardButton(text='Программный')

    reply_kb.add(btn_issl, btn_prog)

    return reply_kb

@bot.callback_query_handler(func=lambda callback: callback.data)
def check_choice(callback):
    if callback.data == 'doc_name':
        bot.send_message(callback.message.chat.id, 'Введите название файла')
        bot.register_next_step_handler(callback.message, change_doc_name)
    elif callback.data == 'doc_font_size':
        bot.send_message(callback.message.chat.id, 'Введите размер шрифта (pt)')
        bot.register_next_step_handler(callback.message, change_doc_font_size)
    elif callback.data == 'doc_geometry':
        bot.send_message(callback.message.chat.id, 'Введи размеры полей <i><b>через пробел</b></i>\n(левое правое верхнее нижнее)', parse_mode='HTML')
        bot.register_next_step_handler(callback.message, change_doc_geometry)
    elif callback.data == 'online':
        users["{0}".format(callback.message.chat.id)].bib_refs.append(BibOnline())

        curr_bib = users["{0}".format(callback.message.chat.id)].bib_refs[-1]

        bot.send_message(callback.message.chat.id, 
                         '⚠️ Введите <b>краткое название</b> источника (на английском)\n\n'\
                         'Например: <i>chirkova18_arxiv</i>', parse_mode='HTML')
        bot.register_next_step_handler(callback.message, bib_set_label, curr_bib)
    elif callback.data == 'book':
        users["{0}".format(callback.message.chat.id)].bib_refs.append(BibBook())

        curr_bib = users["{0}".format(callback.message.chat.id)].bib_refs[-1]

        bot.send_message(callback.message.chat.id, 
                         '⚠️ Введите <b>краткое название</b> источника (на английском)\n\n'\
                         'Например: <i>chirkova18_arxiv</i>', parse_mode='HTML')
        bot.register_next_step_handler(callback.message, bib_set_label, curr_bib)
    elif callback.data == 'inbook':
        users["{0}".format(callback.message.chat.id)].bib_refs.append(BibInbook())

        curr_bib = users["{0}".format(callback.message.chat.id)].bib_refs[-1]

        bot.send_message(callback.message.chat.id, 
                         '⚠️ Введите <b>краткое название</b> источника (на английском)\n\n'\
                         'Например: <i>chirkova18_arxiv</i>', parse_mode='HTML')
        bot.register_next_step_handler(callback.message, bib_set_label, curr_bib)
    elif callback.data == 'article':
        users["{0}".format(callback.message.chat.id)].bib_refs.append(BibArticle())

        curr_bib = users["{0}".format(callback.message.chat.id)].bib_refs[-1]

        bot.send_message(callback.message.chat.id, 
                         '⚠️ Введите <b>краткое название</b> источника (на английском)\n\n'\
                         'Например: <i>chirkova18_arxiv</i>', parse_mode='HTML')
        bot.register_next_step_handler(callback.message, bib_set_label, curr_bib)
    
def change_doc_name(message):
    # name : string
    users["{0}".format(message.chat.id)].default_filepath_ = message.text
    bot.send_message(message.chat.id, 'Требуется ли изменить параметры?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, is_change)

def change_doc_font_size(message):
    # size : string, int
    size = message.text
    users["{0}".format(message.chat.id)].font_size_ = f'{size}pt'
    bot.send_message(message.chat.id, 'Требуется ли изменить параметры?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, is_change)

def change_doc_geometry(message):
    # all : int
    l = list(map(int, message.text.split()))
    left = l[0]
    right = l[1]
    top = l[2]
    bottom = l[3]

    users["{0}".format(message.chat.id)].geometry_options_ = {
                   'left': f'{left}mm',
                   'right': f'{right}mm',
                   'top': f'{top}mm',
                   'bottom': f'{bottom}mm'}
    
    bot.send_message(message.chat.id, 'Требуется ли изменить параметры?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, is_change)

def add_dirs(message):
    print('Adding dirs...')

    # Добавляем папку, где будет храниться информация пользователя
    usr_dir_path = 'users/dir-' + str(message.chat.id)
    os.mkdir(usr_dir_path)

    # Добавляем папку, где будут храниться картинки пользователя
    usr_graphics_path = os.path.join(usr_dir_path, 'graphics')
    os.mkdir(usr_graphics_path)

    users["{0}".format(message.chat.id)].default_filepath_ = usr_dir_path
    users["{0}".format(message.chat.id)].title_name_ = os.path.join(usr_dir_path, 'title')
    users["{0}".format(message.chat.id)].chat_id = message.chat.id
    users["{0}".format(message.chat.id)].path = usr_dir_path
    users["{0}".format(message.chat.id)].graphics_path = usr_graphics_path
    users["{0}".format(message.chat.id)].bib_path = os.path.join(usr_dir_path, 'refs')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '👋 <b>Добро пожаловать!</b>\n\n'\
                     'Бот помогает заполнить отчет по курсовому проекту, <b>автоматически добавляя все рекомендации по оформлению.</b>'\
                     'В конце работы вы получите ваш pdf-файл\n\n'
                     'Перед работой с ботом, советуем прочитать рекомендации по содержанию: '\
                     r'https://docs.google.com/document/d/1Mjhw5jVO1bv-XD1PrSyE2nhg8F-z1W9b/edit', parse_mode='HTML')
    
    bot.send_message(message.chat.id, 'ℹ️ <b>Доступные комманды:</b> \n\n'\
                     '''/start - Начать
/makefile - Создать документ
/section - Добавить главу
/subsection - Добавить подглаву
/subsubsection - Добавить подподглаву
/paragraph - Начать новый параграф
/table - Добавить таблицу
/list - Добавить список
/math - Добавить простое уравнение
/cite - Добавить ссылку на библиографию
/next - Перейти к заполнению нового раздела''', parse_mode='HTML')
    
    bot.send_message(message.chat.id, '📝 Для того, чтобы добавить текст, просто введите его и отправьте.\n\n'\
                     'Бот поддерживает жирный шрифт, курсив, зачеркивание и подчеркивание прямо из Telegram')
    
    bot.send_message(message.chat.id, '🖼 Для отправки изображения, просто отправьте его\n\n'
                     '❗️ В десктопной версии приложения потребуется добавить пункт <b>сжать изображение</b>', parse_mode='HTML')
    
    bot.send_message(message.chat.id, '🖊 Для того, чтобы приступить к <b>заполнению отчета</b>, введите комманду /makefile', parse_mode='HTML')

@bot.message_handler(commands=['makefile'])
def makefile(message):
    users["{0}".format(message.chat.id)] = UserInfo2()
    add_dirs(message)
    
    bot.send_message(message.chat.id, '⚠️ Сейчас вам предстоит ввести параметры документа')
    bot.send_message(message.chat.id, 
    '<b>Стандартные параметры документа:</b>\n'\
    '◽️ Имя файла: your_file\n'\
    '◽️ Размер страницы: A4\n'\
    '◽️ Размер шрифта: 12 пт\n'\
    '◽️ Поля:\n'\
        '    ▫️ Левое: 25 мм\n'\
        '    ▫️ Правое: 10 мм\n'\
        '    ▫️ Верхнее: 20 мм\n'\
        '    ▫️ Нижнее: 20 мм\n',
        parse_mode='HTML')

    bot.send_message(message.chat.id, '⚠️ Требуется ли изменить параметры?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, is_change)

def is_change(message):
    if message.text == 'Да':
        kb = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='Имя файла', callback_data='doc_name')
        btn2 = types.InlineKeyboardButton(text='Размер шрифта', callback_data='doc_font_size')
        btn3 = types.InlineKeyboardButton(text='Поля', callback_data='doc_geometry')
        kb.add(btn1, btn2, btn3)

        bot.send_message(message.chat.id, '...', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, '⚠️ Выберите параметр, который требуется изменить', reply_markup=kb)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, '✅ Переходим к созданию титульного листа', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id,
                      '⚠️ Введите ФИО студента\n\n'\
                      'Введите в формате: <i>Фамилия Имя Отчество</i>', parse_mode='HTML')
        bot.register_next_step_handler(message, set_title_student)
    else:
        bot.send_message(message.chat.id, '❗️ Выберите ответ на кнопке')
        bot.send_message(message.chat.id, '⚠️ Требуется ли изменить параметры?', reply_markup=start_reply_kb())
        bot.register_next_step_handler(message, is_change)

def set_title_student(message):
    users["{0}".format(message.chat.id)].student_ = message.text
    bot.send_message(message.chat.id, '⚠️ Выберите тип вашего проекта', reply_markup=type_reply_kb())
    bot.register_next_step_handler(message, set_title_type)

def set_title_type(message):
    if message.text == 'Исследовательский':
        users["{0}".format(message.chat.id)].type_ = 'б исследовательском'
    elif message.text == 'Программный':
        users["{0}".format(message.chat.id)].type_ = ' программном'
    else:
        bot.send_message(message.chat.id, '❗️ Выберите ответ на кнопке')
        bot.send_message(message.chat.id, '⚠️ Введите тип вашего проекта', reply_markup=type_reply_kb())
        bot.register_next_step_handler(message, set_title_type) 

    if message.text == 'Исследовательский' or message.text == 'Программный':
        bot.send_message(message.chat.id, '⚠️ Введите тему вашего проекта', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, set_title_topic)

def set_title_topic(message):
    users["{0}".format(message.chat.id)].topic_ = only_quots(message.text)
    bot.send_message(message.chat.id, '⚠️ Введите номер вашей группы')
    bot.register_next_step_handler(message, set_title_group)

def set_title_group(message):
    users["{0}".format(message.chat.id)].group_ = message.text
    bot.send_message(message.chat.id,
                      '⚠️ Введите ФИО руководителя проекта\n\n'\
                      'Введите в формате: <i>Фамилия Имя Отчество</i>', parse_mode='HTML')
    bot.register_next_step_handler(message, set_title_assistant)

def set_title_assistant(message):
    users["{0}".format(message.chat.id)].assistant_ = message.text
    bot.send_message(message.chat.id, '⚠️ Введите должность вашего руководителя')
    bot.register_next_step_handler(message, set_title_post)

def set_title_post(message):
    users["{0}".format(message.chat.id)].post_ = message.text
    bot.send_message(message.chat.id,
                      '⚠️ Введите место работы вашего руководителя в родительном падеже\n\n'\
                      'Например: Факультета компьютерных наук НИУ ВШЭ')
    bot.register_next_step_handler(message, set_title_work)

def set_title_work(message):
    users["{0}".format(message.chat.id)].work_ = message.text
    set_title(
              title_name=users["{0}".format(message.chat.id)].title_name_,
              type = users["{0}".format(message.chat.id)].type_,
              topic=users["{0}".format(message.chat.id)].topic_,
              student=users["{0}".format(message.chat.id)].student_,
              group=users["{0}".format(message.chat.id)].group_,
              assistant=users["{0}".format(message.chat.id)].assistant_,
              post=users["{0}".format(message.chat.id)].post_,
              work=users["{0}".format(message.chat.id)].work_)
    
    bot.send_message(message.chat.id, '✅ Переходим к заполнению библиографии')
    bot_add_bib(message)

def set_annot(message):
    users["{0}".format(message.chat.id)].next = set_key_words

    users["{0}".format(message.chat.id)].document_ = set_tex_document(users["{0}".format(message.chat.id)])
    add_tex_packages(users["{0}".format(message.chat.id)].document_)
    add_tex_preamble(users["{0}".format(message.chat.id)].document_)
    add_tex_title(users["{0}".format(message.chat.id)].document_, 'title')
    add_tex_table_of_contents(users["{0}".format(message.chat.id)].document_)

    users["{0}".format(message.chat.id)].annotation_ = add_tex_annotation(users["{0}".format(message.chat.id)].document_)

    bot.send_message(message.chat.id, '⚠️ Введите текст аннотации')
    bot.send_message(message.chat.id, '🪄 Чтобы ввести текст с нового абзаца введите команду /paragraph\n\n'\
                     '🪄 Чтобы перейти заполнению нового раздела введите команду /next')
    
def set_key_words(message):
    users["{0}".format(message.chat.id)].next = None
    bot.send_message(message.chat.id, 'ℹ️ Теперь вам предстоит заполнить <b><i>Список ключевых слов</i></b>', parse_mode='HTML')
    bot.send_message(message.chat.id, 
                     '❔ <b><i>Подсказка</i></b>\n\n'\
                     '5-10 слов или фраз, характеризующих содержание '\
                     '(на том же языке, на котором написан текст работы)', parse_mode='HTML')
    bot.send_message(message.chat.id, '⚠️ Введите ключевые слова через запятую с пробелом\n\n'\
                     'Например: <i>Глубинное обучение, разреживание моделей, рекуррентные нейронные сети</i>', parse_mode='HTML')
    bot.register_next_step_handler(message, set_intro)

def set_intro(message):
    users["{0}".format(message.chat.id)].next = None
    add_tex_key_words(users["{0}".format(message.chat.id)].document_, message.text)

    bot.send_message(message.chat.id, 'ℹ️ Теперь вам предстоит заполнить <b><i>Введение</i></b>', parse_mode='HTML')
    bot.send_message(message.chat.id, 
                     '❔ <b><i>Подсказка</i></b>\n\n'\
                     'По смыслу, это одновременно неформальное введение '\
                     'в работу и пересказ работы длиной 1-2 страницы. '\
                     'В введении обычно дается описание <i>предметной области</i>, '\
                     'неформально формулируется <i>постановка задачи</i>, описывается '\
                     'ее актуальность и значимость, неформально описываются '\
                     '<i>основные результаты работы</i>, в том числе их новизна и значимость. '\
                     'При выполнении группового проекта в конце введения стоит описать '\
                     'структуру деления задач между участниками проекта.', parse_mode='HTML')
    
    users["{0}".format(message.chat.id)].next = set_literature

    bot_add_section(message, 'Введение')
    bot.send_message(message.chat.id, '⚠️ Начинайте заполнять этот раздел')

def set_literature(message):
    users["{0}".format(message.chat.id)].next = bot_add_chapters

    bot.send_message(message.chat.id, 'ℹ️ Теперь вам предстоит заполнить <b><i>Обзор литературы</i></b>', parse_mode='HTML')
    bot.send_message(message.chat.id, 
                     '❔ <b><i>Подсказка</i></b>\n\n'\
                     'Краткое описание и характеристика релевантных работ. Для исследовательского проекта: позиционирование вашей работы относительно других современных работ (к примеру: предложенный метод эффективнее работы [1] потому-то, в работе исследуется дополнительный случай, который не исследуется в [2] и т.п.). Для программного проекта: обзор похожих программных решений, их сравнительный анализ и описание почему их нельзя использовать для решения поставленной задачи. Обзор литературы не должен выглядеть как перечисление релевантных работ, он должен включать в себя анализ этих работ и позиционировать вашу работу относительно других существующих работ.', parse_mode='HTML')

    bot_add_section(message, 'Обзор литературы')
    bot.send_message(message.chat.id, '⚠️ Начинайте заполнять этот раздел')


# Image adder
@bot.message_handler(content_types=['photo'])
def bot_set_image(message):
    photo_id = message.photo[-1].file_id
    file_photo = bot.get_file(photo_id)

    filedir_and_name, file_extencion = os.path.splitext(file_photo.file_path)
    downloaded_file_photo = bot.download_file(file_photo.file_path)

    filedir, filename = os.path.split(filedir_and_name)
    print(filedir)
    print(filename, file_extencion)
    src = os.path.join(users["{0}".format(message.chat.id)].graphics_path, filename + file_extencion)
    no_dir_src = filename + file_extencion
    with open(src, 'wb') as local_file:
        local_file.write(downloaded_file_photo)

    bot.send_message(message.chat.id, '❔ <b>Подсказка</b>\n\n'\
                     'В описании поясните, что происходит на изображении', parse_mode='HTML')
    bot.send_message(message.chat.id, '⚠️ Введите <b>описание изображения</b>', parse_mode='HTML')
    bot.register_next_step_handler(message, bot_add_image, no_dir_src, filename)

def bot_add_image(message, path, label):
    add_image(users["{0}".format(message.chat.id)].document_, path, message.text, label_name=label)
    bot.send_message(message.chat.id, '✅ Изображение было успешно добавлено')

# Table adder
@bot.message_handler(commands=['table'])
def bot_set_table(message):
    bot.send_message(message.chat.id, '⚠️ Введите <b>размер таблицы</b> через <b>пробел</b>\n\n'\
                     'Например, если хотите ввести таблицу размера 4 на 5, введите <i>4 5</i>', parse_mode='HTML')
    
    bot.register_next_step_handler(message, bot_add_table)

def set_table_data(message, num_of_rows, num_of_columns, i, j):
    print(i, j)
    if i < num_of_rows:
        if j < num_of_columns:
            users["{0}".format(message.chat.id)].table_data[i][j] = message.text
            if i + 1 == num_of_rows and j + 1 == num_of_columns:
                bot.send_message(message.chat.id, '⚠️ Введите описание таблицы')
                bot.register_next_step_handler(message, set_table_caption, num_of_rows, num_of_columns)
                return
            if j + 1 == num_of_columns:
                bot.send_message(message.chat.id,
                      '⚠️ Введите данные в\n'\
                      f'{i + 1 + 1} строку, 1 столбец')
            else:
                bot.send_message(message.chat.id,
                      '⚠️ Введите данные в\n'\
                      f'{i + 1} строку, {j + 1 + 1} столбец')
            bot.register_next_step_handler(message, set_table_data, num_of_rows, num_of_columns, i, j + 1)
        else:
            set_table_data(message, num_of_rows, num_of_columns, i + 1, 0)
    else:
        bot.send_message(message.chat.id, '⚠️ Введите описание таблицы')
        bot.register_next_step_handler(message, set_table_caption, num_of_rows, num_of_columns)

def set_table_caption(message, num_of_rows, num_of_columns):
    add_table(users["{0}".format(message.chat.id)].document_, message.text, num_of_rows, num_of_columns, users["{0}".format(message.chat.id)].table_data)
    users["{0}".format(message.chat.id)].table_data.clear()
    bot.send_message(message.chat.id, '✅ Таблица была успешно добавлена')


def bot_add_table(message):
    rows, clmns = map(int, message.text.split())
    users["{0}".format(message.chat.id)].table_data = [['' for i in range(clmns)] for j in range(rows)]

    bot.send_message(message.chat.id,
                      '⚠️ Введите данные в\n'\
                      '1 строку, 1 столбец')
    bot.register_next_step_handler(message, set_table_data, rows, clmns, 0, 0)

# List adder
@bot.message_handler(commands=['list'])
def bot_set_list(message):
    reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton(text='Нумерованный список')
    btn2 = types.KeyboardButton(text='Маркированный список (список с точками)')
    reply_kb.add(btn1, btn2)

    bot.send_message(message.chat.id, '⚠️ Выберите, какой список хотите добавить', reply_markup=reply_kb)
    bot.register_next_step_handler(message, bot_set_list_items)

def add_list_items(message, list_type):
    if message.text == '0':
        if list_type == 'enum':
            add_list_enumerate(users["{0}".format(message.chat.id)].document_, users["{0}".format(message.chat.id)].items)
            users["{0}".format(message.chat.id)].items.clear()
        elif list_type == 'itemize':
            add_list_itemize(users["{0}".format(message.chat.id)].document_, users["{0}".format(message.chat.id)].items)
            users["{0}".format(message.chat.id)].items.clear()

        bot.send_message(message.chat.id, '✅ Список был успешно добавлен')
    else:
        users["{0}".format(message.chat.id)].items.append(message.text)
        bot.send_message(message.chat.id, '⚠️ Введите элемент списка\n\n'\
                     'Чтобы закончить ввод, введите 0', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_list_items, list_type)

def bot_set_list_items(message):
    if message.text == 'Нумерованный список':
        bot.send_message(message.chat.id, '⚠️ Введите элемент списка\n\n'\
                     'Чтобы закончить ввод, введите 0', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_list_items, 'enum')
    elif message.text == 'Маркированный список (список с точками)':
        bot.send_message(message.chat.id, '⚠️ Введите элемент списка\n\n'\
                     'Чтобы закончить ввод, введите 0', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_list_items, 'itemize')
    else:
        print('hz')

# Math adder
@bot.message_handler(commands=['math'])
def bot_set_math(message):
    bot.send_message(message.chat.id, '⚠️ Введите простое уравнение\n\n'\
                     'Например, <i>y = 5x^2 + 3</i>', parse_mode='HTML')
    
    bot.register_next_step_handler(message, bot_add_math)

def bot_add_math(message):
    add_math(users["{0}".format(message.chat.id)].document_, NoEscape(message.text))
    bot.send_message(message.chat.id, '✅ Уравнение было успешно добавлено')

# Cite adder
def txt_arr_cites(message):
    result = ''
    for key in users["{0}".format(message.chat.id)].cites_:
        if not users["{0}".format(message.chat.id)].cites_[key].is_triggered:
            result += (key + '\n')

    return result

@bot.message_handler(commands=['cite'])
def bot_add_cite(message):
    if users["{0}".format(message.chat.id)].triggered_len > 0:
        bot.send_message(message.chat.id, 'ℹ️ Вы еще не сослались на следующие источники:\n\n{0}'.format(txt_arr_cites(message)))

    cites_reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for key in users["{0}".format(message.chat.id)].cites_:
        cites_reply_kb.add(types.KeyboardButton(text=key))

    bot.send_message(message.chat.id, '⚠️ Выберите, на какой источник хотите сослаться', reply_markup=cites_reply_kb)
    bot.register_next_step_handler(message, bot_cite_handler)

def bot_cite_handler(message):
    if message.text not in users["{0}".format(message.chat.id)].cites_:
        cites_reply_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
        for key in users["{0}".format(message.chat.id)].cites_:
            cites_reply_kb.add(types.KeyboardButton(text=key))

        bot.send_message(message.chat.id, '❗️ Выберите ответ на кнопке!')
        bot.send_message(message.chat.id, '⚠️ Выберите, на какой источник хотите сослаться', reply_markup=cites_reply_kb)
        bot.register_next_step_handler(message, bot_cite_handler)

    add_cite(users["{0}".format(message.chat.id)].document_, message.text)
    users["{0}".format(message.chat.id)].cites_[message.text].is_triggered = True
    users["{0}".format(message.chat.id)].triggered_len -= 1
    bot.send_message(message.chat.id, f'✅ Была добавлена ссылка на {message.text}', reply_markup=types.ReplyKeyboardRemove())


def bot_add_chapters(message):
    users["{0}".format(message.chat.id)].next = bot_add_conclusion
    bot_send_hint_sections(message)
    bot_send_hint_subsections(message)
    bot_send_hint_subsubsections(message)
    bot.send_message(message.chat.id, 'ℹ️ Теперь вам предстоит заполнить <b><i>ваши главы</i></b>\n\n'\
                     'Выше были даны указания, как правильно добавлять главы, подглавы и подподглавы. '\
                     'Все что вы введете после комманды, будет добавлено в выбранную секцию.\n\n'\
                     'Например вы введете /section, после этого введете называние главы.'\
                     'Комманда subsection, добавит подгаву этой главы. Если после этого вы начнете вводить текст или пришлете '\
                     'картинку, то они добавятся в эту подглаву.\n\n'\
                     'Если же вы захотите, начать новую подглаву или главу, введите команды /subsection или /section соответственно\n\n', parse_mode='HTML')
    
    bot.send_message(message.chat.id, '❔ <b>Подсказка</b>\n\n'\
                     'Главы (обычно от 2 до 5). Здесь структура сильно зависит от темы проекта.'\
                     'Например, работа, предлагающая некий новый метод решения какой-то задачи, может содержать следующие главы: формальная постановка задачи и анализ ее особенностей, описание предлагаемого метода, теоретический анализ метода, экспериментальное исследование и сравнение с аналогами.\n\n'\
                     'Например, работа, исследующая особенности применения некоторого метода для различных задач, может содержать следующие главы: описание метода, обзор применимости метода для различных задач с описанием этих задач, анализом и обоснованием выбора конкретных задач для вашего исследования,  экспериментальный анализ применимости метода к задаче 1 в сравнении с аналогами, то же для задачи 2 и т.д. \n\n'\
                     'Например, работа, посвященная разработке программной системы для решения практической задачи, может содержать следующие главы: описание и обоснование всех выбранных архитектурных решений/алгоритмов/технологий, описание подхода к тестированию разработанного решения и обоснование выбранных метрик качества, результаты тестирования разработанной системы и ее сравнение с известными аналогами. \n\n'\
                     'Каждую главу, для которой это уместно, стоит завершать кратким заключением с основными выводами. Это поможет выделить основные результаты текущей главы и плавно перейти к следующей главе.',
                     parse_mode='HTML')
    bot.send_message(message.chat.id, '⚠️ Если захотите перейти к разделу <b>Заключение</b>, воспользуйтесь коммандой /next', parse_mode='HTML')

def bot_add_conclusion(message):
    users["{0}".format(message.chat.id)].next = bot_set_bib
    bot.send_message(message.chat.id, 'ℹ️ Теперь вам предстоит заполнить <b><i>заключение</i></b>\n\n', parse_mode='HTML')
    bot.send_message(message.chat.id, '❔ <b>Подсказка</b>\n\n'\
                     'Перечисление и характеристика результатов работы (как положительных, так и отрицательных, если таковые есть), перспективы дальнейшей деятельности. ', parse_mode='HTML')
    bot_add_section(message, 'Заключение')
    bot.send_message(message.chat.id, '⚠️ Введите содержание заключения')

def bot_set_bib(message):
    add_tex_literature(users["{0}".format(message.chat.id)].document_)
    end_doc(message)

# End document
def end_doc(message):
    bot.send_message(message.chat.id, '✅ <b>Заполнение работы закончено!</b>', parse_mode='HTML')
    bot.send_message(message.chat.id, '⏳ <b>Ваш файл...</b>', parse_mode='HTML')

    users["{0}".format(message.chat.id)].document_.generate_tex(os.path.join(users["{0}".format(message.chat.id)].path, 'your_file'))
    compile_tex(message)

    bot.send_document(message.chat.id, open(os.path.join(users["{0}".format(message.chat.id)].path, 'your_file.pdf'), 'rb'))
    shutil.rmtree(users["{0}".format(message.chat.id)].path)
    bot.send_message(message.chat.id, '🖊 Для того, чтобы приступить к новому <b>заполнению отчета</b>, введите комманду /makefile', parse_mode='HTML')


def compile_tex(message):
    os.chdir(users["{0}".format(message.chat.id)].path)
    os.system('pdflatex ' + 'your_file')

    os.system('biber ' + 'your_file')

    os.system('pdflatex ' + 'your_file')
    os.system('pdflatex ' + 'your_file')
    os.system('pdflatex ' + 'your_file')

    os.chdir('../../')

# Section adder
def bot_add_section(message, title):
    if title == None:
        title = message.text
    bot.send_message(message.chat.id, f'✅ Был добавлен раздел {title}')
    add_tex_section(users["{0}".format(message.chat.id)].document_, title)

@bot.message_handler(commands=['section'])
def bot_new_sect(message):
    bot_send_hint_sections(message)
    bot.send_message(message.chat.id, '⚠️ Введите имя раздела')
    bot.register_next_step_handler(message, bot_add_section, None)


# Subsection adder
def bot_add_subsection(message, title):
    if title == None:
        title = message.text
    bot.send_message(message.chat.id, f'✅ Был добавлен подраздел {title}')
    add_tex_subsection(users["{0}".format(message.chat.id)].document_, title)

@bot.message_handler(commands=['subsection'])
def bot_new_subsect(message):
    bot_send_hint_subsections(message)
    bot.send_message(message.chat.id, '⚠️ Введите имя подраздела')
    bot.register_next_step_handler(message, bot_add_subsection, None)


# Subsubsection adder
def bot_add_subsubsection(message, title):
    if title == None:
        title = message.text
    bot.send_message(message.chat.id, f'✅ Был добавлен подподраздел {title}')
    add_tex_subsubsection(users["{0}".format(message.chat.id)].document_, title)

@bot.message_handler(commands=['subsubsection'])
def bot_new_subsubsect(message):
    bot_send_hint_subsubsections(message)
    bot.send_message(message.chat.id, '⚠️ Введите имя подподраздела')
    bot.register_next_step_handler(message, bot_add_subsubsection, None)


# Next adder
@bot.message_handler(commands=['next'])
def bot_next(message):
    bot.send_message(message.chat.id, '✅ Переходим к заполению следующего раздела')
    users["{0}".format(message.chat.id)].next(message)


# Paragraph adder
@bot.message_handler(commands=['paragraph'])
def bot_new_par(message):
    bot.send_message(message.chat.id, '✅ Был добавлен новый параграф')
    add_paragraph(users["{0}".format(message.chat.id)].document_)

# Text adder
@bot.message_handler(content_types=['text'])
def bot_add_text(message):
    
    add_text(users["{0}".format(message.chat.id)].document_, only_quots(ent2latex(message)))
    bot.send_message(message.chat.id, '✅ Текст был успешно добавлен')
    bot_send_hint_text(message)

def bot_gen_tex(message):
    bot.send_message(message.chat.id, 'Сгенерирован tex-файл')
    users["{0}".format(message.chat.id)].document_.generate_tex('simpletex')


# Hint adders
def bot_send_hint_sections(message):
    bot.send_message(message.chat.id, '🪄 Чтобы добавить раздел введите комманду /section\n\n'\
                     'Все, что вы введете после этой команды будет добавлено в этот раздел (в том числе и посекции и подподсекции)\n\n'\
                     '🪄 Чтобы перейти к заполнению нового раздела введите комманду /next')
    
def bot_send_hint_subsections(message):
    bot.send_message(message.chat.id, '🪄 Чтобы добавить подраздел введите комманду /subsection\n\n'\
                     'Все, что вы введете после этой команды будет добавлено в этот раздел (в том числе и подподсекции)\n\n'\
                     '🪄 Чтобы перейти к заполнению нового раздела введите комманду /next')
    
def bot_send_hint_subsubsections(message):
    bot.send_message(message.chat.id, '🪄 Чтобы добавить подподраздел введите комманду /subsubsection\n\n'\
                     'Все, что вы введете после этой команды будет добавлено в этот раздел\n\n'\
                     '🪄 Чтобы перейти к заполнению нового раздела введите комманду /next')

def bot_send_hint_text(message):
    bot.send_message(message.chat.id, '🪄 Чтобы ввести текст с нового абзаца введите комманду /paragraph\n\n'\
                     '🪄 Чтобы перейти к заполнению нового раздела введите комманду /next')


# -------------------------------------------------------------------------------------------------------------------------------------------

def bib_inline_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='🌐 Онлайн источник', callback_data='online')
    btn2 = types.InlineKeyboardButton(text='📚 Книга', callback_data='book')
    btn3 = types.InlineKeyboardButton(text='📖 Глава из книги', callback_data='inbook')
    btn4 = types.InlineKeyboardButton(text='🧾 Статья', callback_data='article')
    btn5 = types.InlineKeyboardButton(text='🔬 Конференция', callback_data='inproceedings')
    kb.add(btn1, btn2, btn3, btn4, row_width=1)

    return kb

# @bot.callback_query_handler(func=lambda callback: callback.data)
# def check_choice(callback):
#     bot.send_message(callback.message.chat.id, '📍 Приступим к заполнению библиографии')
#     if callback.data == 'online':
#         users["{0}".format(message.chat.id)].bib_refs.append(BibOnline())
#     elif callback.data == 'book':
#         users["{0}".format(message.chat.id)].bib_refs.append(BibBook())
#     elif callback.data == 'inbook':
#         users["{0}".format(message.chat.id)].bib_refs.append(BibInbook())
#     elif callback.data == 'article':
#         users["{0}".format(message.chat.id)].bib_refs.append(BibArticle())

#     curr_bib = users["{0}".format(message.chat.id)].bib_refs[-1]

#     bot.send_message(callback.message.chat.id, 
#                          '⚠️ Введите <b>краткое название</b> источника (на английском)\n\n'\
#                          'Например: <i>chirkova18_arxiv</i>', parse_mode='HTML')
#     bot.register_next_step_handler(callback.message, bib_set_label, curr_bib)

# Bib adders
def bib_set_label(message, bib_ref):
    bib_ref.label = message.text.lower()

    bot.send_message(message.chat.id, 
                         '⚠️ Введите <b>Автора</b>\n\n'\
                         'Например: <i>Nadezhda Chirkova</i> или <i>Donald E. Knuth</i>\n'\
                         'Если конкретного автора нет, введите 0\n', 
                         parse_mode='HTML')
    bot.register_next_step_handler(message, bib_set_author, bib_ref)

def bib_set_author(message, bib_ref):
    if message.text != '0':
        bib_ref.author = message.text
    else:
        bib_ref.author = ''

    bot.send_message(message.chat.id, 
                         '⚠️ Введите <b>название</b>\n\n'\
                         'Например: <i>Knuth: Computers and Typesetting</i>', 
                         parse_mode='HTML')
    bot.register_next_step_handler(message, bib_set_title, bib_ref)

def bib_set_title(message, bib_ref):
    bib_ref.title = message.text

    if isinstance(bib_ref, BibOnline):
        bot.send_message(message.chat.id, 
                         '⚠️ Введите <b>Ссылку на материал</b>\n\n'\
                         'Например: <i>http://www-cs-faculty.stanford.edu/~uno/abcde.html</i>', 
                         parse_mode='HTML')
        bot.register_next_step_handler(message, bib_set_url, bib_ref)
    elif isinstance(bib_ref, BibBook) or isinstance(bib_ref, BibInbook):
        bot.send_message(message.chat.id, '⚠️ Введите <b>Издательство</b>\n\n'\
                         'Например: <i>Addison-Wesley</i>', 
                         parse_mode='HTML')
        bot.register_next_step_handler(message, bib_set_publisher, bib_ref)
    elif isinstance(bib_ref, BibArticle):
        bot.send_message(message.chat.id, '⚠️ Введите <b>Год выпуска материала</b>\n\n'\
                         'Например: <i>1968</i>', 
                         parse_mode='HTML')
        bot.register_next_step_handler(message, bib_set_year, bib_ref)

def bib_set_publisher(message, bib_ref):
    bib_ref.publisher = message.text

    bot.send_message(message.chat.id, '⚠️ Введите <b>Год выпуска материала</b>\n\n'\
                         'Например: <i>1968</i>', 
                         parse_mode='HTML')
    bot.register_next_step_handler(message, bib_set_year, bib_ref)

def bib_set_year(message, bib_ref):
    bib_ref.year = message.text

    if isinstance(bib_ref, BibBook):
        bot.send_message(message.chat.id, '⚠️ Введите <b>серию книги</b>\n\n'\
                         'Например: <i>Four volumes</i>\n\n'\
                         'Если такой нет, введите 0', 
                         parse_mode='HTML')
        bot.register_next_step_handler(message, bib_set_series, bib_ref)
    elif isinstance(bib_ref, BibInbook):
        bot.send_message(message.chat.id, '⚠️ Введите <b>номер главы</b>, на которую хотите сослаться\n\n'\
                         'Например: <i>1.2</i>\n\n',
                         parse_mode='HTML')
        bot.register_next_step_handler(message, bib_set_chapter, bib_ref)
    elif isinstance(bib_ref, BibArticle):
        bot.send_message(message.chat.id, '⚠️ Введите <b>название журнала</b>, в котором опубликовалась статья\n\n'\
                         'Например: <i>TUGBoat</i>\n\n',
                         parse_mode='HTML')
        bot.register_next_step_handler(message, bib_set_journal, bib_ref)

def bib_set_journal(message, bib_ref):
    bib_ref.journal = message.text

    bot.send_message(message.chat.id, '⚠️ Введите <b>общий номер выпуска</b> журнала (Volume.), в котором опубликовалась статья\n\n'\
                         'Например, Vol.59 No.4 означает, что это четвертый выпуск журнала за год, который имеет общий номер 59.\n\n',
                         parse_mode='HTML')
    bot.register_next_step_handler(message, bib_set_volume, bib_ref)

def bib_set_volume(message, bib_ref):
    bib_ref.volume = message.text

    bot.send_message(message.chat.id, '⚠️ Введите <b>номер выпуска</b> журнала за <b>год</b> (No.), в котором опубликовалась статья\n\n'\
                         'Например, Vol.59 No.4 означает, что это четвертый выпуск журнала за год, который имеет общий номер 59.\n\n',
                         parse_mode='HTML')
    bot.register_next_step_handler(message, bib_set_number, bib_ref)

def bib_set_number(message, bib_ref):
    bib_ref.number = message.text

    bot.send_message(message.chat.id, '⚠️ Введите <b>номера страниц</b>, на которые хотите сослаться\n\n'\
                         'Введите номера страниц через --, например <i>342--351</i>',
                         parse_mode='HTML')
    bot.register_next_step_handler(message, bib_set_pages, bib_ref)

def bib_set_pages(message, bib_ref):
    bib_ref.pages = message.text


    users["{0}".format(message.chat.id)].cites_[bib_ref.label] = bib_ref
    bib_add_article(users["{0}".format(message.chat.id)].bib_, bib_ref)

    bot.send_message(message.chat.id, '✅ Заполнили данные для журнальной статьи')
    bot.send_message(message.chat.id, 'Требуется ли еще добавить источник?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, bib_is_change)

def bib_set_chapter(message, bib_ref):
    bib_ref.chapter = message.text

    users["{0}".format(message.chat.id)].cites_[bib_ref.label] = bib_ref
    bib_add_inbook(users["{0}".format(message.chat.id)].bib_, bib_ref)

    bot.send_message(message.chat.id, '✅ Заполнили данные для главы из книги')
    bot.send_message(message.chat.id, 'Требуется ли еще добавить источник?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, bib_is_change)

def bib_set_series(message, bib_ref):
    if message.text != '0':
        bib_ref.series = message.text
    else:
        bib_ref.series = ''

    users["{0}".format(message.chat.id)].cites_[bib_ref.label] = bib_ref
    bib_add_book(users["{0}".format(message.chat.id)].bib_, bib_ref)

    bot.send_message(message.chat.id, '✅ Заполнили данные для книги')
    bot.send_message(message.chat.id, 'Требуется ли еще добавить источник?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, bib_is_change)

def bib_set_url(message, bib_ref):
    bib_ref.url = message.text

    bot.send_message(message.chat.id, 
                         '⚠️ Введите <b>Дату обращения к источнику</b>\n\n'\
                         'Введите дату в формате ГОД-МЕСЯЦ-ДЕНЬ\n\n'
                         'Например: <i>2013-05-16</i>', 
                         parse_mode='HTML')
        
    bot.register_next_step_handler(message, bib_set_urldate, bib_ref)

def bib_set_urldate(message, bib_ref):
    bib_ref.urldate = message.text

    users["{0}".format(message.chat.id)].cites_[bib_ref.label] = bib_ref
    bib_add_online(users["{0}".format(message.chat.id)].bib_, bib_ref)

    bot.send_message(message.chat.id, '✅ Заполнили данные для онлайн источника')
    bot.send_message(message.chat.id, 'Требуется ли еще добавить источник?', reply_markup=start_reply_kb())
    bot.register_next_step_handler(message, bib_is_change)

def bib_is_change(message):
    if message.text == 'Да':
        bot.send_message(message.chat.id, '...', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, '⚠️ Выберите, на какой тип какого источника хотите сослаться', 
                         reply_markup=bib_inline_kb())
    elif message.text == 'Нет':
        users["{0}".format(message.chat.id)].bib_.close()
        users["{0}".format(message.chat.id)].triggered_len = len(users["{0}".format(message.chat.id)].cites_)
        bot.send_message(message.chat.id, '.bib сгенерирован')

        bot.send_message(message.chat.id, '✅ Заполнили библиографию', reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, '✅ Переходим к заполнению основного документа')
        bot.send_message(message.chat.id, 'ℹ️ Теперь вам предстоит заполнить <b><i>Аннотацию</i></b>', parse_mode='HTML')
        bot.send_message(message.chat.id, 
                     '❔ <b><i>Подсказка</i></b>\n\n'\
                     'По смыслу, аннотация это очень краткий пересказ вашей работы, '\
                     'из которого релевантный человек должен быть способен понять, '\
                     'что вы делали идейно. Она обычно описывает постановку задачи '\
                     'и основные результаты работы в достаточно неформальной формулировке.\n\n'\
                     '<i>Объем до 2000 знаков</i>', parse_mode='HTML')
        set_annot(message)

    else:
        bot.send_message(message.chat.id, '❗️ Выберите ответ на кнопке')
        bot.send_message(message.chat.id, 'Требуется ли еще добавить источник?', reply_markup=start_reply_kb())
        bot.register_next_step_handler(message, bib_is_change)
    
def bot_add_bib(message):
    users["{0}".format(message.chat.id)].bib_ = make_bib_file(users["{0}".format(message.chat.id)].bib_path)
    bot.send_message(message.chat.id, 'ℹ️ Теперь вам предстоит заполнить <b><i>Библиографию</i></b>', parse_mode='HTML')

    bot.send_message(message.chat.id, '⚠️ Выберите, на какой тип какого источника хотите сослаться', reply_markup=bib_inline_kb())


bot.polling()
