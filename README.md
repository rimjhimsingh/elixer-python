# elixer-python
Here we use regular expressions to implement a trivial scanner and implement a recursive-descent parser for a small language.

### Useful definitions to know:
A sentence in the language consists of a sequence of zero-or-more data-literal's.

A data-literal is either a list literal, a tuple literal, a map literal, or a primitive literal.

A primitive literal is either an integer, atom or boolean.

A list literal is a sequence of 0-or-more comma-separated data-literal's within square brackets [ and ].

A tuple literal is a sequence of 0-or-more comma-separated data-literal's within braces { and }.

A map literal is a sequence of 0-or-more comma-separated key-pair's within a decorated left brace %{ and a regular right brace }.

A key-pair is either a sequence consisting of a data-literal, a right-arrow => followed by a data-literal, or a sequence consisting of a key followed by a data-literal.

An integer consists of a sequence of one-or-more digits, possibly containing internal underscores _.

An atom consists of a colon :, followed by an alphabetic character or underscore _ followed by a sequence of zero-or-more alphanumeric characters or underscores _.

A key is just like an atom but the : must be at the end instead of the start.

A boolean is one of the words true or false.
