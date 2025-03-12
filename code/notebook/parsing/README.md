# notebook.parsing

This module features closely related recursive descent Tokenizer and Parser classes sharing instances of the Token named tuple.

The general design of the tokenizers and parsers is loosely based on the book "Crafting Interpreters" by Robert Nystrom. Some features like contexts and error highlighting are home-baked. Many other differences stem from Python performance considerations.
