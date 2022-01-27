## NLP Lecture 3, 1-26-2022

---

#### Capturing Groups

The idea with capturing groups is whenever you use parenthesese as part of the regular expression pattern - it allows you to easily pull out what was in those parenthesis. 

Imagine we are looking for words that are preceded by "an":
 - We can use a capturing group to find the whole expression "an ____" but then only capture the word of interest. One example for this is `/\b[Aa]n ([^ ]*)\b/`. The `/b` is a shortcut for a word boundary.
 - `re.search()` returns a match object.
   - group 0 - entire match
   - group 1 - 1st capturing group
   - group 2 - 2nd capturing group
 - If we wanted to look for "to ___ or not to ___":
   - `/\bto ([^ ]*) or not to \1\b/`

A simple program to illustrate regex capturing groups and rawstrings

```python
import re

def re_examples(searchstring, regex):
    pattern = re.compile(regex)
    mo_match = pattern.match(searchstring)
    print(".match():   " + str(mo_match))
    mo_search = pattern.search(searchstring)
    print(".search():   " + str(mo_search))
    mo_fullmatch = pattern.fullmatch(searchstring)
    print(".match():   " + str(mo_fullmatch))
    liststr_findall = pattern.findall(searchstring)
    print(".fndall():   " + str(liststr_findall))

def main():
    to_search = """ hi! an apple a day keeps the doctor away.
                to be or not to be, that is the question.
                here is another line of text.
                is this an exaple that is useful? """

    re_example(to_search, '[Aa]n ([^ ]*'))
    ## You need to add an r here so python can interpret the escape characters
    re_example(to_search, r'\bto ([^ ]*) or not to \1\b')

if __name__ == '__main__':
    main()

```

#### Substitution

`re.sub(pattern, replacement, string)`

Replacement string can include backrefs to capturing groups `\1` or `\2`

### Finite State Automata

An FSA is a model of computation that can accept or reject a string.

Definitions:
 - Q: Finite set of states
 - Sigma: Input alphabet - finite set of symbols
 - q: start state
 - F: final states F<=Q
 - delta(q,i): transition function
   - Q x Sigma --> Q


Let's build an automata that accepts strings that begin with b and end with a

`sigma: {a,b}`

FSA that accepts strings that do not contain `aa`

q3 is a dump state
q1, q2 are final states

```
q0  a-> q1  a-> q3 <-a
                   <-b
            b-> q2
    b-> q2  a-> q1
            b-> q2
```

FSA that accepts strings containing 'aba'

q4 is final accept state
q1,2,3 are final reject states


```
q0  a-> q1  b-> q3  a->q4   <-a
                            <-b
                    b->q2
            a-> q1
    b-> q2  a-> q1
            b-> q2
```

**Regular Language**
FSA accepting rejecting = REGEX(minus capturing groups) Full Match