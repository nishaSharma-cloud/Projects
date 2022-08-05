# Image Classification on MNIST dataset
This project performs a basic classification of images on the MNIST dataset using a basic neural network
  * Data is imported using TensorFlow.Keras
  * The Labels are encoded to categorical values using Keras
  * The data is reshaped from array to vector
  * Data is normalized using mean and std with a variation of epsilon to prevent the values from converging to absolute zero
  * The Neural network is a Sequential model with:
    * 128-neuron input dense layer with activation function as ReLU and input shape of 784
    * 128-neuron hidden dense layer with activation function as ReLU
    * 10-neuron output dense layer with activation function as Softmax
    * Loss as categorical cross-entropy
    * And the model is measured on accuracy metrics
    * Model is trained for 4 epochs.
  * The model reaches train accuracy of 96.7% with 0.1136 loss and test accuracy of 96.67% with 0.1099 loss
 
 # Technology stack:
 * TensorFlow
 * Keras
 * MNIST
 * Matplotlib
