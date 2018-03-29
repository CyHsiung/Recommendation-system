import os
import sys
from os.path import join

project_dir = os.path.abspath('./')
'''
while project_dir[-3:] != 'src':
    project_dir = os.path.abspath(join(project_dir, os.pardir))
project_dir = join(project_dir, '..')
'''
sys.path.append(project_dir)
from src.metapath2vec.meta2vec import meta2vec
# call function
userEmbed, prodEmbed, missingUser = meta2vec(nodeById = None, userNum = None, prodNum = None, tag_fileName = None, pref_fileName = None)
