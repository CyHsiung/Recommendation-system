import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf

def meta_embed(x_train, seed, drop_rate):
    dense_1 = tf.layers.dense(inputs = x_train, units = 20, activation = tf.tanh)
    weight = tf.Variable([1.0])
    drop_1 = tf.layers.dropout(inputs = dense_1, rate = drop_rate)
    return weight * drop_1

def HIN_model(x_train_0, x_train_1, drop_rate = 1, seed=None):
    
    with tf.name_scope("weighted_sum"):
        embed_1 = meta_embed(x_train_0, seed, drop_rate)
        embed_2 = meta_embed(x_train_1, seed, drop_rate)
        weighted_sum = tf.sigmoid(embed_1 + embed_2)
           
    y = tf.layers.dense(inputs = weighted_sum, units = 1)
    return y

    
