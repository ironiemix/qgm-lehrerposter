#!/usr/bin/python
# -*- coding: utf-8 -*-

# this is a q'n'd hack to create a first set of 
# control files out of one csv-file

file = open("kollegium","r")
for line in file:
    line=line.rstrip()
    fields = line.split(";")
    outfile=fields[2].lower() + ".txt"
    out = open(outfile,"w")
    out.write("name=\"" + fields[1] + " " + fields[0] + "\"")
    out.write("\n")
    out.write("subjects=\"\"\n")
    out.write("picture=\"\"")
    out.close()
file.close()
