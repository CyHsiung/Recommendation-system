import numpy as np
import tensorflow as tf
import os
import sys
from os.path import join
from tqdm import tqdm
import shutil

import datetime

project_dir = os.path.abspath('./')
sys.path.append(project_dir)
from src.HIN.model import HIN_model
from src.HIN.load_data import test_load_data
corpus_dir = join(project_dir, 'corpus')
models_dir = join(project_dir, 'models')
if not os.path.exists(models_dir):
    os.makedirs(models_dir)

saveModel_dir = join(models_dir, 'HIN_model')

def train_neural_network(x_train_list, y_train, x_val_list, y_val, learning_rate = 0.05, drop_rate = 0.7, epochs = 10, batch_size = 5):
    if os.path.exists(saveModel_dir):
        shutil.rmtree(saveModel_dir, ignore_errors=True)
    os.makedirs(saveModel_dir)
    
    x_input_0 = tf.placeholder(tf.float32, shape=(None, 300), name = 'input_0')
    x_input_1 = tf.placeholder(tf.float32, shape=(None, 300), name = 'input_1')
    y_input = tf.placeholder(tf.float32, shape=None, name = 'output')
    drop_prob = tf.placeholder(tf.float32, shape = None)
    with tf.name_scope("prediction"):
        prediction = HIN_model(x_input_0, x_input_1, drop_prob, seed = 42)
        y_pred = tf.identity(prediction, name = 'y_pred')
        cost = tf.losses.mean_squared_error(predictions = y_pred, labels = y_input)
                              
    with tf.name_scope("training"):
        optimizer = tf.train.AdamOptimizer(learning_rate).minimize(cost)
    
    
    # to save model
    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())

        start_time = datetime.datetime.now()

        iterations = int(len(x_train_list[0])/batch_size) + 1
        # run epochs

        for epoch in range(epochs):
            start_time_epoch = datetime.datetime.now()
            print('Epoch: ', epoch)
            epoch_loss = 0
            # mini batch
            for itr in tqdm(range(iterations)):
                mini_batch_x = [x_train_list[0][itr * batch_size: min((itr + 1)*batch_size, len(x_train_list[0])), :], x_train_list[1][itr * batch_size: min((itr + 1)*batch_size, len(x_train_list[1])), :]]
                mini_batch_y = y_train[itr * batch_size: min((itr + 1)*batch_size, len(y_train))]
                if not mini_batch_x:
                    continue
                _optimizer, _cost = sess.run([optimizer, cost], feed_dict={x_input_0: mini_batch_x[0], x_input_1: mini_batch_x[1], y_input: mini_batch_y, drop_prob: drop_rate})
                epoch_loss += _cost

            #  using mini batch in case not enough memory
            minLoss = float("Inf")
            numValBatches = int(len(x_val_list[0])/batch_size)
            loss = 0
            for itr in range(numValBatches):
                mini_batch_x_val = [x_val_list[0][itr * batch_size: min((itr + 1)*batch_size, len(x_val_list[0])), :], x_val_list[1][itr * batch_size: min((itr + 1)*batch_size, len(x_val_list[1])), :]]
                mini_batch_y_val = y_val[itr * batch_size: min((itr + 1)*batch_size, len(y_val))]
                if not mini_batch_x_val:
                    continue
                loss += sess.run(cost, feed_dict={x_input_0: mini_batch_x_val[0], x_input_1: mini_batch_x_val[1], y_input: mini_batch_y_val,})
            valLoss = round(loss / (numValBatches * batch_size), 3)
            end_time_epoch = datetime.datetime.now()
            print(' Testing Set loss:', valLoss, ' Time elapse: ', str(end_time_epoch - start_time_epoch))
            if valLoss < minLoss:
                # save model when better performance
                saver.save(sess, join(saveModel_dir, 'loss_' + str(valLoss)))
                saver.save(sess, join(saveModel_dir, 'best'))
                minLoss = valLoss 

        end_time = datetime.datetime.now()
        print('Time elapse: ', str(end_time - start_time))

if __name__ == '__main__':
    x_train, y_train, x_val, y_val = test_load_data()
    train_neural_network(x_train, y_train, x_val, y_val)
    
    
    
