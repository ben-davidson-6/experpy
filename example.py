import tensorflow as tf

from experpy.callback import GitTrackCallback

# dataset
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# model
model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10)
])

# loss
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

# build full model
metric = 'accuracy'
model.compile(
    optimizer='adam',
    loss=loss_fn,
    metrics=[metric])


# will need to build the metric, repo and tracker
callback = GitTrackCallback(metric, mode='max')


model.fit(
    x_train,
    y_train,
    epochs=5,
    callbacks=[callback])

