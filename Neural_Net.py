import numpy as np
import matplotlib.pyplot as plt

X = np.genfromtxt('traindata.csv', delimiter=',')
Y = np.genfromtxt('trainlabel.csv', delimiter=',')
Y = Y.reshape((1, np.shape(Y)[0]))
Y = Y > 1.0
X = X.T

print(np.shape(X))      #X.shape == (# features, # training examples)
print(np.shape(Y))      #Y.shape == (1, # training examples)

test_data = np.genfromtxt('testdata.csv', delimiter=',')
test_label = np.genfromtxt('testlabel.csv', delimiter=',')
test_label = test_label.reshape((1, np.shape(test_label)[0]))
test_label = test_label > 1.0
test_data = test_data.T

#Normalize features
mean = X.mean(axis=0)
std = X.std(axis=0)
train_data = (X - mean) / std
test_mean = test_data.mean(axis=0)
test_std = test_data.std(axis=0)
test_data = (test_data - test_mean) / test_std

#X = None            #assign to training set
#Y = None            #assign to labels for X

shape_X = np.shape(X)
shape_Y = np.shape(Y)
m = np.shape(X)[1]

def sigmoid(z):
    return 1 / (1 + np.exp(-(z)))

"""
Arguments:
X -- input dataset of shape (input size, number of examples)
Y -- labels of shape (output size, number of examples)
Returns:
n_x -- the size of the input layer
n_h -- the size of the hidden layer
n_y -- the size of the output layer """
def layer_sizes(X, Y):
    n_x = np.shape(X)[0]
    n_h = 4
    n_y = np.shape(Y)[0]
    return n_x, n_h, n_y

"""
Arguments:
X -- input dataset of shape (input size, number of examples)
Y -- labels of shape (output size, number of examples)
Returns:
params -- python dictionary containing your parameters:
                W1 -- weight matrix of shape (n_h, n_x)
                b1 -- bias vector of shape (n_h, 1)
                W2 -- weight matrix of shape (n_y, n_h)
                b2 -- bias vector of shape (n_y, 1) """
def initialize_parameters(X, Y):
    n_x = np.shape(X)[0]
    n_h = 4
    n_y = np.shape(Y)[0]

    print('Input layer size: ' + str(n_x))
    print('Hidden layer size: ' + str(n_h))
    print('Output layer size: ' + str(n_y))

    W1 = np.random.randn(n_h, n_x) * 0.01       #initalize weights randomly to avoid symmetry
    b1 = np.zeros((n_h, 1))
    W2 = np.random.randn(n_y, n_h) * 0.01
    b2 = np.zeros((n_y, 1))

    assert (W1.shape == (n_h, n_x))             #ensure everything is the correct size
    assert (b1.shape == (n_h, 1))
    assert (W2.shape == (n_y, n_h))
    assert (b2.shape == (n_y, 1))

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters

"""
Argument:
X -- input data of size (n_x, m)
parameters -- python dictionary containing your parameters (output of initialization function)
Returns:
A2 -- The sigmoid output of the second activation
cache -- a dictionary containing "Z1", "A1", "Z2" and "A2"  """
def forward_propagation(X, parameters):

    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    Z1 = W1.dot(X) + b1
    A1 = np.tanh(Z1)            #An = g(Wn * Xn-1 + bn) where g is the activation function
    Z2 = W2.dot(A1) + b2
    A2 = sigmoid(Z2)            #A2.shape == (1, X.shape[1])

    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}

    return A2, cache

"""
Computes the cross-entropy cost given in equation (13)
Arguments:
A2 -- The sigmoid output of the second activation, of shape (1, number of examples)
Y -- "true" labels vector of shape (1, number of examples)
parameters -- python dictionary containing your parameters W1, b1, W2 and b2
Returns:
cost -- cross-entropy cost given equation (13)  """
def compute_cost(A2, Y, parameters):
    m = Y.shape[1]  # number of example
    cost = -(1 / m * np.sum(Y.dot(np.log(A2).T) + (1 - Y).dot(np.log(1 - A2).T)))
    cost = np.squeeze(cost)
    return cost

