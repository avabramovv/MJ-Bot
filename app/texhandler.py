# Подключаем необходимые библиотеки
from pylatex import Document, Section, Subsection, Subsubsection, \
    Tabular, Math, TikZ, Axis, Command, Package, \
    Plot, Figure, SubFigure, Matrix, Alignat, Marker, \
    Label, Hyperref, Center, Foot, Itemize, Enumerate

from pylatex.table import Tabular, Table
from pylatex.basic import NewLine, LineBreak, NewPage, Environment
from pylatex.utils import italic, bold, NoEscape

from myhandlers import to_figures, myLabel, myRef

import random

import os

# sects = []

# \DeclareFieldFormat{labelnumberwidth}{#1.}

def set_tex_document(user_class):
    return Document(default_filepath=user_class.default_filepath_, 
                    documentclass='extarticle', 
                    document_options=[user_class.page_size_, user_class.font_size_],
               fontenc=['T1', 'T2A'], lmodern=False, textcomp=False,
               geometry_options=user_class.geometry_options_)

def add_tex_packages(document):
    document.packages.append(Package('babel', options=['english', 'russian']))
    document.packages.append(Package('float'))
    document.packages.append(Package('ulem', options='normalem'))
    document.packages.append(Package('amsmath'))
    document.packages.append(Package('amsthm'))
    document.packages.append(Package('amssymb'))
    document.packages.append(Package('fancyhdr'))
    document.packages.append(Package('setspace'))
    document.packages.append(Package('enumitem'))
    document.packages.append(Package('graphicx'))
    document.packages.append(Package('colortbl'))
    document.packages.append(Package('tikz'))
    document.packages.append(Package('pgf'))
    document.packages.append(Package('subcaption'))
    document.packages.append(Package('listings'))
    document.packages.append(Package('indentfirst'))
    document.packages.append(Package('biblatex', options={'backend': 'biber',
                                                 'style': 'numeric',
                                                 'maxbibnames': 99}))
    document.packages.append(Package('hyperref', options={'colorlinks': 'true',
                                                 'citecolor': 'blue',
                                                 'linkcolor': 'blue',
                                                 'bookmarks': 'false',
                                                 'hypertexnames': 'true',
                                                 'urlcolor': 'blue'}))
    document.packages.append(Package('indentfirst'))
    document.packages.append(Package('mathtools'))
    document.packages.append(Package('booktabs'))
    document.packages.append(Package('threeparttable', options='flushleft'))
    document.packages.append(Package('tablefootnote'))
    document.packages.append(Package('chngcntr'))

def add_tex_preamble(document):
    document.preamble.append(Command('addbibresource', NoEscape('refs.bib')))
    document.preamble.append(Command('counterwithin', extra_arguments='section', arguments='table'))
    document.preamble.append(Command('counterwithin', extra_arguments='section', arguments='figure'))
    document.preamble.append(Command('graphicspath', NoEscape(r'{graphics/}')))
    document.preamble.append(Command('makeatletter'))
    document.preamble.append(Command('makeatother'))
    document.preamble.append(Command('setlength', Command('parindent'), extra_arguments='1.25cm'))
    document.preamble.append(Command('renewcommand', Command('baselinestretch'), extra_arguments='1.5'))

    document.preamble.append(NoEscape(r'\newcommand{\bibref}[3]{\hyperlink{#1}{#2 (#3)}}'))
    document.preamble.append(NoEscape(r'\addto\captionsrussian{\def\refname{Список литературы (или источников)}}'))

    document.preamble.append(NoEscape(r'\renewcommand{\theenumi}{\arabic{enumi}}'))
    document.preamble.append(NoEscape(r'\renewcommand{\labelenumi}{\arabic{enumi}}'))
    document.preamble.append(NoEscape(r'\renewcommand{\theenumii}{.\arabic{enumii}}'))
    document.preamble.append(NoEscape(r'\renewcommand{\labelenumii}{\arabic{enumi}.\arabic{enumii}.}'))
    document.preamble.append(NoEscape(r'\renewcommand{\theenumiii}{.\arabic{enumiii}}'))
    document.preamble.append(NoEscape(r'\renewcommand{\labelenumiii}{\arabic{enumi}.\arabic{enumii}.\arabic{enumiii}.}'))

