from keras.layers import Input, Dense, Lambda, concatenate, Conv1D, Concatenate, Flatten, MaxPooling1D
from keras.models import Sequential, Model
from nn_evaluation_interface import plot_loss

# Import Sotchastic Gradient Descent object from Keras to allow for tweaking its learning rate.
from keras.optimizers import SGD

# A deep autoencoder which learns to reconstruct fragment spectra.
# Structure: (Input)1000-256-128-16-128-256-1000(Output)
def basic_autoencoder(x_train, epochs=100, encoded_dim=10):
    # Create input based on the provided x_train data structure.
    inputLayer = Input(shape=(x_train.shape[1],))  # fixed
    # Since an autoencoder reconstructs input, output will have the same shape as input.
    output_dims = x_train.shape[1]

    # Create the encoding layers using Keras' functional API.
    l = inputLayer
    l = Dense(256, activation='relu')(l)
    l = Dense(128, activation='relu')(l)
    l = Dense(16, activation='relu')(l)

    # Create reference to latent space in case we need it later for interpolation(not used in the end)
    latent_space = l

    # Create decoding layers using functional API.
    l2 = Dense(128, activation='relu')(l)
    l2 = Dense(256, activation='relu')(l2)
    l2 = Dense(output_dims, activation='relu')(l2)

    # Store reference to final output.
    out_layer = l2

    auto_model = Model(input=inputLayer, output=out_layer)  # Create model.

    # Set SGD learning rate and compile model with MSE as loss function.
    sgd = SGD(lr=0.1)
    auto_model.compile(loss='mean_squared_error', optimizer=sgd)

    # Train the model for the specified number of epochs, using the specified validation fraction.
    autoencoder_train = auto_model.fit(x_train, x_train, shuffle=False, validation_split=val_fraction, epochs=epochs)

    # Once traning is done, plot model loss and validation loss
    # This is a visual guide for how well the model is learning (is it overfitting, underfitting?)
    plot_loss(autoencoder_train, epochs)

    return auto_model  # Return the model, now trained.


# An encoder which learns to turn fragment spectra into CDK fingerprints for the same molecule.
# Structure: (Input)1000-256-128-16-128-256-307(Output)
def fingerprint_autoencoder(x_train_spectra, x_train_fingerprints, epochs=100, lr=0.5):
    # Create input based on the provided x_train data structure.
    input_layer = Input(shape=(x_train_spectra.shape[1],))
    # Since output is not the same as input, we obtain its shape separately.
    output_dims = x_train_fingerprints.shape[1]

    # Create the encoding layers using functional API.
    l = input_layer
    l = Dense(256, activation='relu')(l)
    l = Dense(128, activation='relu')(l)
    l = Dense(16, activation='relu')(l)

    # Create reference to latent space
    latent_space = l

    # Create decoding layers using functional API.
    l2 = Dense(128, activation='relu')(l)
    # Linear activation function followed by sigmoid to get outputs between 0 and 1.
    # This is done because the output fingerprint is a set of bits (0 or 1).
    # Linear activation ensures that values can be negative (necessary for sigmoid to function)
    l2 = Dense(256, activation='linear')(l2)
    l2 = Dense(output_dims, activation='sigmoid')(l2)

    # Store reference to final output.
    out_layer = l2

    auto_model = Model(input=input_layer, output=out_layer)

    # Set SGD learning rate provided as parameter and compile model with MSE as loss function.
    sgd = SGD(lr=lr)
    auto_model.compile(loss='mean_squared_error', optimizer=sgd)

    # Train the model for the specified number of epochs, using the specified validation fraction.
    autoencoder_train = auto_model.fit(x_train_spectra, x_train_fingerprints, shuffle=False,
                                       validation_split=val_fraction, epochs=epochs)

    # Once traning is done, plot model loss and validation loss
    plot_loss(autoencoder_train, epochs)

    return auto_model  # Return the model, now trained.