"""
preform backward propagation
Arguments:
parameters -- python dictionary containing our parameters
cache -- a dictionary containing "Z1", "A1", "Z2" and "A2".
X -- input data of shape (2, number of examples)
Y -- "true" labels vector of shape (1, number of examples)
Returns:
grads -- python dictionary containing your gradients with respect to different parameters   """
def backward_propagation(parameters, cache, X, Y):
    m = X.shape[1]

    W1 = parameters["W1"]
    W2 = parameters["W2"]

    A1 = cache["A1"]
    A2 = cache["A2"]

    dZ2 = A2 - Y
    dW2 = dZ2.dot(A1.T) / m
    db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = W2.T.dot(dZ2) * (1 - np.power(A1, 2))
    dW1 = dZ1.dot(X.T) / m
    db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)

    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}

    return grads

"""
Updates parameters using the gradient descent update rule given above
Arguments:
parameters -- python dictionary containing your parameters
grads -- python dictionary containing your gradients
Returns:
parameters -- python dictionary containing your updated parameters  """
def update_parameters(parameters, grads, learning_rate=1.2):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]

    W1 = W1 - learning_rate * dW1
    b1 = b1 - learning_rate * db1
    W2 = W2 - learning_rate * dW2
    b2 = b2 - learning_rate * db2

    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}

    return parameters

"""
Arguments:
X -- dataset of shape (2, number of examples)
Y -- labels of shape (1, number of examples)
n_h -- size of the hidden layer
num_iterations -- Number of iterations in gradient descent loop
print_cost -- if True, print the cost every 1000 iterations
Returns:
parameters -- parameters learnt by the model. They can then be used to predict. """
def nn_model(X, Y, n_h, num_iterations=10000, print_cost=False):
    n_x = layer_sizes(X, Y)[0]
    n_y = layer_sizes(X, Y)[2]

    parameters = initialize_parameters(X, Y)
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]

    costs = []

    for i in range(0, num_iterations):
        A2, cache = forward_propagation(X, parameters)
        cost = compute_cost(A2, Y, parameters)
        grads = backward_propagation(parameters, cache, X, Y)
        parameters = update_parameters(parameters, grads, learning_rate=1.2)

        # Print the cost every 1000 iterations
        if print_cost and i % 1000 == 0:
            print("Cost after iteration %i: %f" % (i, cost))
        if i % 50 == 0:
            costs.append(cost)

    return parameters, costs

"""
Using the learned parameters, predicts a class for each example in X
Arguments:
parameters -- python dictionary containing your parameters
X -- input data of size (n_x, m)
Returns
predictions -- vector of predictions of our model (red: 0 / blue: 1)    """
def predict(parameters, X):
    A2, cache = forward_propagation(X, parameters)
    predictions = (A2 > 0.5)
    return predictions

def print_accuracy(parameters, X):
    predictions = predict(parameters, X)
    print ('Accuracy: %d' % float((np.dot(Y,predictions.T) + np.dot(1-Y,1-predictions.T))/float(Y.size)*100) + '%')

parameters = initialize_parameters(X, Y)
A2, cache = forward_propagation(X, parameters)
grads = backward_propagation(parameters, cache, X, Y)
parameters, costs = nn_model(X, Y, 4, num_iterations=2000, print_cost=True)

plt.plot(costs)
plt.show()

predictions = predict(parameters, X)
print ('Accuracy train data: %d' % float((np.dot(Y,predictions.T)
                                          + np.dot(1-Y,1-predictions.T))/float(Y.size)*100) + '%')
predictions = predict(parameters, test_data)
print ('Accuracy test data: %d' % float((np.dot(test_label,predictions.T)
                                         + np.dot(1-test_label,1-predictions.T))/float(test_label.size)*100) + '%')

