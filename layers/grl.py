import tensorflow as tf
from keras import backend as K
from keras.layers import Layer
from uuid import uuid4

class GRL(Layer):
    def build(self, input_shape):
        self.trainable_weights = []
        super(GRL, self).build(input_shape)

    def call(self, inputs):
        x, input_lambda = inputs
        grad_name = 'GRL-' + str(uuid4())

        _lambda = input_lambda[0][0]

        @tf.RegisterGradient(grad_name)
        def _flip_gradients(op, grad):
            return [tf.negative(grad) * _lambda]

        g = K.get_session().graph
        with g.gradient_override_map({'Identity': grad_name}):
            y = tf.identity(x)
        return y

    def compute_output_shape(self, input_shape):
        return input_shape

    def get_config(self):
        base_config = super(GRL, self).get_config()
        return dict(list(base_config.items()))