def add_tex_title(document, title_name):
    document.append(Command('input', NoEscape(f'{title_name}.tex')))

def add_tex_table_of_contents(document):
    document.append(NewPage())
    document.append(Command('setcounter', 'page', extra_arguments=2))
    to_figures(document, Command('hypersetup', {'linkcolor': 'black'}), Command('tableofcontents'))

def add_tex_annotation(document):
    document.append(NewPage())
    sect_ann = Section('Аннотация')
    sect_ann.numbering = False
    sect_ann.label = None
    document.append(sect_ann)

    sect_ann.append(Command('addcontentsline', arguments=['toc', 'section'], extra_arguments='Аннотация'))

    return sect_ann
    # \addcontentsline{toc}{section}{Аннотация}

def add_tex_key_words(document, key_words):
    sect_key = Section('Ключевые слова')
    sect_key.numbering = False
    sect_key.label = None
    document.append(sect_key)

    sect_key.append(NoEscape(key_words))

    document.append(Command('pagebreak'))

def add_tex_subsubsection(document, subsubsection_title):
    subsubsect = Subsubsection(document, subsubsection_title)
    document.append(subsubsect)

    subsubsect.label = None

def add_tex_subsection(document, subsection_title):
    subsect = Subsection(subsection_title)
    document.append(subsect)

    subsect.label = None
     
def add_tex_section(document, section_title):
    document.append(NewPage())
    sect = Section(section_title)
    document.append(sect)
    sect.label = None

def add_tex_literature(document):
    # Добавляем Список литературы
    document.append(NewPage())
    document.append(Command('printbibliography', options={'heading': 'bibintoc'}))

def tex_generate_tex(document):
    document.generate_tex()

def add_text(add_to, text):
    # Автоматически добавляет пробел в конец
    add_to.append(NoEscape(text) + NoEscape(' '))

def add_cite(add_to, cite_name):
    add_to.append(NoEscape(r'\cite{'f'{cite_name}''}'))
    # add_to.append(Command('cite', arguments=cite_name))

def add_space_before_text(add_to):
    add_to.append(NoEscape(chr(92) + ' '))

def add_list_itemize(add_to, items):
    itemize = Itemize()
    add_to.append(itemize)
    for item in items:
        itemize.add_item(item)

    return itemize

def add_list_enumerate(add_to, items):
    enum = Enumerate(options=NoEscape(r'label={\arabic{enumi}.}'))
    add_to.append(enum)
    
    for item in items:
        enum.add_item(item)

    return enum


def get_tabular_args(num_of_columns):
    result = '|'
    for i in range(0, num_of_columns):
        result += 'l|'

    print(result)
    return result

def add_table(add_to, caption, num_of_rows, num_of_columns, data):
    table = Table(position='htb!') 
    table.add_caption(caption)
    table.append(Command('footnotesize'))
    table.append(Command('centering'))

    add_to.append(table)

    tabular = Tabular(get_tabular_args(num_of_columns))
    table.append(tabular)

    tabular.add_hline()
    for i in range(0, num_of_rows):
        tabular.add_row(data[i])
        tabular.add_hline()

def add_image(add_to, img_name, caption, width_=0.7, label_name=''):
    pic = Figure(position='H')
    add_to.append(pic)
    pic.add_image(filename=img_name, width=NoEscape(r'{0}\textwidth'.format(width_)))
    pic.add_caption(NoEscape(caption))

    myLabel(pic, Marker(NoEscape(label_name), 'fig', False))

    # with sect_imgs.create(Figure(position='ht')) as pic:
    #     pic.add_image('example.png')
    #     pic.add_caption(NoEscape('''Пример графика. Тут должна быть подпись,
    #                          поясняющая что происходит на рисунке (краткая, но достаточная для понимания основной идеи графика).'''))
    #         # doc.append(Label(Marker(NoEscape('by_epochs'), 'fig')))
    #     myLabel(pic, Marker(NoEscape('by_epochs'), 'fig', False))

    return pic

def add_ref(add_to, type, ref_name):
    myRef(add_to, Marker(NoEscape(ref_name), type, False))
    
def add_paragraph(add_to):
    add_to.append(NewLine())

def add_url_link(add_to, link):
    add_to.append(Command('url', arguments=link))

