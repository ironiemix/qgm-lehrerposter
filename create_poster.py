#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO
# Automatische Berechnung der Zeilen/Spalten
# Verschiedene Sektionen? Refis, Sekratariat, SL?
# Rand und Titel

import os
import glob
import configparser

# in diesem Verzeichnis muss es zwei Unterverzeichnisse geben:
# pics    -> Bilder
# control -> Text-Dateien zur Steuerung
posterdir="/home/frank/Downloads/kftmp/lehrerposter"
# Sectionen des Posters
sections = {"Schulorganisation":"000_personal", "Lehrerinnen und Lehrer":"010_lehrer", "Referendarinnen und Referendare":"020_referendare"}
# Name der Ausgabedatei
outpic = "/home/frank/lehrerposter.jpg"
# Manuelle Optionen für montage
montageopts = " -tile 9x -geometry 500x500+10+10 -pointsize 34"

picsdir = posterdir + "/pics"
controldir = posterdir + "/control"

parameters = configparser.ConfigParser()

## FIXME Check if Dirs exist

mps=""
for sec in sections.iterkeys():
	print sec
	print(sections[sec])
	sectionfiles = os.path.join(controldir, sections[sec], "*.ini")
	print(sectionfiles)
	sectionoutfile = sections[sec] + ".jpg"


	for filename in sorted(glob.glob(sectionfiles)):
		parameters.read(filename)
		name = parameters.get("global","name")
		subjects = parameters.get("global","subjects")
		picture = parameters.get("global","picture")
		
		if picture == '""':
			picture = "dummy.jpg"
		if subjects == '""':
			subjects = 'NN'

		name = name.replace('"','')
		subjects = subjects.replace('"','')
		picture = picsdir + "/" + picture
		#print(name)
		#print(subjects)
		#print(picture)
		
		label = '"' + name + '  \\n ' + subjects + '"'
		#print(label)

		mps = mps + ' -label ' + label + ' ' + picture

	montagecommand =  "montage " + montageopts + mps + " " + sectionoutfile
	titlecommand = "convert " + sectionoutfile + ' -gravity North -background Plum -pointsize 70  -splice 0x87  -annotate +0+5 "' +  sec + '" ' + sectionoutfile

	# schreibe shellkommando
	commandfile = open("montage.sh",'w')
	commandfile.write(montagecommand.encode('utf8'))
	commandfile.write("\n")
	commandfile.write(titlecommand.encode('utf8'))
	commandfile.close()

	os.system("chmod 755 ./montage.sh")
	os.system("./montage.sh")
	os.system("rm ./montage.sh")
	mps=""

seclist=""
for sec in sorted(sections.itervalues()):
 	seclist = seclist + sec +".jpg " 
        print(sec)

mergecommand = "montage -tile 1x -geometry +0+30 " + seclist  + " lehrerposter.jpg"

# schreibe shellkommando
commandfile = open("merge.sh",'w')
commandfile.write(mergecommand.encode('utf8'))
commandfile.write("\n")
commandfile.write(mergecommand.encode('utf8'))
commandfile.close()

os.system("chmod 755 ./merge.sh")
os.system("./merge.sh")
os.system("rm ./merge.sh")
