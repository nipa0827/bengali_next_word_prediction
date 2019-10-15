# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 18:52:53 2019

@author: nipa
"""
import io
import re
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import keras.utils as ku
from keras.models import load_model
from keras.layers import Embedding, LSTM, Dense
from keras.callbacks import EarlyStopping
from keras.models import Sequential
from time import time
import keras
from keras.models import Model

def data_preprocess():
    data = []
    letter = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,?:1‘234567890{}[]’১২৩৪৫৬৭৮৯০."
    with io.open('stop_word.txt', "r", encoding="utf-8") as file:
        filedata = file.read()

    data = filedata.split("\n")
    with io.open('C:\\Users\\nipa\\Desktop\\word.txt', "r", encoding="utf-8") as file:
        filedata = file.read()
        #replace end of line with \n
        filedata = filedata.replace("। ", "\n")
  
    #remove all number
    filedata = ''.join(i for i in filedata if not i.isdigit())
  
    #remove bracket
    filedata = filedata.replace("(", "")
    filedata = filedata.replace(")", "")
    for word in data:
        filedata = filedata.replace(" "+word+" ", " ")
    
    
    filedata = re.sub(r'\n+', '\n', filedata).strip()
  
    filedata = [char for char in filedata if char not in letter]
    filedata = ''.join(filedata)

    # Write the file out again
    with io.open('C:\\Users\\nipa\\Desktop\\word.txt', "w", encoding="utf-8") as file:
        file.write(filedata)
        

    
def createNumpyArray(sequence):
    sequence = np.pad(sequence, (max_sequence_len-len(sequence), 0), 'constant')
    result = sequence
    return result

def createPredictor(res):
    #length = max_sequence_len-len(res)
    res = np.pad(res, (max_sequence_len-len(res), 0), 'constant')
    result = res
    return result

def createLabel(sequence, length):
    return sequence[length]


with io.open("C:\\Users\\nipa\\Desktop\\word.txt",'r',encoding = 'utf-8') as f:
  data = (f.read())
  
  

tokenizer = Tokenizer()



	# basic cleanup
corpus = data.split("\n")

	# tokenization	
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1
print(total_words)

	# create input sequences using list of tokens
input_sequences = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i+1]
        input_sequences.append(n_gram_sequence)

	# pad sequences 
    
#print(input_sequences)
max_sequence_len = max([len(x) for x in input_sequences])
    
#max_sequence_len = 50

print("Maximum sequence len : " , max_sequence_len)

maxList = max(input_sequences, key = len) 
final_sequence = createNumpyArray(np.array(input_sequences[0]))
#print(maxList)

last_element = np.array(maxList[max_sequence_len-1])

for i in range(len(input_sequences)):
    sequence = np.array(input_sequences[i])
    arr = np.array(createNumpyArray(sequence))
    final_sequence = np.array(np.append(final_sequence, arr, axis = 0))
    
final_sequence = np.array(final_sequence)

final_sequence = final_sequence.reshape(len(input_sequences)+1, max_sequence_len)
print(final_sequence)
maxList = np.delete(maxList, max_sequence_len-1)
predictor = np.array(maxList)
label = np.array(last_element)

max_sequence_len = max_sequence_len - 1


for i in range(len(final_sequence)):
        newSequence = np.array(final_sequence[i])
        newArray = np.array(newSequence[0:max_sequence_len])
        label = np.append(label, np.array(newSequence[len(newSequence)-1]))
        predictor =np.array(np.append(predictor, np.array(newArray)))
       
predictor = predictor.reshape(len(input_sequences)+2, max_sequence_len)
label = ku.to_categorical(label, num_classes=total_words)



def create_model(predictors, label, max_sequence_len, total_words):
    logdir="logs/{}".format(time())
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
    
    
    model = Sequential()
    model.add(Embedding(total_words, max_sequence_len, input_length=max_sequence_len))
    model.add(LSTM(150, return_sequences = True))
    #model.add(Dropout(0.25))
    #model.add(CuDNNLSTM(250, return_sequences = True))
    #model.add(Dropout(0.25))
    model.add(LSTM(150))
    #model.add(Dense(total_words, activation='softmax'))
    #model.add(Dense(int(total_words*1.5), activation='relu'))
    model.add(Dense(total_words, activation='softmax'))
    
    '''
    input_layer = Input(shape = (max_sequence_len-1,))
    embed = Embedding(total_words, 20, input_length=max_sequence_len-1)(input_layer)
    print(embed.shape)
    lstm_1 = CuDNNLSTM(150, return_sequences = True)(embed)
    drop_out_1 = Dropout(0.25)(lstm_1)
    lstm_2 = CuDNNLSTM(200) (drop_out_1)
    #dense_1 = Dense(total_words, activation='relu')(lstm_2)
    #dense_2 = Dense(int(total_words*1.5), activation='relu')(dense_1)
    dense_3 = Dense(total_words, activation='softmax')(lstm_2)
    model = Model(inputs = input_layer, outputs = dense_3)
    '''
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=50, verbose=0, mode='auto')
    print(total_words)
    model.fit(predictors, label, epochs=100, verbose=1,validation_split=0.2, callbacks=[earlystop, tensorboard_callback])
    print(model.summary())
    
    return model 

def generate_text(seed_text, next_words, max_sequence_len, model):
    #keras.backend.clear_session()
    tokenizer = Tokenizer()
    wordList = []
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len, padding= 'pre')
        predicted = model._make_predict_function()
        predicted = model.predict(token_list)
        #np.reshape(predicted, (1, 943))
        #print(predicted.reshape)
        
        topFiveWordIndex = predicted[0].argsort()[-5:][::-1]
        print(topFiveWordIndex)
        output_word = ""
        wordList = []
        
        for i in range(len(topFiveWordIndex)):
            testWord = topFiveWordIndex[i]
            for word, index in tokenizer.word_index.items():
                if index == testWord:
                    output_word = word
                    print(output_word)
                    wordList.append(output_word)
                    break
		
            
    return wordList


data = data_preprocess()
#model = create_model(predictors, label, max_sequence_len, total_words)
#model.save("M1.h5")

#del model
print(label)
model = load_model("M1.h5")
print(generate_text("মাহমুদ হাসান " ,  1,  max_sequence_len, model))
