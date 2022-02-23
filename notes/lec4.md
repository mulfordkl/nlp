## NLP Lecture 4, 1-31-2022

---

### Regular Languages

1. The null set is a regular language
2. Any single letter is a regular language
3. If L1 and L2 are regular languages, then we can combine them to form another regular language. 
    - Concatenation of L1 and L2
    - Union of L1 and L2
    - L1* (0 or more repititions of something in L1)

What is NOT a regular language?

 - a^n^b^n^
   - You would need something that can count (aka have a memory)
   - FSA do not have memory

---

### Morphological Parsing

America**n**, America**ns**, Americ**a**

Stems - *root word* 

**Affixes**
 - Prefix
   - *Un*believable
 - Suffix
   - Runn*ing*
 - Infixes
   - Intensifiers
     - Unfuckingbelievable
   - These usually go before the stressed syllable
 - Circumfixes
   - Not in English (german thing)
   - Put something on the front and the back of the verb

#### Types
 - Inflectional
   - Stem + Affix
   - Affix is a grammatical morpheme
   - Usually results in a word of the same class with added grammatical meaning



   