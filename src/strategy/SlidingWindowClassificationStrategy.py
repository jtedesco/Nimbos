import os
import subprocess
from src.strategy.SlidingWindowStrategy import SlidingWindowStrategy

__author__ = 'jon'


class SlidingWindowClassificationStrategy(SlidingWindowStrategy):
    """
      Abstracts away functionality related to running the SVM classifier for all sliding window classification strategies.
    """

    def learn(self, examples):
        """
          Trains SVM light based on the given training examples. Assumes all training examples are in the proper format.

            @param  examples    The training examples, given in the training data format, where each entry is a tuple of
                                event severity counts for each sub-window, followed by T/F based on whether or not the
                                last window had a fatal event
        """

        # Throw an exception if the 'scratch' training file already exists
        if os.path.exists(self.trainingFileName):
            raise IOError('Error training SlidingWindowClassificationStrategy strategy: %s already exists!' % self.trainingFileName)

        # Remove the model file if it already exists
        if os.path.exists(self.modelFileName):
            print "Removing SVM model file '%s'" % self.modelFileName
            os.remove(self.modelFileName)


        # Build the training file
        trainingFileContent = self.buildDataFileContent(examples)
        trainingFile = open(self.trainingFileName, 'w')
        trainingFile.write(trainingFileContent)
        trainingFile.close()

        # Train a model based on the training file
        subprocess.call('svm_learn "' + self.trainingFileName + '" "' + self.modelFileName + '"', shell=True)

        # Read the learned model and store the string
        modelFile = open(self.modelFileName)
        self.model = modelFile.read()
        modelFile.close()

        # Cleanup
        os.remove(self.trainingFileName)
        os.remove(self.modelFileName)

        # Return the model
        return self.model


    def predict(self, data):
        """
          Uses SVM light to predict the classification for the given features

            @param   data   The data entry to classify, given as a list of data entries in training example format
            @return A list of True/False, each entry representing the prediction for whether or not the next window will
                    have a FATAL error (corresponding to entries in the data)
        """

        # Throw an exception if the 'scratch' training and/or test files already exist
        if os.path.exists(self.predictionsInputFileName):
            raise IOError(
                'Error predicting with SlidingWindowClassificationStrategy strategy: %s already exists!' % self.predictionsInputFileName)
        if os.path.exists(self.predictionsOutputFileName):
            raise IOError(
                'Error predicting SlidingWindowClassificationStrategy strategy: %s already exists!' % self.predictionsOutputFileName)

        # Write the model file if it doesn't already exist
        if not os.path.exists(self.modelFileName):
            modelFile = open(self.modelFileName, 'w')
            modelFile.write(self.model)
            modelFile.close()


        # Create the predictions input file (test data)
        predictionsInputFileContent = self.buildDataFileContent(data)
        predictionsInputFile = open(self.predictionsInputFileName, 'w')
        predictionsInputFile.write(predictionsInputFileContent)
        predictionsInputFile.close()


        # Use SVM light to predict classifications for all data entries
        subprocess.call('svm_classify "' + self.predictionsInputFileName + '" "' + self.modelFileName + '" "' +
                        self.predictionsOutputFileName + '"', shell=True)

        # Cleanup
        os.remove(self.predictionsInputFileName)

        return None

