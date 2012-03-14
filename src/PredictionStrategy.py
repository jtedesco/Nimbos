__author__ = 'jon'

class PredictionStrategy(object):
    """
      Abstract class for failure prediction learning strategies.
    """

    def parseData(self, data):
        """
          Parse training examples from training data
            @param  data    Some arbitrary training data
        """

        raise NotImplementedError("Cannot call 'parseTrainingData' on an abstract strategy object!")


    def learn(self, examples):
        """
          Train the strategy based on some training examples.
            @param  examples    Training examples, structured as a dictionary features -> label/value
        """

        raise NotImplementedError("Cannot call 'train' on an abstract strategy object!")


    def predict(self, features):
        """
          Predict the label or class of some set of features.
            @param  features    The set of features to predict
        """

        raise NotImplementedError("Cannot call 'predict' on an abstract strategy object!")


    def loadModel(self, modelFilePath):
        """
          Load a learned classification or regression model file, given its location on disk.
        """

        self.modelFileName = modelFilePath

        modelFile = open(self.modelFileName)
        self.model = modelFile.read()
        modelFile.close()
