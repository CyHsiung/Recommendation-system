#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
import tensorflow as tf
import json
from os.path import join
import argparse

# project_dir: Recommedation/
project_dir = os.path.abspath('./')
corpus_dir = join(project_dir, 'corpus')

def change_embedding(args):
    model_saver = tf.train.import_meta_graph(join(args.model_directory, args.model_name + '.meta'))
    with tf.Session() as sess:
        print("Save final embeddings as numpy array")
        model_saver.restore(sess, join(args.model_directory, args.model_name))
        np_node_embeddings = tf.get_default_graph().get_tensor_by_name("embedding_matrix/embed_matrix:0")
        np_node_embeddings = sess.run(np_node_embeddings)
        np.savez(os.path.join(args.model_directory, "node_embeddings.npz"),np_node_embeddings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type = str)
    parser.add_argument('--model_directory', type = str)
    args = parser.parse_args()
    change_embedding(args)



