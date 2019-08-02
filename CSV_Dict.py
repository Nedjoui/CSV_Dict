# Nedjoui
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    try:
        from PyQt5.QtWidgets import QLineEdit, QApplication,\
            QWidget, QGridLayout, QLayout, QPushButton, QTextEdit
    except:
        from PySide2.QtWidgets import QLineEdit, QApplication,\
            QWidget, QGridLayout, QLayout, QPushButton, QTextEdit
except:
    print("You have to install PyQt5 or PySide2")
     
import glob
import json
import re
import os
import sys

try:
    with open("lang.json") as language:
        lang_txt=json.load(language)
except:
    pass

try:
    with open("setting.json") as setting:
        style=json.load(setting)
except:
    pass

# to translate from English (lang.json) if there is No translation, keep English words.
def lang(word): 
    try:
        if len((lang_txt["English"]).replace(" ",""))== 0:
            return word
        elif len((lang_txt[word]).replace(" ",""))== 0:
            return word
        else:
            return lang_txt[word]
    except:
        return word

app=QApplication(["CSV_Dict"])
win=QWidget()

# buttons and fields ------------------------
Tran=QPushButton(lang("Translate"))
c1=QPushButton(lang("clear input"))
c2=QPushButton(lang("clear output"))
about_the_dict=QPushButton(lang("About the Dict"))
a=QLineEdit()
txt=QTextEdit()
result=QLineEdit()
number_of_result=QLineEdit()
result.setReadOnly(True)
txt.setReadOnly(False)

## placeholder--------------------------
a.setPlaceholderText(lang("Enter a word or sentence to translate"))
txt.setPlaceholderText(lang('''You will see the translate here.You can copy the hole text or modify it then copy.'''))
number_of_result.setPlaceholderText(lang("Set the number of results"))
result.setPlaceholderText(lang("Number of results"))


box= QGridLayout()
box.addWidget(Tran, 0, 0)
box.addWidget(c1, 0, 1)
box.addWidget(c2, 0, 2)
box.addWidget(about_the_dict, 0, 3)
box.addWidget(a, 1, 0, 1, 4)
box.addWidget(txt, 2, 0, 2,4)
box.addWidget(result, 4,0)
box.addWidget(number_of_result, 4,3)
win.setLayout(box)

a.setFocus()

##Styles from setting.json file ------------------------------------------
try:
    win.setStyleSheet(style["framcolor"])
    a.setStyleSheet(style["input"] ) 
    txt.setStyleSheet(style["output"] )
    Tran.setStyleSheet(style["translate"] )
    c1.setStyleSheet(style["clear input"] )
    c2.setStyleSheet(style["clear output"] )
    about_the_dict.setStyleSheet(style["about the dict"] )
    result.setStyleSheet(style["Number of results"] )
    number_of_result.setStyleSheet(style["Set the number of results"] )
except:
    pass