# A simplified spectrum-fingeprrint encoder.
# Structure: (Input)1000-500-200-307(Output)
def simplified_fingerprint_model(x_train_spectra, x_train_fingerprints, epochs=100, lr=0.5):
    # Create input based on the provided x_train data structure.
    input_layer = Input(shape=(x_train_spectra.shape[1],))
    # Since output is not the same as input, we obtain its shape separately.
    output_dims = x_train_fingerprints.shape[1]

    # Create the encoding layers using functional API.
    l = input_layer
    l = Dense(500, activation='relu')(l)

    # Linear activation ensures that values can be negative (necessary for sigmoid to function)
    l = Dense(200, activation='linear')(l)

    # Save reference to latent space
    latent_space = l

    # Sigmoid activation to get outputs between 0 and 1. This is done because the output fingerprint is a set of bits (0 or 1).
    l2 = Dense(output_dims, activation='sigmoid')(l)

    # Reference for output layer
    out_layer = l2

    auto_model = Model(input=input_layer, output=out_layer)

    # Set SGD learning rate provided as parameter and compile model with MSE as loss function.
    sgd = SGD(lr=0.05)
    auto_model.compile(loss='binary_crossentropy', optimizer=sgd)

    # Train the model for the specified number of epochs, using the specified validation fraction.
    autoencoder_train = auto_model.fit(x_train_spectra, x_train_fingerprints, shuffle=False, validation_split=0.1,
                                       epochs=epochs)

    # Loss Plots
    plot_loss(autoencoder_train, epochs)

    return auto_model


# A simplified fingeprint-family encoder.
# Structure: (Input)307-128-16-8(Output)
def simplified_family_model(x_train_fingerprints, x_train_families, epochs=100, lr=0.5):
    # Create input based on the provided x_train data structure.
    input_layer = Input(shape=(x_train_fingerprints.shape[1],))
    # Since output is not the same as input, we obtain its shape separately.
    output_dims = x_train_families.shape[1]

    # Create the encoding layers using functional API.
    l = input_layer
    l = Dense(128, activation='relu')(l)

    # Linear activation ensures that values can be negative (necessary for sigmoid to function)
    l = Dense(16, activation='linear')(l)

    # Save reference to latent space
    latent_space = l

    # Sigmoid activation to get outputs between 0 and 1. This is done because the output fingerprint is a set of bits (0 or 1).
    l2 = Dense(output_dims, activation='sigmoid')(l)

    # Reference for output layer
    out_layer = l2

    auto_model = Model(input=input_layer, output=out_layer)

    # Set SGD learning rate provided as parameter and compile model with MSE as loss function.
    sgd = SGD(lr=0.05)
    auto_model.compile(loss='binary_crossentropy', optimizer=sgd)

    # Train the model for the specified number of epochs, using the specified validation fraction.
    autoencoder_train = auto_model.fit(x_train_fingerprints, x_train_families, shuffle=False, validation_split=0.1,
                                       epochs=epochs)

    # Loss Plots
    plot_loss(autoencoder_train, epochs)

    return auto_model  # Return model, now trained