def add_bottom_page_link(add_to, info):
    add_to.append(Command('footnote', arguments=info))

def add_math(add_to, eq):
    m = Math(escape=False, data=[eq], inline=False)
    add_to.append(m)

    return m

def bib_add_online(bib, bib_ref):
    bib.write('@online{'f"{bib_ref.label},\n")
    bib.write('author={'f"{bib_ref.author}"'},\n')
    # bib.write('author="{0}",\n'.format(author))
    bib.write('title="{0}",\n'.format(bib_ref.title))
    bib.write('url="{0}",\n'.format(bib_ref.url))
    bib.write('urldate={'f"{bib_ref.urldate}"'},\n')
    bib.write('}\n\n')

class BibOnline:
    def __init__(self):
        self.label = None
        self.author = None
        self.title = None
        self.url = None
        self.urldate = None

        self.is_triggered = False

def bib_add_inbook(bib, bib_ref):
    bib.write('@inbook{'f"{bib_ref.label},\n")
    bib.write('author={'f"{bib_ref.author}"'},\n')
    # bib.write('author="{0}",\n'.format(author))
    bib.write('title="{0}",\n'.format(bib_ref.title))
    bib.write('publisher="{0}",\n'.format(bib_ref.publisher))
    bib.write('year="{0}",\n'.format(bib_ref.year))
    bib.write('chapter="{0}",\n'.format(bib_ref.chapter))
    bib.write('}\n\n')

class BibInbook:
    def __init__(self):
        self.label = None
        self.author = None
        self.title = None
        self.publisher = None
        self.year = None
        self.chapter = None

        self.is_triggered = False

def bib_add_book(bib, bib_ref):
    bib.write('@book{'f"{bib_ref.label},\n")
    bib.write('author={'f"{bib_ref.author}"'},\n')
    # bib.write('author="{0}",\n'.format(author))
    bib.write('title="{0}",\n'.format(bib_ref.title))
    bib.write('publisher="{0}",\n'.format(bib_ref.publisher))
    bib.write('series="{0}",\n'.format(bib_ref.series))
    bib.write('year="{0}",\n'.format(bib_ref.year))
    bib.write('}\n\n')

class BibBook:
    def __init__(self):
        self.label = None
        self.author = None
        self.title = None
        self.publisher = None
        self.year = None
        self.series = None

        self.is_triggered = False

def bib_add_article(bib, bib_ref):
    bib.write('@article{'f"{bib_ref.label},\n")
    bib.write('author={'f"{bib_ref.author}"'},\n')
    # bib.write('author="{0}",\n'.format(author))
    bib.write('title="{0}",\n'.format(bib_ref.title))
    bib.write('journal="{0}",\n'.format(bib_ref.journal))
    bib.write('volume="{0}",\n'.format(bib_ref.volume))
    bib.write('number="{0}",\n'.format(bib_ref.number))
    bib.write('pages="{0}",\n'.format(bib_ref.pages))
    bib.write('year="{0}",\n'.format(bib_ref.year))
    bib.write('}\n\n')

class BibArticle:
    def __init__(self):
        self.label = None
        self.author = None
        self.title = None
        self.journal = None
        self.volume = None
        self.number = None
        self.pages = None
        self.year = None

        self.is_triggered = False



def make_bib_file(name):
    bib_file = open(rf'{name}.bib', 'w')

    return bib_file

    # @article for journal articles (see example above).
    # @inproceedings for conference proceeding articles:
    # @book for books (see examples above).
    # @phdthesis, @masterthesis for dissertations and theses
    # @inbook is for a book chapter where the entire book was written by the same author(s): the chapter of interest is identified by a chapter number:
    # @incollection is for a contributed chapter in a book,
    #  so would have its own author and title. The actual title of the entire book is given in the booktitle field;
    #  it is likely that an editor field will also be present:

