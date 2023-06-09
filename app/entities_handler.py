from pylatex.utils import NoEscape

def only_quots(text):
    result = r''

    is_first_quot = True
    for i in range(len(text)):
        if (text[i] == '-'):
            if (i > 0 and i < len(text) and text[i - 1] == ' ' and text[i + 1] == ' '):
                result += '-'

        if (i < len(text) and text[i] == '_'):
            result += r'\_'

        if (text[i] == '"' and is_first_quot):
            is_first_quot = not is_first_quot
            result += "``"
        elif(text[i] == '"' and not is_first_quot):
            is_first_quot = not is_first_quot
            result += "''"
        elif text[i] != '_':
            result += text[i]
        

    return NoEscape(result)

def ent2latex(message):
    if message.entities == None:
        return message.text
    
    offsets = {}
    for entity in message.entities:
        offsets[entity.offset] = {'length': entity.length, 'type': entity.type}

    result = r''
    i = 0

    while i < len(message.text):
        if (i in offsets):
            has_new_line = False

            if (offsets[i]['type'] == 'bold'):
                    result += r'\textbf{'
            if (offsets[i]['type'] == 'italic'):
                result += r'\textit{'
            if (offsets[i]['type'] == 'underline'):
                result += r'\underline{'
            if (offsets[i]['type'] == 'strikethrough'):
                result += r'\sout{'

            for j in range(i, i + offsets[i]['length']):
                if (message.text[j] == '\n'):
                    if not has_new_line:
                        has_new_line = True
                        result += r'}'
                    result += r'\newline' + '\n'
                else:
                    result += message.text[j]

            if  not has_new_line:
                result += r'}'

            i += offsets[i]['length'] - 1
                        
        else:
            if (message.text[i] != '\n'):
                result += message.text[i]
            else:
                result += r'\newline' + '\n'

        i += 1

    print(result)
    return NoEscape(result)
