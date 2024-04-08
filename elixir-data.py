############LEXER################

import re
from collections import namedtuple
import sys
import json

# Regular expressions for different token types
SKIP_RE = re.compile(r'(( |\t|\n)|\#.*)+')
INT_RE = re.compile(r'\d+(\_\d+)*')
ATOM_RE = re.compile(r':[a-zA-Z_][a-zA-Z0-9_]*')
BOOL_RE = re.compile(r'\b(true|false)\b')
LIST_OP_RE = re.compile(r'\[')
LIST_CL_RE = re.compile(r'\]')
TUPLE_OP_RE = re.compile(r'\{')
TUPLE_CL_RE = re.compile(r'\}')
COLON_RE = re.compile(r':')
MAP_OP_RE = re.compile(r'%\{')
KEY_RE = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*:')
COMMA_RE = re.compile(r',+')
ARROW_RE = re.compile(r'=>')

# Define the token named tuple
Token = namedtuple('Token', 'kind lexeme pos')

# Tokenizer function
def tokenize(text, pos=0):
    toks = []
    while pos < len(text):
        m = SKIP_RE.match(text, pos)
        if m:
            pos += len(m.group())  # Skip whitespace and comments

        if pos>=len(text):break

        if m := INT_RE.match(text, pos):
            tok = Token('INT', m.group(), pos)
        elif m := BOOL_RE.match(text, pos):
            tok = Token('BOOL', m.group(), pos)
        elif m := ATOM_RE.match(text, pos):
            tok = Token('ATOM', m.group(), pos)
        elif m := LIST_OP_RE.match(text, pos):
            tok = Token('LO', m.group(), pos)
        elif m := LIST_CL_RE.match(text, pos):
            tok = Token('LC', m.group(), pos)
        elif m := COMMA_RE.match(text, pos):
            tok = Token('COMMA', m.group(), pos)
        elif m := TUPLE_OP_RE.match(text, pos):
            tok = Token('TUPLE_O', m.group(), pos)
        elif m := TUPLE_CL_RE.match(text, pos):
            tok = Token('TUPLE_C', m.group(), pos)
        elif m := MAP_OP_RE.match(text, pos):
            tok = Token('MAP_OP', m.group(), pos)
        elif m := ARROW_RE.match(text, pos):
            tok = Token('ARROW', m.group(), pos)
        elif m := COLON_RE.match(text, pos):
            tok = Token('COLON', m.group(), pos)
        elif m := KEY_RE.match(text, pos):
            tok = Token('KEY', m.group(), pos)
        
        else:
            # If no regex matches, consider it a single character token
            tok = Token(text[pos], text[pos], pos)
            print(tok)
        pos += len(tok.lexeme)
        toks.append(tok)

    toks.append(Token('EOF', '<EOF>', pos))  # Append EOF token at the end
    return toks


###PARSER####

def parse(text):
    toks = tokenize(text)
    toksIndex = 0
    tok = toks[toksIndex]
    toksIndex += 1

    def sentence(asts):
        while not peek('EOF'):
            dl = data_literal()
            asts.append(dl)
        return asts
    
    
    def data_literal():
        if peek('INT'):
            return integer()
        elif peek('ATOM') or peek('KEY'):
            return atom()
        elif peek('BOOL'):
            return boolean()
        elif peek('LO'):
            return list_literal()
        elif peek('TUPLE_O'):
            return tuple_literal()
        elif peek('MAP_OP'):
            return map_literal()
        else:
            error('data literal', text)

    def integer():
        value = tok.lexeme
        kind = tok.kind
        consume(kind)
        
        return {"%k": "int", "%v": int(value)}

    def atom():

        value = tok.lexeme
        if(value.endswith(":")):
            value = ":" +value[:-1]
        kind = tok.kind
        consume(kind)
        return {"%k": "atom", "%v": value}

    def boolean():
        value = tok.lexeme
        consume('BOOL')
        return {"%k": "bool", "%v": True if value == 'true' else False}

    def list_literal():
        consume('LO')
        items = []
        while not peek('LC'):
            items.append(data_literal())
            if peek('COMMA') :
                consume('COMMA')
                if peek('LC'):
                    error('data literal', text)
            
        consume('LC')
        return {"%k": "list", "%v": items}
    
    def tuple_literal():
        consume('TUPLE_O')
        items = []
        while not peek('TUPLE_C'):
            items.append(data_literal())
            if peek('COMMA'):
                consume('COMMA')
        consume('TUPLE_C')
        return {"%k": "tuple", "%v": items}
    
    def map_literal():
        consume('MAP_OP')
        pairs = []
        while not peek('TUPLE_C'):
            key = data_literal()
            if peek('ARROW'):
                consume('ARROW')
            elif peek('COLON'):
                consume('COLON')
            value = data_literal()
            pairs.append([key, value])
            if peek('COMMA'):
                consume('COMMA')
        consume('TUPLE_C')
        return {"%k": "map", "%v": pairs}

    def peek(kind):
        nonlocal tok
        return tok.kind == kind

    def consume(kind):
        nonlocal tok, toks, toksIndex
        #print(f"consuming {kind} at {tok}")
        if (peek(kind)):
            tok = toks[toksIndex]
            toksIndex += 1
        else:
            error(kind, text)

    def error(kind, text):
        nonlocal tok
        pos = tok.pos
        if pos >= len(text) or text[pos] == '\n': pos -= 1
        lineBegin = text.rfind('\n', 0, pos)
        if lineBegin < 0: lineBegin = 0
        lineEnd = text.find('\n', pos)
        if lineEnd < 0: lineEnd = len(text)
        line = text[lineBegin:lineEnd]
        print(f"error: expecting '{kind}' but got '{tok.kind}'",
              file=sys.stderr)
        print(line, file=sys.stderr)
        nSpace = pos - lineBegin if pos >= lineBegin else 0
        print('^'.rjust(nSpace+1), file=sys.stderr)
        sys.exit(1)

    asts = [];
    sentence(asts)
    if tok.kind != 'EOF': error('EOF', text)
    return asts
####MAIN#######

def main():
    text = sys.stdin.read()
    #print(tokenize(text))
    asts = parse(text)
    print(json.dumps(asts, separators=(',', ':'))) #no whitespace

if __name__ == "__main__":
    main()