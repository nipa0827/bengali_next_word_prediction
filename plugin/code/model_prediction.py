# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:58:22 2019

@author: nipa
"""

from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku
import numpy as np
import keras
from time import time
from keras.models import load_model

with open("/home/iit/Downloads/SPL/data/word.txt",'r',encoding = 'utf-8', errors='ignore') as f:
  data = (f.read())	

tokenizer = Tokenizer()
def dataset_preparation(data):

	# basic cleanup
	corpus = data.lower().split("\n")

	# tokenization	
	tokenizer.fit_on_texts(corpus)
	total_words = len(tokenizer.word_index) + 1

	# create input sequences using list of tokens
	input_sequences = []
	for line in corpus:
		token_list = tokenizer.texts_to_sequences([line])[0]
		for i in range(1, len(token_list)):
			n_gram_sequence = token_list[:i+1]
			input_sequences.append(n_gram_sequence)

	# pad sequences 
	max_sequence_len = max([len(x) for x in input_sequences])
	input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))

	# create predictors and label
	predictors, label = input_sequences[:,:-1],input_sequences[:,-1]
	label = ku.to_categorical(label, num_classes=total_words)

	return predictors, label, max_sequence_len, total_words

def create_model(predictors, label, max_sequence_len, total_words):
	
    logdir="logs/{}".format(time())
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)
    
    model = Sequential()
    model.add(Embedding(total_words, 20, input_length=max_sequence_len-1))
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
    model.fit(predictors, label, epochs=100, verbose=1,validation_split=0.2, callbacks=[earlystop, tensorboard_callback])
    print(model.summary())
    
    return model 


def generate_text(seed_text, next_words, max_sequence_len):
    wordList = []
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding= 'pre')
        predicted = model.predict_proba(token_list, verbose=0)
        print(predicted.shape)
        topFiveWordIndex = predicted[0].argsort()[-5:][::-1]
        output_word = ""
        wordList = []
        
        for i in range(len(topFiveWordIndex)):
            testWord = topFiveWordIndex[i]
            for word, index in tokenizer.word_index.items():
                if index == testWord:
                    output_word = word
                    wordList.append(output_word)
                    break
		
            
    return wordList

predictors, label, max_sequence_len, total_words = dataset_preparation(data)
model = load_model("/home/iit/Downloads/SPL/model/M2.h5")
#print(generate_text("বাংলাদেশ সরকারের হিসাব ।", 1,  max_sequence_len))
 
