## NLP Lecture 1, 1-19-2022

---

### Linguistics
#### Morphology
 - structure of words
 - morphemes
   - a part of a word. Like quarks for words

#### Syntax
 - think the structure of sentences
 - "I saw the man with the telescope". Either the man or the person saying the sentence could have the telescope. Syntax impacts interpretation.

#### Semantics
 - The study of meaning
 - Can help remove some of the ambiguity from syntax
 - "word sense" words can have multiple meanings. Celebrity homonym.

#### Prosody
 - Tone contours in spoken language
  - "thanks a lot" vs. "thanks a lot" (genuine vs. sarcastic)

#### Pragmatics
 - Social context 

---

### REGEX

Pattern to search strings
 - Book uses `/ /` to mean regular expression
 - `/a/` matches `a` as in bl*a*h
 - `/la/` matches `la` as in b*la*h
 - `/./` matches any character as in *b*lah (if first match used)
 - `/[ab]/` matches any one of what is inside square brackets as in `a or b` ex.: *b*lah
 - `/[a-z]/` any character `a` through `z` ex.: *b*lah
 - `/[aeiou]/` matches any vowel
 - `/[^ab]/` matches any character not a or b b*l*ah
 
#### REGEX flow
Build a pattern -> compile pattern -> pattern object -> methods
 - `.match(string)` -> Match pattern at start of string
 - `.search(string)` -> Match pattern, search starting at index 0 of string
 - `.fullmatch(string)` -> Only matches if pattern matches the full string