def set_title(title_name='title', type='', topic='', student='', group='', assistant='', post='', work=''):
    title = open(rf'{title_name}.tex', 'w')
    title.write(
    r'''\begin{titlepage}
    \newpage
    
    {\setstretch{1.0}
    \begin{center}
    ПРАВИТЕЛЬСТВО РОССИЙСКОЙ ФЕДЕРАЦИИ\\
    ФГАОУ ВО НАЦИОНАЛЬНЫЙ ИССЛЕДОВАТЕЛЬСКИЙ УНИВЕРСИТЕТ\\
    «ВЫСШАЯ ШКОЛА ЭКОНОМИКИ»
    \\
    \bigskip
    Факультет компьютерных наук\\
    Образовательная программа «Прикладная математика и информатика»
    \end{center}
    }
    
    \vspace{2em}
    УДК ХХХХХ
    \vspace{5em}
    
    \begin{center}''')

    title.write('\n')
    title.write(r'{\bf Отчет о')
    title.write(type)
    title.write(r' проекте на тему:}\\')
    title.write('\n')
    title.write(r'{\bf ')
    title.write(topic)
    title.write(r'}')
    title.write(r'''
    \end{center}
    
    \vspace{2em}
    
    {\bf Выполнил: \vspace{2mm}}
    
    {\setstretch{1.0}
    \begin{tabular}{l@{\hskip 1.5cm}c@{\hskip 1.5cm}c}''')
    title.write('\n')
    title.write('студент группы БПМИ')
    title.write(group)
    title.write(r' & & \\')
    title.write('\n')
    title.write(student)
    title.write(r' & \rule{3.5cm}{0.15mm}  &  \rule{3.5cm}{0.15mm} \vspace{-2mm} \\')
    title.write('\n')
    title.write(
    r'''
     & \tiny{(подпись)}  & \tiny{(дата)} \\
    \end{tabular}}
    
    \vspace{1em}
    {\bf Принял руководитель проекта: \vspace{2mm}}
    
    {\setstretch{1.0}
    \begin{tabular}{l@{\hskip 1.5cm}l}
    ''')
    title.write('\n')
    title.write(assistant + r'\\' + '\n')
    title.write(post + r'\\' + '\n')
    title.write(work + r' \vspace{10mm}\\' + '\n')
    title.write(
    r'''
    \rule{4cm}{0.15mm}  &  \rule{4cm}{0.15mm} \vspace{-2mm}\\
    {\hskip 1.5cm}\tiny{(подпись)} & {\hskip 1.5cm}\tiny{(дата)} \\
    \end{tabular}}
    
    \vspace{\fill}
    
    \begin{center}
    Москва 2023
    \end{center}
    
    \end{titlepage}
    '''
    )

    title.close()

class UserInfo2:
    def __init__(self,
                 default_filepath='your_file',
                 page_size='a4paper',
                 font_size='12pt',
                 geometry_options={
                   'left': '2.5cm',
                   'right': '1.0cm',
                   'top': '2.0cm',
                   'bottom': '2.0cm'},
                 title_name='your_title',
                 type='б исследовательском',
                 topic='Ваша тема',
                 student='Иванов Иван Иванович',
                 group='2110',
                 assistant='Петров Петр Петрович',
                 post='Научный сотрудник',
                 work='Факультета компьютерных наук НИУ ВШЭ',
                 chat_id = '123',
                 path='',
                 graphics_path='',
                 bib_path = ''):
        
        self.add_curr = None
        self.default_filepath_ = default_filepath
        self.page_size_ = page_size
        self.font_size_ = font_size
        self.geometry_options_ = geometry_options

        self.title_name_= title_name
        self.type_= type
        self.topic_= topic
        self.student_= student
        self.group_= group
        self.assistant_= assistant
        self.post_= post
        self.work_= work

        self.document_ = Document('')

        self.annotation_ = Section('')
        self.key_words_ = Section('')
        self.sections_ = []

        self.bib_ = 'refs.bib'

        self.bib_refs = []

        self.next = None

        self.cites_ = {}
        self.triggered_len = 0

        self.items = []

        self.table_data = []

        self.chat_id = chat_id
        self.path = path
        self.graphics_path = graphics_path
        self.bib_path = bib_path

class UserInfo:
    # def parse_text(self):
    #     self.text = self.parser.get_parsed(self.text)

    def __init__(self, 
                 firstName='FirstName',
                 secondName='SecondName',
                 date=r"\today",
                 title = "Title",
                 text=r"Sample \LaTeX{} document",
                 doc_name="example"):
        self.firstName = firstName
        self.secondName = secondName
        self.date = date
        self.title = title
        # self.parser = MyHTMLParser()
        self.text = text
        self.doc_name = doc_name

        self.doc = Document()
        self.sects = []