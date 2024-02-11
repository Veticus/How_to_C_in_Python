# How to use C libraries with python using CFFI
tl;dr is at the bottom of this file.

While taking a ML course i was asked how Python libraries like `sklearn` and `TensorFlow` 
can use C libraries to be so fast, without having to translate the Python code into C and then 
compiling the whole thing.

The "magic" is in a concept called Foreign Function Interfacing.
Here's a quick demo i showed the two who asked.

NOTE: The example library in this repo is compiled for MacOS. 
So this example might not work "click-and-run" on other OS.

## Part 1: The C stuff
For this demo we'll just implement a function that multiplies two numbers.

### The C code
Here's some quick, and probably dirty, C code that does the multiplication for us.
```c
#include <stdio.h>

double multiply(double a, double b) {
	return a * b;
}
```
We'll put this into the `mult.c` file.

### Compiling the C code into a library
To compile it on MacOS we can use GCC like this:
```bash
gcc -dynamiclib -o libmult.dylib mult.c
```
On Linux we can do something very similar:
```bash
gcc -shared -o libmult.so -fPIC mult.c
```

Note: using the ".dylib" suffix in the filename is "just convention" on macos.
For Linux the convention is ".so" and for windows it's ".dll" (i think - i don't do windows).
But this is just convention. Pretty much any filename will work.

#### Extra note for windows users
If i recall right, you'll need to first create an object file, 
and then create the .dll file you need separately.

I don't have the patience or means to test it, but i've noted these two steps
```batch
gcc -c -fPIC mult.c -o mult.o
gcc -shared -o mult.dll mult.o
```
Windows things aren't of interest to me, so you may find a better way to do this.

## 2: The Python stuff
For this example we'll use a library called cffi, which makes this all a lot easier, safer, better and faster.
All Python code will be in the same file. For this demo i'll call it `main.py`.

### Installing cffi
To install it we simply run `pip install cffi`. 
Remember the good/best practice of doing this in a fresh venv.

### Importing cffi and creating an instance of `FFI`
As usual we import FFI from the cffi package at the top of the `main.py` file.
And, as with many libraries, we then create an instance of FFI.
```python
from cffi import FFI

ffi = FFI()
```

### Defining the signature of the C function
cffi needs to know which function to expect in our C library.
cffi makes this very easy, because we simply add this line to our `main.py` file.
```python
ffi.cdef("double multiply(double, double);")
```
#### Quick note on getting the types right
If you define the wrong data types here, you'll get some weird results,
which can lead to some tricky debugging.
With this example, if you define the function as `"int multiply(int, int);"`, and then
call it with 6 and 7 as parameters, you'll get the number 6 as a result - instead of the expected 42.

### Loading the library
Next we'll load the library with a reference, which we can use to call our `mult()` function.
Again, cffi makes this very easy for us like this:
```python
lib = ffi.dlopen("./libmult.dylib")
```
For Linux and Windows just use the appropriate filename.
Make sure you get the path to the file right.

### Using the function
Finally we can use the function like this:
```python
fancyresult = lib.multiply(6.5, 2)
print(f"My fancy C library says that 6.5 times 2 equals {fancyresult}")
```

Now just run the `main.py` file.
Tadaaaaa



# tl;dr - Shut up and give me the code
## C file
```c
#include <stdio.h>

double multiply(double a, double b) {
	return a * b;
}
```

## Compile
| OS      | Command                                   |
|---------|-------------------------------------------|
| MacOS   | `gcc -dynamiclib -o libmult.dylib mult.c` | 
| Linux   | `gcc -shared -o libmult.so -fPIC mult.c`  |
| Windows | `gcc -c -fPIC mult.c -o mult.o`           |
|         | `gcc -shared -o mult.dll mult.o`          |

## Python file
```python
from cffi import FFI

ffi = FFI()
ffi.cdef("double multiply(double, double);")

lib = ffi.dlopen('./libmult.so')  # Make sure to have the right file name and path

result = lib.multiply(6.5, 7.2)
print(f"The result is: {result}")
```
