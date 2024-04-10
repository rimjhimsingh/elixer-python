# elixer-python
Here we use regular expressions to implement a trivial scanner and implement a recursive-descent parser for a small language.

## Project Structure
elixir-data.ebnf: EBNF grammar of the language.

make.sh: Script to build the project (if necessary).

run.sh: Script to run the parser.

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

### The JSON representation of the different kind of literals should be as follows:

An integer has the JSON representation { "%k": "int", "%v": value } where value is a JSON integer respresenting the value of the integer. For example, the integer 123 should have the JSON representation { "%k": "int", "%v": 123 }.

An atom has the JSON representation { "%k": "atom", "%v": value } where value is a JSON string spelling out the atom. For example, the atom :_a32 should have the JSON representation { "%k": "atom", "%v": ":_a32" }.

A boolean has the JSON representation { "%k": "bool", "%v": value } where value is a JSON boolean representing the value of the boolean. For example, the boolean true should have the JSON representation { "%k": "bool", "%v": true }.

A key has the JSON representation { "%k": "atom", "%v": value } where value is a JSON string spelling out the key lexeme, but with the : moved to the front. For example, the key abc: should have the JSON representation { "%k": "atom", "%v": ":abc" }.

A list has the JSON representation { "%k": "list", "%v": value } where value is a JSON list containing the JSON representations of the individual items in the list. For example, the list [ 1, 2 ] should have the JSON representation:

	{ "%k": "list",
	  "%v": [
	     { "%k": "int", "%v": 1 },
	     { "%k": "int", "%v": 2 }
	  ]
	}
A tuple has the JSON representation { "%k": "tuple", "%v": value } where value is a JSON list containing the JSON representations of the individual items in the tuple. For example, the tuple { 1, :k } should have the JSON representation:

	{ "%k": "tuple",
	  "%v": [
	     { "%k": "int", "%v": 1 },
	     { "%k": "atom", "%v": ":k" }
	  ]
	}
A map has the JSON representation { "%k": "map", "%v": value } where value is a JSON list containing the 2-element JSON lists representing the individual elements in the map. For example, the map %{ :a => 22, b: 33 } should have the JSON representation:

	{ "%k": "map",
	  "%v": [
	     [ { "%k": "atom", "%v": ":a" },
	       { "%k": "int", "%v": 22 }
	     ],
	     [ { "%k": "atom", "%v": ":b" },
	       { "%k": "int", "%v": 33 }
	     ]
	  ]
	}
