import numpy as np
import tensorflow as tf
from os.path import join
import os
import sys

project_dir = os.path.abspath('./')
corpus_dir = join(project_dir, 'corpus')
models_dir = join(project_dir, 'models')
sys.path.append(project_dir)
from src.HIN.load_data import test_load_test

loadModel_dir = 'HIN_model'
loadModelName = 'best'

loadModel_dir = join(models_dir, loadModel_dir)


def predict(x_test_list, y_test, batch_size = 5):
    tf.reset_default_graph()
    model_saver = tf.train.import_meta_graph(join(loadModel_dir, loadModelName + '.meta'))
    with tf.Session() as sess:
        acc = 0
        numValBatches = int(len(x_test_list[0])/batch_size)
        model_saver.restore(sess, join(loadModel_dir, loadModelName))
        graph = tf.get_default_graph()
        x_input_0 = graph.get_tensor_by_name("input_0:0")
        x_input_1 = graph.get_tensor_by_name("input_1:0")
        y_input = graph.get_tensor_by_name("output:0")
        y_predict = graph.get_tensor_by_name('prediction/y_pred:0')
        # get name for all layer 
        '''
        x = [n.name for n in tf.get_default_graph().as_graph_def().node]
        for n in x:
            print(n)
        '''
        y_list = []
        # test data accuracy
        for itr in range(numValBatches):
            mini_batch_x_test = [x_test_list[0][itr * batch_size: min((itr + 1)*batch_size, len(x_test_list[0])), :], x_test_list[1][itr * batch_size: min((itr + 1)*batch_size, len(x_test_list[0])), :]]
            mini_batch_y_test = y_test[itr * batch_size: min((itr + 1) * batch_size, len(y_test))]
            if not mini_batch_x_test:
                continue
            element = sess.run(y_predict, feed_dict={x_input_0: mini_batch_x_test[0], x_input_1: mini_batch_x_test[1], y_input: mini_batch_y_test})
            for i in range(element.shape[0]):
                y_list.append(element[i, 0])
            # print(sess.run(y_predict, feed_dict={x_input_0: mini_batch_x_test[0], x_input_1: mini_batch_x_test[1], y_input: mini_batch_y_test}))
    print("y_list: ", y_list)
    print("predict over")
    
    return y_list
        

if __name__ == '__main__':
    x_test, y_test = test_load_test()
    predict(x_test, y_test)
    
