#!/usr/bin/env python
import numpy as np
from keras.models import Sequential
from keras.layers import (Conv2D, LeakyReLU, Dropout, Flatten,
                          Dense, Activation, BatchNormalization,
                          Conv2DTranspose, UpSampling2D,
                          Reshape)
from keras.optimizers import RMSprop

# https://towardsdatascience.com/gan-by-example-using-keras-on-tensorflow-backend-1a6d515a60d0


def build_discriminator():
    discriminator = Sequential(name="discriminator")
    depth = 5
    dropout = 0.4
    filter_size = 3

    input_shape = (6, 6, 1)

    discriminator.add(Conv2D(
        depth*1,
        filter_size,
        strides=2,
        input_shape=input_shape,
        padding='same',
        activation=LeakyReLU(alpha=0.2))
    )

    discriminator.add(Dropout(dropout))

    discriminator.add(Conv2D(
        depth*2,
        filter_size,
        strides=2,
        padding='same',
        activation=LeakyReLU(alpha=0.2))
    )

    discriminator.add(Dropout(dropout))

    discriminator.add(Flatten())
    discriminator.add(Dense(1))
    discriminator.add(Activation('sigmoid'))
    discriminator.summary()
    return discriminator


def build_generator():
    depth = 5
    generator = Sequential(name="generator")
    generator.add(Dense(3 * 3 * depth, input_dim=10))
    generator.add(BatchNormalization(momentum=0.9))
    generator.add(Activation("relu")),
    generator.add(Reshape((3, 3, depth))),
    generator.add(UpSampling2D()),
    generator.add(Conv2DTranspose(1, 3, padding='same'))
    generator.add(Activation('sigmoid'))
    generator.summary()
    return generator


if __name__ == "__main__":

    discriminator = build_discriminator()
    generator = build_generator()

    optimizer = RMSprop(lr=0.0008, clipvalue=1.0, decay=6e-8)
    dm = Sequential()
    dm.add(discriminator)
    dm.compile(
        loss='binary_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy']
    )

    optimizer = RMSprop(lr=0.0004, clipvalue=1.0, decay=3e-8)
    adversarial = Sequential()
    adversarial.add(generator)
    adversarial.add(discriminator)
    adversarial.compile(
        loss='binary_crossentropy',
        optimizer=optimizer,
        metrics=['accuracy']
    )


    batch_size = 2
    x_train = np.array([
        [
            [[1], [2], [3], [4], [5], [6]],
            [[1], [2], [3], [4], [5], [6]],
            [[1], [2], [3], [4], [5], [6]],
            [[1], [2], [3], [4], [5], [6]],
            [[1], [2], [3], [4], [5], [6]],
            [[1], [2], [3], [4], [5], [6]],
        ],
        [
            [[2], [4], [6], [8], [10], [12]],
            [[2], [4], [6], [8], [10], [12]],
            [[2], [4], [6], [8], [10], [12]],
            [[2], [4], [6], [8], [10], [12]],
            [[2], [4], [6], [8], [10], [12]],
            [[2], [4], [6], [8], [10], [12]],
        ]
    ])

    images_train = x_train

    noise = np.random.uniform(-1.0, 1.0, size=[batch_size, 10])

    epocs = 5000

    for i in range(epocs):

        print("== EPOCH", i)

        images_fake = generator.predict(noise)

        x = np.concatenate((images_train, images_fake))

        y = np.ones([2*batch_size, 1])

        y[batch_size:, :] = 0

        d_loss = dm.train_on_batch(x, y)

        print("Discriminator loss", d_loss)

        y = np.ones([batch_size, 1])

        noise = np.random.uniform(-1.0, 1.0, size=[batch_size, 10])

        a_loss = adversarial.train_on_batch(noise, y)

        print("Adversarial loss", a_loss)


    noise = np.random.uniform(-1.0, 1.0, size=[1, 10])
    print("prediction", generator.predict(noise))