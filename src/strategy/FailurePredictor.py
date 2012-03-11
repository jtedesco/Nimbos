__author__ = 'jon'

class FailurePredictor(object):
    """
      Acts as an interface for machine learning strategies to be used on log data for failure prediction. The interface
        expects users to add all learning examples before running the learning algorithm.
    """

    def __init__(self, model):
        """
          Constructs a prediction strategy object, containing empty example dictionary
        """

        super(FailurePredictor, self).__init__()

        # The training examples for the model
        self.examples = {}

        # The learning model
        self.model = model
        self.trainedModel = False


    def addLearningExample(self, features, value):
        """
          Provides an interface to add a learning example and its label or value to the body of learning examples.
            @param  features    The features of the learning example, given as a tuple (so that it is hashable)
            @param  value       The label or value associated with this example
        """

        self.examples[features] = value


    def removeLearningExample(self, features):
        """
          Provides an interface to remove a learning example and its label or value from the body of learning examples.
            @param  features    The features of the learning example, given as a tuple (so that it is hashable)
        """

        del self.examples[features]


    def train(self):
        """
          Use the learning algorithm associated with this object on the set of learning examples
        """

        # Train the model & mark it as trained
        self.model.train(self.examples)
        self.trainedModel = True


    def predict(self, features):
        """
          Use the presumably learned model to predict the label or value of a given set of features
            @param  features    The features of the example for which to predict the value or label
        """

        if self.trainedModel:
            return self.model.predict(features)
        else:
            raise NotImplementedError('Must train learning model before attempting to predict label or value!')