def Translate():
    entrys_list=[]
    entry=0
    txt.clear()
    result.clear()
    # to specify the number of results
    try:
        number_r=int(number_of_result.text())
    except:
        try:
            number_r=style["number_of_result"]
        except:        
            number_r=25
    #------------------------------------------------
    try:
        try: # if there is a setting.json file -------------------
            for path in style["paths"]:
                for csv_f in glob.glob(path + "*.csv"):
                    with open(csv_f) as f:
                        lines=f.readlines()
                        for line in lines:
                            the_line=re.sub("[ًٌٍَُِّْـ-]", "", line).upper()
                            the_text=re.sub("[ًٌٍَُِّْـ-]", "", a.text()).upper()
                            if a.text() != "" and the_text in the_line:
                                if line in entrys_list:
                                    pass
                                else:
                                    entry=entry+1                          
                                    txt.append(f"<p style='{style['break'][0]}'"  + ">" + str(entry) + f" :{style['break'][1]*style['break'][2]}</p>")
                                    index_semicolon= line.index(";")
                                    txt.append(f'''<p style="{style['line1']}">''' + line[:index_semicolon] + "</p>")
                                    txt.append(f'''<p style="{style['line2']}">'''  + line[index_semicolon+1:] + "</p>")
                                    
                            if entry==number_r:
                                break
    
        except: # if there is No setting.json file -----------------
            for path in ["csv/", "csv_files/", ""]:
                for csv_f in glob.glob(path + "*.csv"):
                    with open(csv_f) as f:
                        lines=f.readlines()
                        for line in lines:       
                            the_line=re.sub("[ًٌٍَُِّْـ-]", "", line).upper()
                            the_text=re.sub("[ًٌٍَُِّْـ-]", "", a.text()).upper()
                            if a.text() != "" and the_text in the_line:
                                if line in entrys_list:
                                    pass
                                else:
                                    entry=entry+1
                                    txt.append(f"{entry} :---------------------")
                                    index_semicolon= line.index(";")
                                    txt.append(line[:index_semicolon])
                                    txt.append(line[index_semicolon+1:])
                                    entrys_list.append(line)
                                                                   
                            if entry==number_r:
                                break
                                        
                
        if entry==0:
                    txt.append(lang("So sorry, there is no results"))
        else:
                result.setText(lang("Number of results") + ": " + str(entry))
        
    except: 
        txt.append(lang("There is No CSV file"))
        txt.append(lang("open setting.json file go to the first entry 'paths' then add your paths to CSV files"))

def about():# connect with about the Dict button
    if lang('English').upper().replace(" ", "")==str("Arabic").upper() or\
        lang('English').upper().replace(" ", "")==str('Arab').upper() or\
            lang('English').replace(" ", "")==str('العربية') or\
                lang('English').replace(" ", "")==str('عربية') :
        txt.setText('''
    السلام عليكم
- شكرا جزيلا لاستعمالك قاموس CSV_Dict
- هذا القاموس يقرأ ملفات csv فقط، المفصولة بفاصلة منقوطة ";"
- يمكنك وضع الملفات بإمتداد csv في مجلد بهذين الاسمين "csv" ,"csv_files" أو مباشرة بجانب الملف CSV_Dict.
- يمكنك إدراج مسارات أخرى لملفات بإمتداد csv وذلك بفتح الملف setting.json ثم إدراج المسارات في القائمة paths. 
- يمكنك البحث عن كلمة أو جملة لكلا اللغتين مع العلم أن إدراج مسافة قبل أو بعد الكلمة قد تغير النتائج المعروضة.
- لتغيير الألون، حجم الخط ، الخلفية......إلخ، افتح ملف setting.json ثم غير كما تشاء. 
- لتغيير اللغة إلى العربية افتح ملف lang.json وأمام كلمة English أكتب:عرببة أو العرببة أو Arab أو Arabic وللإنجليزية اترك المزدوجين فارغين. 
- لمعلومات أكثر اقرأ الملف المرفق إقرأني. 

     أخوكم: Nedjoui
        ''')
    else:
        txt.setText('''
    Assalamu Alykom,
- Thank you for using CSV_Dict.
- This Dictionary read csv files, with semicolon ";" delimiter "separated".
- you can put csv files in folders with this names "csv" or "csv_files", or put them in the same folder with "CSV_Dict" file.
- you can specify other paths for "csv files" by opening setting.json file then add your paths.
- you can search for a word or a sentence (both languages), when you put space before or after the word the rusalts maybe it will change.
- if you want to change colors, font-size, background.........etc, open setting.json file and change whatever you want.
- you can change the language from "lang.json".
- for more info read "readme" file.

--------- by: Nedjoui ------------------
        ''')

## connect buttons with their Functions -----------------------------            
Tran.clicked.connect(Translate)
a.editingFinished.connect(Translate)
c1.clicked.connect(a.clear)
c2.clicked.connect(txt.clear)
about_the_dict.clicked.connect(about)

win.show()
#app.exec_()
sys.exit(app.exec_())

