import numpy as np
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error

def main():
    # [dispensals in a day, ml per dispensal, dispenser capacity(ml)]
    train_x = np.array([[123, 1, 1000], [89, 1, 1000], [46, 1, 1000], [66, 1, 1000], [76, 1, 1000], [34, 1, 1000], [12, 1, 1000]], dtype=float)
    test_x = np.array([[100, 1, 1000], [44, 1, 1000], [27, 1, 1000]], dtype=float)
    # [days until dispenser fluid ran out]
    train_y = np.array([[9], [13], [26], [19], [17], [33], [47]], dtype=float)
    test_y = np.array([[7], [21], [35]], dtype=float)

    # normalize
    scaler = MinMaxScaler(feature_range=(0, 1))
    train_x = scaler.fit_transform(train_x)
    train_y = scaler.fit_transform(train_y)
    test_x = scaler.fit_transform(test_x)
    test_y = scaler.fit_transform(test_y)

    train_y = np.squeeze(train_y)
    test_y = np.squeeze(test_y)

    #reshape to [samples, time steps, features]
    train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))
    test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))

    # create LSTM and train model
    model = Sequential()
    model.add(LSTM(100, input_shape=(train_x.shape[1], train_x.shape[2])))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer="adam")
    model.fit(train_x, train_y, epochs=100, batch_size=1, verbose=2)

    # prediction
    train_output = model.predict(train_x)
    test_output = model.predict(test_x)

    # de-normalize
    test_output = scaler.inverse_transform(test_output)

    for i in range(len(test_output)):
        prediction = round(test_output[i][0])
        print("Dispenser {} will run out of sanitizer in {} days".format(i+1, prediction))

if __name__ == "__main__":
    main()