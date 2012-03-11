Nimbos
======
Prediction framework for Hadoop clusters

# Project structre
  * <tt>/log</tt> contains the log files to parse, see parsers for expected format
  * <tt>/src</tt> contains all project source code
  ** <tt>/src/parser</tt> contains parsers for log files
  ** <tt>/src/strategy</tt> contains learning algorithm strategies for common log components
  * <tt>/test</tt> contains all automated tests

Run <code>./cleanup.sh</code> to remove all compiled Python code if desired.