# Creates and trains spectrum-fingerprint encoder which combines Dense layers with a single Conv1D layer using a Merge Layer
# A hybrid neural network: requires both normal and convolutional spectra as inputs: convolutional has 1 more dimension
# Allows for specifying training epochs and kernel size(filter width). Number of filters is kept constant
def conv_autoencoder(x_train_conv, x_train_dense, x_train_fingerprints, epochs=100, kernel_size=20):
    # Grab input and output shapes
    conv_input = Input(shape=(x_train_conv.shape[1], 1))
    dense_input = Input(shape=(x_train_dense.shape[1],))
    output_dims = x_train_fingerprints.shape[1]

    # 1D convolution on spectra
    c = conv_input
    # Name layer in case weights need to be extracted.
    c = Conv1D(32, kernel_size, activation='relu', padding='valid', name='conv_layer')(conv_input)
    f = Flatten()(c)  # Flatten for merging

    # Dense layer on spectra
    d = dense_input
    d = Dense(500, activation='relu')(d)

    # Merge convolution and dense layers
    m = concatenate(([f, d]))
    # Linear activation layer
    m = Dense(200, activation='linear')(m)

    # Save reference to latent space
    latent_space = m
    # Final sigmoid layer to get fingerprint output.
    l2 = Dense(output_dims, activation='sigmoid')(m)

    out_layer = l2

    auto_model = Model(inputs=[conv_input, dense_input], output=out_layer)

    # Set SGD learning rate, compile model with MSE as loss function
    sgd = SGD(lr=0.5)
    auto_model.compile(loss='mean_squared_error', optimizer=sgd)

    # Train model using specified number of epochs and validationf fraction.
    autoencoder_train = auto_model.fit([x_train_conv, x_train_dense], x_train_fingerprints, shuffle=False,
                                       validation_split=0.1, epochs=epochs)

    # Plot loss
    plot_loss(autoencoder_train, epochs)

    return auto_model


# Creates and trains a fingerprint-spectrum encoder which uses only a convolution layer
# Note that the input must be ready for the Conv1D layer: needs an additional dimension added.
# Allows for specifying training epochs and kernel size(filter width). Number of filters is kept constant
def conv_only_autoencoder(x_train_conv, x_train_fingerprints, epochs=100, kernel_size=20):
    # Grab input and output shapes
    conv_input = Input(shape=(x_train_conv.shape[1], 1))
    output_dims = x_train_fingerprints.shape[1]

    # 1D convolution on spectra
    c = conv_input
    # Name layer in case we want to extract weights
    c = Conv1D(32, kernel_size, activation='relu', padding='valid', name='conv_layer')(conv_input)
    c = MaxPooling1D()(c)
    c = Flatten()(c)

    d = Dense(200, activation='linear')(c)

    l2 = Dense(output_dims, activation='sigmoid')(d)

    out_layer = l2

    auto_model = Model(inputs=conv_input, output=out_layer)

    # Set learning rate, compile model with mse
    sgd = SGD(lr=0.5)
    auto_model.compile(loss='mean_squared_error', optimizer=sgd)

    # Train for specified number of epochs
    autoencoder_train = auto_model.fit(x_train_conv, x_train_fingerprints, shuffle=False,
                                       validation_split=0.1, epochs=epochs)

    plot_loss(autoencoder_train, epochs)

    return auto_model


# Creates and trains a hybrid model identical to conv_autoencoder but with an added MaxPooling1D layer.
def conv_pool_autoencoder(x_train_conv, x_train_dense, x_train_fingerprints, epochs=100, kernel_size=20):
    conv_input = Input(shape=(x_train_conv.shape[1], 1))
    dense_input = Input(shape=(x_train_dense.shape[1],))
    output_dims = x_train_fingerprints.shape[1]

    # 1D convolution on spectra
    c = conv_input
    print(kernel_size)
    c = Conv1D(32, kernel_size, activation='relu', padding='valid', name='conv_layer')(conv_input)
    c = MaxPooling1D()(c)
    f = Flatten()(c)  # Flatten for merging

    # Dense layer on spectra
    d = dense_input
    d = Dense(500, activation='relu')(d)

    # Merge convolution and dense layers
    m = concatenate(([f, d]))
    m = Dense(200, activation='linear')(m)

    latent_space = m

    l2 = Dense(output_dims, activation='sigmoid')(m)

    out_layer = l2

    auto_model = Model(inputs=[conv_input, dense_input], output=out_layer)

    # Set learning rate, compile.
    sgd = SGD(lr=0.5)
    auto_model.compile(loss='mean_squared_error', optimizer=sgd)

    autoencoder_train = auto_model.fit([x_train_conv, x_train_dense], x_train_fingerprints, shuffle=False,
                                       validation_split=0.1, epochs=epochs)

    plot_loss(autoencoder_train, epochs)

    return auto_model