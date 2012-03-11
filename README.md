Nimbos
======
Prediction framework for Hadoop clusters

## Project structure
  * <code>/log</code> contains the log files to parse, see parsers for expected format
  * <code>/src</code> contains all project source code
    * <code>/src/parser</code> contains parsers for log files
    * <code>/src/strategy</code> contains learning algorithm strategies for common log components
  * <code>/test</code> contains all automated tests

Run <code>./cleanup.sh</code> to remove all compiled Python code if desired.