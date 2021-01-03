#!/usr/bin/env python3

from tensorflow import keras
from keras import layers

from keras import regularizers

from keras.datasets import mnist
import numpy as np

# This is the size of our encoded representations
encoding_dim = 32  # 32 floats -> compression of factor 24.5, assuming the input is 784 floats

input_img = keras.Input(shape=(1024,))
encoded = layers.Dense(256, activation='relu')(input_img)
encoded = layers.Dense(64, activation='relu')(encoded)
encoded = layers.Dense(32, activation='relu')(encoded)
#encoded = layers.Dense(16, activation='relu')(encoded)

decoded = layers.Dense(64, activation='relu')(encoded)
decoded = layers.Dense(256, activation='relu')(decoded)
decoded = layers.Dense(1024, activation='sigmoid')(decoded)

# This model maps an input to its reconstruction
autoencoder = keras.Model(input_img, decoded)

autoencoder.compile(optimizer='adam', loss='binary_crossentropy')
#autoencoder.compile(optimizer='rmsprop', loss='mean_squared_error')

#(x_train, _), (x_test, _) = mnist.load_data()
data = np.load( 'pieces_2021-01-03_0513.npy' )
validation_split = int(len(data)*0.8)
x_train = data[:validation_split]
x_test = data[validation_split:]

# We will normalize all values between 0 and 1 and we will flatten the 28x28 images into vectors of size 784.

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
print(x_train.shape)
print(x_test.shape)

# Now let's train our autoencoder for 50 epochs:

autoencoder.fit(x_train, x_train,
                epochs=50,
                batch_size=256,
                shuffle=True,
                validation_data=(x_test, x_test))

autoencoder.save_weights( 'autoencoder_deep.h5' )

encoder = keras.Model(input_img, encoded)
#encoder.compile(optimizer='rmsprop', loss='mean_squared_error')
#encoder.load_weights( 'autoencoder_deep.h5' )
#for l1, l2 in zip( encoder, autoencoder ) :
#	l1.set_weights( l2.get_weights() )
#sys.exit()

encoded_imgs = encoder.predict(x_test)
np.savetxt( 'encoded_images_32.txt', encoded_imgs)

# After 50 epochs, the autoencoder seems to reach a stable train/validation loss value of about 0.09. We can try to visualize the reconstructed inputs and the encoded representations. We will use Matplotlib.

# Encode and decode some digits
# Note that we take them from the *test* set
## encoded_imgs = encoder.predict(x_test)
## decoded_imgs = decoder.predict(encoded_imgs)
decoded_imgs = autoencoder.predict(x_test)

# Use Matplotlib (don't ask)
import matplotlib.pyplot as plt

n = 40  # How many digits we will display
plt.figure(figsize=(20, 4))
for i in range(n):
    # Display original
    ax = plt.subplot(2, n, i + 1)
    plt.imshow(x_test[i].reshape(32, 32))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    # Display reconstruction
    ax = plt.subplot(2, n, i + 1 + n)
    plt.imshow(decoded_imgs[i].reshape(32, 32))
    plt.gray()
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()

