```c
new Person
    it takes food
    its name is "John"
    its age is 25
    its gender is "male"
    its position is 20
    its is_active is true
    fun walks
        takes meters // no `it` for functions
        gives its position + meters

    fun eats
        display "eating {food}" // string interpolation

    fun sleeps
        its is_active is false // Variable value change

    fun died
        its is_active is nothing 


person is Person with "Apple" food
person walks 20 meters // in python person.walk(meters = 20) 
person walks 20 // Also corrent
person eats
person died
display person's is_active

Is it readable?
So; syntax is (simple)

// comment
variable is value
fun name
    takes params // if any
    // return statement uses gives
    gives ...

// call
name arg1, arg2 ...
name arg1 param1, arg2 param2 // Equivalent to name(param=arg)

// Classes
new Class
    it takes params...
    its property is nothing // it = self, 's = . so; self.property = None; nothing means null or none
    its property2 is 10
    its call is its method1 // Same as self.call = self.method1()
    
    fun method1
        gives nothing
    fun method2
        display "Nothing"

object = Class takes args...
object method1
object method2

if condition?
    value....
elif condition?
    value....
else?
    value....
// operators
/*
    '===': 'type', // Type or
    '!==': 'not-type', // Type
    '->': 'in', // Membership :in
    ':>': 'not in', // Membership :in
    '&&': '&', // Bitwise :&&
    '||': '|', // Bitwise :||
    '~~': '~', // Bitwise :~
    '><': '^', // Bitwise
    '&': 'and', // Boolean
    '|': 'or', // Boolean
    '!': 'not', // Boolean
    '=': '==', // Relational
    '~': '!=', // Relational
    '>=' : '>=', // Relational
    '<=' : '<=', // Relational
    '>': '>', // Relational
    '<': '<', // Relational
    '//': '//', // Arithemtic
    '^': '**', // Arithemtic
    '+': '+', // Arithemtic
    '-': '-', // Arithemtic
    '*': '*', // Arithemtic
    '/': '/', // Arithemtic
    '%': '%' // Arithemtic

*/

while codnition?
    ...


/*
You can use skip, break etc
*/
for item -> iterable
    ...

repeat 4
    ...

repeat 4 as i
    ... // you can then use i here

try
    ...
e -> Specific type(s) of error?
    ... you can use e here
finally
    ...

// eg
try
    1/0
e -> ZeroDivisionError KeyError ValueError TypeError?
    dispaly "incorrect"
finally
    display "Code Completed"
```
Some clarifications
- Function call: Always this way:

    ```cpp
    function_name args
    function_name arg param pairs
    function_name // for no param
    // to make no call
    // use
    'function_name'
    ```

- Strings: stirngs are always written in double quotes even multiline.
- nothing means None, absence, logically, it is false. Well, actually, it is same as None in Python.
