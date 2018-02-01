#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO
# Automatische Berechnung der Zeilen/Spalten
# Verschiedene Sektionen? Refis, Sekratariat, SL?
# Rand und Titel

import os
import glob
import configparser

# Boundig Box für skalierte Bilder
bbox = "1000x1000"

# Farbe der Trenner
sepcolor = "gray94"

# in diesem Verzeichnis muss es zwei Unterverzeichnisse geben:
# pics    -> Bilder
# control -> Text-Dateien zur Steuerung
posterdir="/home/frank/Dokumente/011_Schule/AL_SLTeam/qg-intra.net/lehrerposter/personaldaten"
# Sectionen des Posters
#sections = {"Schulorganisation":"000_personal", "Lehrerinnen und Lehrer":"010_lehrer", "Referendarinnen und Referendare":"020_referendare"}
sections = {" ":"000_personal", "  ":"010_lehrer", "    ":"020_referendare"}
#sections = {"Lehrerinnen und Lehrer":"010_lehrer"}
# Name der Ausgabedatei
outpic = "/home/frank/lehrerposter.jpg"
# Manuelle Optionen für montage
montageopts = " -tile 10x -geometry 500x500+10+10 -pointsize 34"

picsdir = posterdir + "/pics"
scaleddir = posterdir + "/scaled"
controldir = posterdir + "/control"
headerpic = picsdir + "/_header.jpg"

parameters = configparser.ConfigParser()

## FIXME Check if Dirs exist

mps=""
for sec in sections.keys():
    print(sec)
    print(sections[sec])
    sectionfiles = os.path.join(controldir, sections[sec], "*.ini")
    print(sectionfiles)
    sectionoutfile = sections[sec] + ".jpg"
    print(sectionoutfile)
    
    for filename in sorted(glob.glob(sectionfiles)):
        parameters.read(filename)
        name = parameters.get("global","name")
        subjects = parameters.get("global","subjects")
        picture = parameters.get("global","picture")
                
        if picture == '""':
            picture = "dummy.jpg"
        #if subjects == '""':
        #    subjects = 'NN'

        name = name.replace('"','')
        subjects = subjects.replace('"','')
        picture = picture.replace('"','')
        picscaled = scaleddir + "/" + picture
        picture = picsdir + "/" + picture

        # Bild nach scaled skalieren
        resizecommand = "convert " + picture + " -resize " + bbox + " " + picscaled
        os.system(resizecommand)

        # Debug
        #print(name)
        #print(subjects)
        #print(picture)
        #print(picscaled)

        label = '"' + name + '  \\n ' + subjects + '"'
        #print(label)

        mps = mps + ' -label ' + label + ' ' + picscaled

    montagecommand =  "montage " + montageopts + mps + " " + sectionoutfile
    titlecommand = "convert " + sectionoutfile + ' -gravity North -background ' + sepcolor + ' -pointsize 70  -splice 0x87  -annotate +0+5 "' +  sec + '" ' + sectionoutfile

    # schreibe shellkommando
    commandfile = open("montage.sh",'wb')
    commandfile.write(montagecommand.encode('utf8'))
    commandfile.write(b"\n")
    commandfile.write(titlecommand.encode('utf8'))
    commandfile.close()

    os.system("chmod 755 ./montage.sh")
    os.system("./montage.sh")
    os.system("rm ./montage.sh")
    mps=""


seclist=headerpic + " "
for sec in sorted(sections.values()):
    seclist = seclist + sec +".jpg " 


mergecommand = "montage -tile 1x -geometry +0+30 " + seclist  + " lehrerposter.jpg"

# schreibe shellkommando
commandfile = open("merge.sh",'wb')
commandfile.write(mergecommand.encode('utf8'))
commandfile.write(b"\n")
commandfile.write(mergecommand.encode('utf8'))
commandfile.close()

os.system("chmod 755 ./merge.sh")
os.system("./merge.sh")
os.system("rm ./merge.sh")
