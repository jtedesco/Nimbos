__author__ = 'jon'

class PredictionStrategy(object):
    """
      Abstract class for failure prediction learning strategies.
    """

    def parseTrainingData(self, data):
        """
          Parse training examples from training data
            @param  data    Some arbitrary training data
        """

        raise NotImplementedError("Cannot call 'train', LearningStrategy is abstract!")


    def train(self, examples):
        """
          Train the strategy based on some training examples.
            @param  examples    Training examples, structured as a dictionary features -> label/value
        """

        raise NotImplementedError("Cannot call 'train', LearningStrategy is abstract!")


    def predict(self, features):
        """
          Predict the label or class of some set of features.
            @param  features    The set of features to predict
        """

        raise NotImplementedError("Cannot call 'predict', LearningStrategy is abstract!")
