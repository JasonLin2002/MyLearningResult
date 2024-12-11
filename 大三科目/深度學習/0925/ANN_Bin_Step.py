import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore

def binary_step( x ):
    return np.where( x >= 0, 1, 0 )

def draw_error_history( data ):
    plt.figure(figsize=(10, 7))
    x = np.array(range(1, len(data)+1))
    plt.plot(x, data)
    plt.grid( True )
    plt.title('Error history')
    plt.xlabel('iteration')
    plt.ylabel('mse')
    plt.show()

if __name__ == '__main__':
    train_input = np.array([[0, 0, 1],
                            [1, 1, 1],
                            [1, 0, 1],
                            [0, 1, 1]])
    train_output = np.array([[0, 1, 1, 0]]).T
    np.random.seed( 1 )
    synaptic_weights = 2 * np.random.random((3, 1)) - 1
    bias = np.random.rand(1)
    learning_rate = 0.1

    print(f'Random starting synaptic weights:\n{synaptic_weights}')
    print(f'Random starting bias:\n{bias}')
    print(f'Learning rate:\n{learning_rate}')

    epochs = 10
    history = []
    for iteration in range( epochs ):
        linear_output = np.dot(train_input, synaptic_weights) + bias
        predicted_output = binary_step( linear_output )
        error = train_output - predicted_output
        print( f'Epoch: {iteration} => Error: {error}')
        synaptic_weights += learning_rate * np.dot(train_input.T, error)
        bias += learning_rate * sum( error )
        history.append( sum(error ** 2) / len(predicted_output) )

    print(f'Final synaptic weights: \n{synaptic_weights}')
    print(f"After training bias: \n{bias}")
    draw_error_history( np.array( history ))