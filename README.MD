# Experpy \*work in progress*

Cheap and cheerful way to track tensorflow experiments through git tags with minimal effort using `tf.keras.callbacks.Callback`:


```python
# example.py

from experpy.callback import GitTrackCallback

# build my model
# ...

metric = 'accuracy'
model.compile(
    optimizer='adam',
    loss=loss_fn,
    metrics=[metric])


# will find the repo containing example.py and track the
# metric of interest. 
# - An automatic commit is made on the current branch 
#   if there are some untracked files or differences between the 
#   working directory and last commit
# - At the end of each epoch a tag with the metric value is updated
#   with the value pulled from the TF logs

callback = GitTrackCallback(metric, mode='max')


model.fit(
    x_train,
    y_train,
    epochs=5,
    callbacks=[callback])

```
You can see what this looks like from me running `example.py` while having the `testing` branch checked out:
```bash
$ git log --oneline --decorate --graph --all

*   91b99cf (tag: experpy-accuracy-0.9766833186149597, testing) Merge branch 'main' into testing
|\  
| * 5451333 (HEAD -> main) will find the repo automatically
* | a0ed1c4 (tag: experpy-accuracy-0.975600004196167) AUTO experpy AUTO
* | 9df2bd8 (tag: experpy-accuracy-0.9768833518028259) AUTO experpy AUTO
|/  
* e290a80 have some basic functionality
* cdba2c8 made basic git functionality
* 32ec90e (origin/main, origin/HEAD) Initial commit
```

To install
```pip install git+https://github.com/ben-davidson-6/experpy```
