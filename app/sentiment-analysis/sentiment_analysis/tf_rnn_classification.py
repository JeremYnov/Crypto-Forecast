import numpy as np

import tensorflow_datasets as tfds
import tensorflow as tf

tfds.disable_progress_bar()

import matplotlib.pyplot as plt

BUFFER_SIZE = 10000
BATCH_SIZE = 64
VOCAB_SIZE = 1000
PKL_FILENAME = "sentiment_analysis/trained_model.pkl"

class RNNClassifier:
    def __init__(self) -> None:
        pass

    def plot_graphs(history, metric):
        plt.plot(history.history[metric])
        plt.plot(history.history["val_" + metric], "")
        plt.xlabel("Epochs")
        plt.ylabel(metric)
        plt.legend([metric, "val_" + metric])

    def input_pipeline(self):
        dataset, info = tfds.load("imdb_reviews", with_info=True, as_supervised=True)
        self.train_dataset, self.test_dataset = dataset["train"], dataset["test"]
        self.train_dataset.element_spec

        for example, label in self.train_dataset.take(1):
            print("text: ", example.numpy())
            print("label: ", label.numpy())

        self.train_dataset = (
            self.train_dataset.shuffle(BUFFER_SIZE)
            .batch(BATCH_SIZE)
            .prefetch(tf.data.AUTOTUNE)
        )
        self.test_dataset = self.test_dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

        for example, label in self.train_dataset.take(1):
            print("texts: ", example.numpy()[:3])
            print()
            print("labels: ", label.numpy()[:3])

        self.encoder = tf.keras.layers.TextVectorization(max_tokens=VOCAB_SIZE)
        self.encoder.adapt(self.train_dataset.map(lambda text, label: text))

        vocab = np.array(self.encoder.get_vocabulary())
        print(vocab[:20])

        encoded_example = self.encoder(example)[:3].numpy()
        print(encoded_example)

        for n in range(3):
            print("Original: ", example[n].numpy())
            print("Round-trip: ", " ".join(vocab[encoded_example[n]]))
            print()
    
    def two_layers_model_creation(self):
        self.model = tf.keras.Sequential([
        self.encoder,
        tf.keras.layers.Embedding(len(self.encoder.get_vocabulary()), 64, mask_zero=True),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64,  return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(1)
        ])
    def two_layers_model_compile(self):
        self.model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                optimizer=tf.keras.optimizers.Adam(1e-4),
                metrics=['accuracy'])

    def two_layers_model_train(self):
        history = self.model.fit(self.train_dataset, epochs=10,
                        validation_data=self.test_dataset,
                        validation_steps=30)
        test_loss, test_acc = self.model.evaluate(self.test_dataset)
        print('Test Loss:', test_loss)
        print('Test Accuracy:', test_acc)
    
    def define_model(self):
        self.input_pipeline()
        self.two_layers_model_creation()
        self.two_layers_model_compile()
        self.two_layers_model_train()
        self.save_trained_model()

    def save_trained_model(self):
        # Save the Modle to file in the current working directory
        tf.keras.models.save_model(self.model,'trained_model/rnn_trained_model')

    def load_trained_model(self):
        # Load the Model back from file
        self.trained_model = tf.keras.models.load_model('trained_model/rnn_trained_model')


    def two_layers_model_prediction(self, text):
        self.load_trained_model()
        # predict on a sample text without padding.
        prediction = self.trained_model.predict(np.array([text]))
        return prediction