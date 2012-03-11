__author__ = 'jon'

class Parser(object):
    """
      Defines parser interface for parsing log files from the log directory
    """


    def __init__(self):
        self.logDirectoryPath = '../../log'


    def parse(self):
        """
          Returns a list of dictionaries, representing the entries of the parsed log
        """
        raise NotImplementedError("Implement 'parse' in concrete subclass!")


    def summarize(self):
        """
          Returns a dictionary describing/summarizing the log format, with the list of constants possible for each entry
            or 'None' type for entries that contain arbitrary values.
        """
        raise NotImplementedError("Implement 'summarize' in concrete subclass!")
