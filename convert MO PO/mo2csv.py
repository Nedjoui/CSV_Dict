import polib # pip install polib

#to include Arbic and exclude Persia we need these letters
# نحتاج هذه الحروف لإدراج الترجمات العربية واستبعاد بعض الترجمات الفارسية

l_a="ضصثقفغعهخحجدطكمنتالبيسشئءؤرىذأإةوزظ" # Arabic letters
l_p="گپژچ"   # some Persian letters not like Arabic letters

x=0
with open("mo_file.txt") as t:
	line=t.readlines()
	for path in line:
		try:
			mo = polib.mofile(path.strip())

			for entry in mo.translated_entries():
				if entry.msgstr:
					with open("mo.csv", "+a") as f:
						for letter in l_a:
							if letter in entry.msgstr and letter not in l_p:
								line= '''{} ; {}'''.format(entry.msgid.replace(";",",").replace("\n", " "), entry.msgstr.replace(";" , ",").replace("\n", " "))
								print (line , file=f)
								break
		except:
			  print(path)

