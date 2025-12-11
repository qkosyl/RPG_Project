'''
namespaces
In Python a namespace is the place where a variable is stored.
Namespaces are implemented as dictionaries, where keys are the object names,
and the values are the objects themselves.

Types
built in - The built-in namespace contains the names of all of Python's built-in objects.
Global - The global namespaces contain names at the level of the main program.
Enclosing -
Enclosed Namespace
The enclosed namespace includes names defined inside an outer function.
local
The local namespace includes local names inside a function.


built-in functions = built-in namespace
V
imported Module = global namespace
V
enclosing level
V
local function = local namespace

A scope, in comparison, defines which namespaces will be
looked in and in what order. The scope of any reference
always starts in the local namespace and moves outwards
until it reaches the module's global namespace before
moving on to the built-ins, which is the last level of namespaces.

A namespace is a dictionary for mapping symbolic names
to their values. When you do any assignment, you are,
in fact, updating a namespace dictionary. When you refer
to an object by its name, Python looks through a list
of several namespaces trying to find one
with the name as a key.


locals() -> w funckji pokaze wszystkie variable dostepne
globals() -> pierdoli globalne z poziomu zwyklego
odplajac locals() w zwyklym wpierdala te globalne

def outer_function(msg):
        message = msg

        def inner_function():
            print(message)

        return inner_function

my_function = outer_function('Hi!')
my_function()
Hi!

def function_with_counter():
        count = 1
        dupa = 1
        def some_function(msg):
            nonlocal count
            nonlocal dupa
            count *= 2
            dupa += 1
            print(f'{count:4}: {msg} dupa {dupa}')

        return some_function

print_with_counter = function_with_counter()
print_with_counter('Hello')
print_with_counter('I count my calls')
print_with_counter('I count my calls')

DEKORATORY
def decorator_function(func):
    def wrapper():
        func() -> przykladowo print("add sprinkles") /
        func() -> jest też funkcją która została używa w głównej przykladowo w get_icecrea()
       wtedy parametrem dla dekoratora jest (func)
    return wrapper
@decorator_function
def get_icecream():
    print("here is your icecream")

get_icecream() -> tutaj zostanie dodany dekorator

Wrapper jest po to aby nie było sytuacji w ktorej korzystamy z funkcji decoratora
a odpala również funkcje niedekoracyjną

wrappery i func potrzebują *args, **kwargs inaczej wywali program bo get_icecream()
podało przykladowo jakis parametr

'''
from typing import Dict
import time

execution_time: Dict[str, float] = {}


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        calc_time = end_time - start_time
        execution_time[func.__name__] = calc_time
        return result
    return wrapper


@time_decorator
def func_add(a, b):
    time.sleep(0.2)
    return a + b

func_add(1,2)
print(execution_time)