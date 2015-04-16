# How It Works #

The java\_to\_python script works as follows:

  1. given input file (or stdin) is read and passed to a lexer and parser
  1. parser generates an AST
  1. AST is passed to tree walker
  1. tree walker walks the AST, calling code to build a Source object
  1. Source object is written to output file (or stdout)

Each of these is explained further below.

1.  Input Read, Lexed, and Parsed

2.  Parser Generates AST

3.  AST Passed to Tree Walker

4.  Tree Walker Walks AST to Build Source Object

5.  Source Object Written to Output