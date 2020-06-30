
from random import randint
import numpy as np
import time
import tensorflow as tf
#resnet
LAYERS=4
FILTERS=16
is_using_TPU=False
#if I use tpu, optimizer must handle by "tf.tpu.CrossShardOptimizer" to cross more than one tpus.And then use it as GPU!!!
def net_fn(features, labels, mode):
	#The features must be: <tensor, shape=(batch_size, 6,7, 4)>
	#The labels must be: {'policy':<tensor, shape=(batch_size, 170)>, 'value':<tensor, shape=(batch_size, 1)>}
	#which value is z, and policy is pi in AlphaGo Zero paper
	#not to reshape as possible because TPU doesn't good at it
	
	#init
	layer=tf.compat.v1.layers.conv2d(inputs=features, filters=FILTERS, kernel_size=(2, 2), padding="same", activation=None)
	layer=tf.layers.batch_normalization(inputs=layer, axis=-1, center=False, scale=False, fused=True)
	layer=tf.nn.relu(layer)
	#residual block
	for i in range(LAYERS-1):
		layer=tf.compat.v1.layers.conv2d(inputs=layer, filters=FILTERS, kernel_size=(2, 2), padding="same", activation=None)
		layer=tf.layers.batch_normalization(inputs=layer, axis=-1, center=False, scale=False, fused=True)
		layer=tf.nn.relu(layer)
	#policy head
	policy_head_layer=tf.compat.v1.layers.conv2d(inputs=layer, filters=2, kernel_size=(1, 1), padding="same", activation=None)
	policy_head_layer=tf.layers.batch_normalization(inputs=policy_head_layer, axis=-1, center=False, scale=False, fused=True)
	policy_head_layer=tf.nn.relu(policy_head_layer)
	policy_head_layer=tf.reshape(policy_head_layer, [-1, 84])
	policy_head_output=tf.layers.dense(inputs=policy_head_layer, units=7)
	
	value_head_layer=tf.compat.v1.layers.conv2d(inputs=layer, filters=1, kernel_size=(1, 1), padding="same", activation=None)
	value_head_layer=tf.layers.batch_normalization(inputs=value_head_layer, axis=-1, center=False, scale=False, fused=True)
	value_head_layer=tf.nn.relu(value_head_layer)
	value_head_layer=tf.reshape(value_head_layer, [-1, 42])
	value_head_layer=tf.layers.dense(inputs=value_head_layer, units=16, activation=tf.nn.relu)
	value_head_output=tf.layers.dense(inputs=value_head_layer, units=1, activation=tf.math.sigmoid)
	
	logits={'policy_head':policy_head_output,'value_head':value_head_output}
	
	policy_head=tf.estimator.MultiClassHead(name='policy_head',n_classes=7)
	value_head=tf.estimator.RegressionHead(name='value_head')
	
	multi_head=tf.estimator.MultiHead([policy_head,value_head])
	
	return multi_head.create_estimator_spec(features=features,mode=mode, logits=logits,optimizer=tf.keras.optimizers.Adam,regularization_losses=tf.keras.regularizers.l2)
