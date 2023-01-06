import numpy as np
import pandas as pd
import emoji as emoji
from keras.utils import to_categorical
from keras.layers import LSTM, Dropout, Dense, Activation
from keras.models import Sequential
from keras.models import model_from_json


def return_emoji(sentence):
    train = pd.read_csv("train_emoji.csv", header=None)
    train.drop(labels=[2, 3], axis=1, inplace=True)
    test = pd.read_csv("test_emoji.csv", header=None)

    emoji_dictionary = {"0": "\u2764\uFE0F",  # :heart: prints a black instead of red heart depending on the font
                        "1": ":baseball:",
                        "2": ":beaming_face_with_smiling_eyes:",
                        "3": ":downcast_face_with_sweat:",
                        "4": ":fork_and_knife:",
                        "5": ":panda:",
                        "6": ":automobile:"
                        }

    emoji.emojize(":automobile:")

    data = train.values
    XT = train[0]
    Xt = test[0]

    YT = to_categorical(train[1])
    Yt = to_categorical(test[1])

    embeddings = {}
    with open(r'glove.6B.50d.txt', encoding='utf-8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coeffs = np.asarray(values[1:], dtype='float32')

            # print(word)
            # print(coeffs)
            embeddings[word] = coeffs

    def getOutputEmbeddings(X):
        embedding_matrix_output = np.zeros((X.shape[0], 10, 50))
        for ix in range(X.shape[0]):
            X[ix] = X[ix].split()
            for jx in range(len(X[ix])):
                embedding_matrix_output[ix][jx] = embeddings[X[ix][jx].lower()]

        return embedding_matrix_output

    emb_XT = getOutputEmbeddings(XT)
    emb_Xt = getOutputEmbeddings(Xt)

    model = Sequential()
    model.add(LSTM(64, input_shape=(10, 50), return_sequences=True))
    model.add(Dropout(0.4))
    model.add(LSTM(64, input_shape=(10, 50)))
    model.add(Dropout(0.3))
    model.add(Dense(7))
    model.add(Activation('softmax'))

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
    model.fit(emb_XT, YT, batch_size=32, epochs=100, shuffle=True, validation_split=0.1)

    model.evaluate(emb_Xt, Yt)
    pred = np.argmax(model.predict(emb_Xt), axis=1)

    with open("model.json", "w") as file:
        file.write(model.to_json())
    model.save_weights("model.h5")

    with open("model.json", "r") as file:
        model = model_from_json(file.read())
    model.load_weights("model.h5")

    test_str = sentence
    X = pd.Series([test_str])
    emb_X = getOutputEmbeddings(X)
    p = np.argmax(model.predict(emb_X), axis=1)
    # print(' '.join(X[0]))
    ret_emoji = emoji.emojize(emoji_dictionary[str(p[0])])
    return ret_emoji
