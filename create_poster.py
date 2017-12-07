#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO
# Automatische Berechnung der Zeilen/Spalten
# Verschiedene Sektionen? Refis, Sekratariat, SL?
# Rand und Titel

import os
import glob
import time
import configparser
from subprocess import call

# in diesem Verzeichnis muss es zwei Unterverzeichnisse geben:
# pics    -> Bilder
# control -> Text-Dateien zur Steuerung
posterdir="/home/frank/Downloads/kftmp/lehrerposter"
outpic = "/home/frank/lehrerposter.jpg"
montageopts = " -tile 9x "

picsdir = posterdir + "/pics"
controldir = posterdir + "/control"
controlfiles = controldir + "/*.ini"

parameters = configparser.ConfigParser()

## FIXME Check if Dirs exist

mps=""
for filename in sorted(glob.glob(controlfiles)):
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

montagecommand =  "montage " + montageopts + mps + " " + outpic

# schreibe shellkommando
commandfile = open("montage.sh",'w')
commandfile.write(montagecommand.encode('utf8'))
commandfile.close()

os.system("chmod 755 ./montage.sh")
os.system("./montage.sh")
os.system("rm ./montage.sh")
