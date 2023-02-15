import os

def build_tex(userInfo):
    print('build tex')

    os.mkdir('files/dir-' + userInfo.name)
    w_path = 'files/dir-' + userInfo.name + '/' + userInfo.name + '.tex'
    f = open(w_path, 'w')

    f.write(r"\documentclass[12pt, letterpaper, twoside]{article}" + "\n")
    f.write(r"\usepackage[utf8]{inputenc}" + "\n")
    f.write(r"\usepackage[russian]{babel}" + "\n")
    f.write("\n")

    f.write(r"\title{" + userInfo.title + "}" + "\n")
    f.write(r"\author{" + userInfo.firstName + " " + userInfo.secondName + "}" + "\n")

    
    f.write(r"\date{" + userInfo.date + "}" + "\n")

    f.write("\n")
    
    f.write(r"\begin{document}" + "\n")
    f.write("\n")

    f.write(r"\maketitle" + "\n")
    f.write("\n")

    f.write(userInfo.text + "\n")
    f.write("\n")

    f.write(r"\end{document}")

    f.close()


def compile_tex(name):
    print('compile tex')

    rel_path = 'files/dir-' + name + '/' + name + '.tex'
    path = os.getcwd() + '/' + rel_path
    os.chdir('files/dir-' + name)
    os.system("pdflatex " + path)
    os.chdir('../../')



class UserInfo:
    def __init__(self, 
                 firstName='FirstName',
                 secondName='SecondName',
                 date=r"\today",
                 title = "Title",
                 text=r"Sample \LaTeX{} document",
                 name="example"):
        self.firstName = firstName
        self.secondName = secondName
        self.date = date
        self.title = title
        self.text = text
        self.name = name

    # def __str__(self):
    #     return (f"{self.firstName} {self.secondName} {self.date} {self.title} {self.text} {self.name} {self.lang}")
