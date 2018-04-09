import numpy as np

def test_load_data():
    x_train = [np.random.rand(40, 300), np.random.rand(40, 300)] 
    # x_train = [np.concatenate((np.zeros((20,300)),np.ones((20,300))), axis = 0), np.concatenate((np.ones((20,300)),np.zeros((20,300))), axis = 0)]
    y_train = [0] * 20 + [5] * 20
    # x_train = [np.random.rand(16,24,18,1)] * 10 + [np.random.rand(26,20,22,1)] * 10
    x_val = [np.concatenate((np.zeros((5,300)),np.ones((5,300))), axis = 0), np.concatenate((np.ones((5,300)),np.zeros((5,300))), axis = 0)]
    
    y_val = [0] * 5 + [5] * 5
    return x_train, y_train, x_val, y_val

def test_load_test():
    x_test = [np.concatenate((np.zeros((5,300)),np.ones((5,300))), axis = 0), np.concatenate((np.ones((5,300)),np.zeros((5,300))), axis = 0)]
    y_test = [0] * 5 + [5] * 5 
    return x_test, y_test
    
        
if __name__ == '__main__':
    x_train, y_train, x_val, y_val = test_load_data()
    print(x_train[0:2], y_train[0].shape, x_val[0].shape, y_val[0].shape)
    print(y_val)
