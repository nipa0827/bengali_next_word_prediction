# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 19:58:22 2019

@author: nipa
"""

from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, Activation, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku
import numpy as np
import keras
from time import time
from keras.models import load_model
import io
import json

with io.open("C:\\Users\\nipa\\Desktop\\FINAL\\plugin\\editor\\input.txt", 'r', encoding='utf-8', errors='ignore') as f:
    data = (f.read())

tokenizer = Tokenizer()

# maping_dict = json.load(open('dict.json', 'r', encoding="utf-8"))

corpus = data.split("\n")
# tokenization
tokenizer.fit_on_texts(corpus)

total_words = len(tokenizer.word_index) + 1
# create input sequences using list of tokens
input_sequences = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        n_gram_sequence = token_list[:i + 1]
        # print(n_gram_sequence)
        input_sequences.append(n_gram_sequence)

max_sequence_len = max([len(x) for x in input_sequences])
print(max_sequence_len)
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
predictors, label = input_sequences[:, :-1], input_sequences[:, -1]

label = ku.to_categorical(label, num_classes=total_words)


def create_model(predictors, label, max_sequence_len, total_words):
    logdir = "logs/{}".format(time())
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

    input_len = max_sequence_len - 1
    model = Sequential()
    model.add(Embedding(total_words, 20, input_length=input_len))
    model.add(LSTM(150))
    model.add(Dropout(0.1))
    model.add(Dense(total_words, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=["accuracy"])
    model.fit(predictors, label, epochs=50, verbose=1)
    return model

    '''
    logdir="logs/{}".format(time())
    tensorboard_callback = keras.callbacks.TensorBoard(log_dir=logdir)

    model = Sequential()
    model.add(Embedding(total_words, max_sequence_len-1, input_length=max_sequence_len-1))
    model.add(LSTM(512, return_sequences = True))
    #model.add(Dropout(0.15))
    #model.add(CuDNNLSTM(250, return_sequences = True))
    #model.add(Dropout(0.25))
    #model.add(Dense(int(total_words*1.5), activation='relu'))
    model.add(LSTM(512))
    #model.add(Dense(total_words, activation='softmax'))

    model.add(Dense(total_words, activation='softmax'))

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

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=0, mode='auto')

    model.fit(predictors, label, epochs=50, verbose=1,validation_split=0.2, callbacks=[earlystop, tensorboard_callback])
    print(model.summary())

    return model 
    '''


def generate_text(seed_text, next_words=1):
    # keras.backend.clear_session()
    wordList = []
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len - 1, padding='pre')
        predicted = model._make_predict_function()
        predicted = model.predict(token_list)
        # np.reshape(predicted, (1, 943))
        # print(predicted.reshape)
        topFiveWordIndex = predicted[0].argsort()[-5:][::-1]
        output_word = ""
        wordList = []

        for i in range(len(topFiveWordIndex)):
            testWord = topFiveWordIndex[i]
            for word, index in tokenizer.word_index.items():
                if index == testWord:
                    output_word = word
                    # print(output_word)
                    # output_word = maping_dict[output_word]
                    wordList.append(output_word)
                    break

    return wordList


# model = create_model(predictors, label, max_sequence_len, total_words)
# model.save("C:\\Users\\nipa\\Desktop\\model\\M2.h5")
model = load_model("C:\\Users\\nipa\\Desktop\\FINAL\\plugin\\editor\\M2.h5")

text = "বাংলাদেশের ক্রিকেটাররা কষ্ট বেশি দিতে। আমাদের "
text = text.split("। ")
print(text[len(text) - 1])
print(generate_text(text[len(text) - 1]))
print(generate_text("বাংলাদেশ সরকারের হিসাব ।"))
