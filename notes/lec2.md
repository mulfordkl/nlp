## NLP Lecture 2, 1-24-2022

---

### More REGEX

#### Anchors

 - `^` start of string
 - `$` end of string

#### Counting operators

Normally these apply only to the character that it is bound to. If you want to use the counting operators to match several characters at a time, use groupings.
 
 - `a?` 0 or 1 occurrence of `a`
 - `a*` 0 or more
 - `a+` 1 or more
 - `a | b` matches `a` or `b`. Output can be unexpected with multiple groupings. Usage: `(ab)|(cd)`
 - `{m,n}` repeats `m` to `n` times, if either are left off it is 'up to' or 'at least', respectively.

Counting operators are all **greedy** and will match as much as possible.
Parentheses are used for grouping

 - `(abc)?` matches `abc` or nothing. This is true for `?`, `*`, or `+`
 - `bl?ah` matches something that has `b` - any number of `l` - and then `ah` as in *blah*
 - `[a-z]+` matches 1 or more of any letter
 - `[a-z]*` matches any lower case string, including the empty string

#### Some examples

Using `string.fullmatch`

 - Write a regex that will match any string that begins in a and ends in b 
   - `/a.*b/`
 - Any string that begins with a capital letter and ends with a lowercase letter
   - `/[A-Z].*[a-z]/`
 - Any string that has in it a q not followed by a u
   - `/.*q[^u].*/` this produces a FN for `'abq'`. Improve it with `/.*q([^u].*)|$/`
 - Any string that contains a consonant cluster of length > 3
   - `/[^aeiou][^aeiou][^aeiou]+/` - includes all non letter characters
   - Can also do this with the counting operator `{m,n}`
   - Correct: `/.*[b-df-hj-np-tv-z]{3,}].*/`
 - Any string that contains a word that doesn't contain a vowel
   - `//`