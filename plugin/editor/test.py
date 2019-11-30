# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 16:53:09 2019

@author: nipa
"""

import io
from model_prediction import generate_text
import csv

with io.open("C:\\Users\\nipa\\Desktop\\spl\\bengali_next_word_prediction\\plugin\\editor\\word.txt",'r',encoding = 'utf-8', errors='ignore') as f:
  data = (f.read())

def test_data_generation(num_of_words):
    corpus = data.split("\n")
    
    test_data = []
    actual_result = []
    
    for i in range(len(corpus)):
        line = corpus[i]
        line = line.split()
        
        if len(line) != 0:
            actual_result.append(line[num_of_words])
            line = line[0:num_of_words]
        
            test_data.append(' '.join(map(str, line)))
    
    return test_data, actual_result
    
test_data, actual_result = test_data_generation(1)


with io.open("C:\\Users\\nipa\\Desktop\\spl\\bengali_next_word_prediction\\plugin\\editor\\given_one_word_test.txt",'a',encoding = 'utf-8', errors='ignore') as f:
    for i in range(len(test_data)):
        result = generate_text(test_data[i])
        
        print(result)
        print(actual_result[i])
        
        if(actual_result[i] in result):
            result = 1
        else:
            result = 0

        line = test_data[i] + " , "  + actual_result[i]+ " , " + str(result) + "\n"
        f.write(line)
        
f.close()