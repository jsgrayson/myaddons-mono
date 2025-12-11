import re

class SLPP:
    def __init__(self):
        self.text = ''
        self.ch = ''
        self.at = 0
        self.len = 0
        self.depth = 0
        self.space = re.compile(r'\s', re.M)
        self.alnum = re.compile(r'\w', re.M)
        self.newline = '\n'
        self.tab = '\t'

    def decode(self, text):
        if not text or not isinstance(text, str):
            return
        # Remove comments
        text = re.sub(r'--.*$', '', text, flags=re.M)
        self.text = text
        self.at = 0
        self.len = len(text)
        self.depth = 0
        self.next()
        result = self.value()
        return result

    def next(self):
        if self.at >= self.len:
            self.ch = None
            return None
        self.ch = self.text[self.at]
        self.at += 1
        return self.ch

    def value(self):
        self.white()
        if not self.ch:
            return
        if self.ch == '{':
            return self.object()
        if self.ch == '[':
            self.next()
        if self.ch in ['"', "'", '[']:
            return self.string()
        if self.ch.isdigit() or self.ch == '-':
            return self.number()
        return self.word()

    def white(self):
        while self.ch and self.space.match(self.ch):
            self.next()

    def object(self):
        o = {}
        k = None
        idx = 0
        numeric_keys = False
        self.depth += 1
        self.next()
        self.white()
        if self.ch and self.ch == '}':
            self.depth -= 1
            self.next()
            return o # Empty dict
        while self.ch:
            self.white()
            if self.ch == '{':
                v = self.object()
                if k:
                    o[k] = v
                    k = None
                else:
                    # Array item
                    o[idx] = v
                    idx += 1
                    numeric_keys = True
            elif self.ch == '}':
                self.depth -= 1
                self.next()
                if numeric_keys and not any(isinstance(x, str) for x in o.keys()):
                    # Convert to list if all keys are integers 0..N
                    # Lua arrays are 1-based, but we used 0-based idx.
                    # Actually Lua mixed tables are complex.
                    # For simplicity: if we have keys 0, 1, 2... return list values
                    return list(o.values())
                return o
            else:
                if self.ch == '[':
                    self.next()
                    k = self.value()
                    self.white()
                    if self.ch == ']':
                        self.next()
                    self.white()
                    if self.ch == '=':
                        self.next()
                        v = self.value()
                        o[k] = v
                        k = None
                else:
                    # Unquoted key or value
                    val = self.value()
                    self.white()
                    if self.ch == '=':
                        self.next()
                        k = val
                        v = self.value()
                        o[k] = v
                        k = None
                    else:
                        if k:
                            o[k] = val
                            k = None
                        else:
                            # Array item
                            o[idx] = val
                            idx += 1
                            numeric_keys = True
            self.white()
            if self.ch == ',':
                self.next()
                self.white()
            elif self.ch == ';': # Lua allows ; separator
                self.next()
                self.white()
    
    def word(self):
        s = ''
        if self.ch != None:
            s = self.ch
        self.next()
        while self.ch is not None and self.alnum.match(self.ch) and self.ch != '_':
            s += self.ch
            self.next()
        
        # Handle booleans/nil
        if s == 'true': return True
        if s == 'false': return False
        if s == 'nil': return None
        return s

    def number(self):
        n = ''
        if self.ch == '-':
            n += '-'
            self.next()
        while self.ch and (self.ch.isdigit() or self.ch == '.'):
            n += self.ch
            self.next()
        try:
            return int(n)
        except:
            try:
                return float(n)
            except:
                return 0

    def string(self):
        quote = self.ch
        if quote == '[':
            # Handle [[ string ]]
            self.next() # skip [
            start = self.at
            end = self.text.find(']]', start)
            if end == -1: return ""
            s = self.text[start:end]
            self.at = end + 2
            self.next() # skip ]
            self.next() # skip ]
            return s
        
        self.next()
        s = ''
        while self.ch and self.ch != quote:
            if self.ch == '\\':
                self.next()
                if self.ch == 'n': s += '\n'
                elif self.ch == 't': s += '\t'
                else: s += self.ch
            else:
                s += self.ch
            self.next()
        self.next()
        return s

def decode(text):
    parser = SLPP()
    return parser.decode(text)
