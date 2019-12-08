# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 14:58:35 2019

@author: nipa1
"""

import io
import re


def data_preprocesses():
    data = []
    letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,?:1‘234567890{}[]’১২৩৪৫৬৭৮৯০."
    with io.open('stop_word.txt', "r", encoding="utf-8") as file:
        filedata = file.read()

    data = filedata.split("\n")
    with io.open('C:\\Users\\nipa\\Desktop\\prothom_alo.txt', "r", encoding="utf-8") as file:
        filedata = file.read()
        # replace end of line with \n
        filedata = filedata.replace("। ", "\n")

    # remove all number
    filedata = ''.join(i for i in filedata if not i.isdigit())

    # remove bracket
    filedata = filedata.replace("(", "")
    filedata = filedata.replace(")", "")
    for word in data:
        filedata = filedata.replace(" " + word + " ", " ")

    filedata = re.sub(r'\n+', '\n', filedata).strip()

    filedata = [char for char in filedata if char not in letter]
    filedata = ''.join(filedata)

    # Write the file out again
    with io.open('C:\\Users\\nipa\\Desktop\\prothom_alo.txt', "w", encoding="utf-8") as file:
        file.write(filedata)


