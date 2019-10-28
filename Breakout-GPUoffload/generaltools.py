import sys
import json
import base64
import numpy as np
import random
import collections

#region performance evaluation tools
# def test_set(xs):
def check_dup_set(xs):
    seen = set()  # O(1) lookups
    for x in xs:
        if x not in seen:
            seen.add(x)
        else:
            return True

    return False

# def test_counter(xs):
def check_dup_counter(xs):
    freq = collections.Counter(xs)
    for k in freq:
        if freq[k] > 1:
            return True

    return False

# def test_dict(xs):
def check_dup_dict(xs):
    d = {}
    for x in xs:
        if x in d:
            return True
        d[x] = 1

    return False

# def test_sort(xs):
def check_dup_sort(xs):
    ys = sorted(xs)

    for n in range(1, len(xs)):
        if ys[n] == ys[n-1]:
            return True

    return False

def test_performance_eveluation():
    import sys, timeit
    print (sys.version + "\n")
    xs = list(range(10000)) + [999]
    fns = [p for name, p in globals().items() if name.startswith('check_dup')]
    for fn in fns:
        print ('%50s %.5f' % (fn, timeit.timeit(lambda: fn(xs), number=100)))
#endregion


#region General Functions
def sort_dict(dict_param, sort_by_key_param=True, reverse_param=False):
    # NOTE, when sorting by values, values can be duplicated, e.g.
    # x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0, 5: 2}
    # when sorting by value:
    # sorted_x = sorted(x.items(), key=lambda kv: kv[1])
    # output is a list of tuples ordered by values of the original dict:
    # [(0, 0), (2, 1), (1, 2), (5, 2), (4, 3), (3, 4)]
    # when sorting by key:
    # sorted_x = sorted(x.items(), key=lambda kv: kv[0])
    # output is a list of tuples ordered by keys of the original dict:
    # [(0, 0), (1, 2), (2, 1), (3, 4), (4, 3), (5, 2)]
    # by default, sort_by_key_param=True, i.e. sort by key
    # by default, reverse=False, i.e. sort in ascending order
    index = 0   # by default, sort by key
    if sort_by_key_param:
        index = 0
    else :      # otherwise, sort by value
        index = 1
    sorted_dict_param = sorted(dict_param.items(), key=lambda kv: kv[index], reverse=reverse_param)
    return sorted_dict_param


def shuffle_dict(a_dict):
    print('function: {}'.format(sys._getframe().f_code.co_name))

    l = list(a_dict.keys())
    random.shuffle(l)
    shuffled_a_dict = dict()
    for key in l:
        shuffled_a_dict.update({key: a_dict[key]})      # It's ok, dict.update take a copy not a reference

    print('unshuffled_dict = {} \nshuffled_keys = {} \nshuffled_dict={}'.format(
        a_dict, l, shuffled_a_dict))

    print('Exit {} function'.format(sys._getframe().f_code.co_name))
    return shuffled_a_dict


# this function is a deep sorting function sort every level of a json object
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def Base64Encode(nparray):
    return json.dumps([str(nparray.dtype),base64.b64encode(nparray),nparray.shape])


def Base64Decode(jsonDump):
    loaded = json.loads(jsonDump)
    dtype = np.dtype(loaded[0])
    arr = np.frombuffer(base64.decodestring(loaded[1]),dtype)
    if len(loaded) > 2:
        return arr.reshape(loaded[2])
    return arr


def SimpleEncode(nparray_param):
    return json.dumps(nparray_param.tolist())


def SimpleDecode(jsonDump):
    return np.array(json.loads(jsonDump))
#endregion


#region Tree Traversal Classes
#In-order Traversal
'''In this traversal method, the left subtree is visited first, then the root and later the right sub-tree. 
We should always remember that every node may represent a subtree itself.
In the below python program, we use the Node class to create place holders for the root node as well as 
the left and right nodes. Then we create a insert function to add data to the tree. 
Finally the Inorder traversal logic is implemented by creating an empty list and adding the left node 
first followed by the root or parent node. At last the left node is added to complete the Inorder traversal. 
Please note that this process is repeated for each sub-tree until all the nodes are traversed.'''
class Node:
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data
# Insert Node
    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()

# Inorder traversal
# Left -> Root -> Right
    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            res = res + self.inorderTraversal(root.right)
        return res

def test_in_order_traversal_tree():
    # root = Node(27)
    # root.insert(14)
    # root.insert(35)
    # root.insert(10)
    # root.insert(19)
    # root.insert(31)
    # root.insert(42)
    root = Node('annal')
    root.insert('annam')
    root.insert('annas')
    root.insert('annat')
    root.insert('annet')
    root.insert('annex')
    root.insert('annie')
    root.insert('anniv')
    root.insert('annoy')
    root.insert('annot')
    root.insert('annul')
    root.insert('annum')
    root.insert('annus')
    root.insert('ennew')
    root.insert('ennia')
    root.insert('ennoy')
    root.insert('ennui')
    root.insert('inned')
    root.insert('inner')
    root.insert('innet')
    root.insert('unnet')
    root.insert('unnew')
    print('In order traversal tree = {}'.format(root.inorderTraversal(root)))


# Pre-order Traversal
'''In this traversal method, the root node is visited first, then the left subtree and finally the right subtree.
In the below python program, we use the Node class to create place holders for the root node as well as 
the left and right nodes. Then we create a insert function to add data to the tree. 
Finally the Pre-order traversal logic is implemented by creating an empty list and adding the root node 
first followed by the left node. At last the right node is added to complete the Pre-order traversal. 
Please note that this process is repeated for each sub-tree until all the nodes are traversed.'''
class Node:
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data
# Insert Node
    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()

# Preorder traversal
# Root -> Left ->Right
    def PreorderTraversal(self, root):
        res = []
        if root:
            res.append(root.data)
            res = res + self.PreorderTraversal(root.left)
            res = res + self.PreorderTraversal(root.right)
        return res

def test_pre_order_traversal_tree():
    # root = Node(27)
    # root.insert(14)
    # root.insert(35)
    # root.insert(10)
    # root.insert(19)
    # root.insert(31)
    # root.insert(42)
    root = Node('annal')
    root.insert('annam')
    root.insert('annas')
    root.insert('annat')
    root.insert('annet')
    root.insert('annex')
    root.insert('annie')
    root.insert('anniv')
    root.insert('annoy')
    root.insert('annot')
    root.insert('annul')
    root.insert('annum')
    root.insert('annus')
    root.insert('ennew')
    root.insert('ennia')
    root.insert('ennoy')
    root.insert('ennui')
    root.insert('inned')
    root.insert('inner')
    root.insert('innet')
    root.insert('unnet')
    root.insert('unnew')
    print('Pre order traversal tree = {}'.format(root.PreorderTraversal(root)))


# Post-order Traversal
'''In this traversal method, the root node is visited last, hence the name. 
First we traverse the left subtree, then the right subtree and finally the root node.
In the below python program, we use the Node class to create place holders for the root node as well as 
the left and right nodes. Then we create a insert function to add data to the tree. 
Finally the Post-order traversal logic is implemented by creating an empty list and adding the left node 
first followed by the right node. At last the root or parent node is added to complete the Post-order traversal. 
Please note that this process is repeated for each sub-tree until all the nodes are traversed.'''
class Node:
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data
# Insert Node
    def insert(self, data):

        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

# Print the Tree
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()

# Postorder traversal
# Left ->Right -> Root
    def PostorderTraversal(self, root):
        res = []
        if root:
            res = self.PostorderTraversal(root.left)
            res = res + self.PostorderTraversal(root.right)
            res.append(root.data)
        return res

def test_post_order_traversal_tree():
    # root = Node(27)
    # root.insert(14)
    # root.insert(35)
    # root.insert(10)
    # root.insert(19)
    # root.insert(31)
    # root.insert(42)
    root = Node('annal')
    root.insert('annam')
    root.insert('annas')
    root.insert('annat')
    root.insert('annet')
    root.insert('annex')
    root.insert('annie')
    root.insert('anniv')
    root.insert('annoy')
    root.insert('annot')
    root.insert('annul')
    root.insert('annum')
    root.insert('annus')
    root.insert('ennew')
    root.insert('ennia')
    root.insert('ennoy')
    root.insert('ennui')
    root.insert('inned')
    root.insert('inner')
    root.insert('innet')
    root.insert('unnet')
    root.insert('unnew')
    print('Post order traversal tree = {}'.format(root.PostorderTraversal(root)))
#endregion


#region Python Inheritance
'''these are some syntax examples for python inheritance'''
'''!!! IMPORTANT, DO NOT USE (object) in the declaration, 
debug output TypeError, 
probably because we are using python 3.x'''


'''Below is a simple example of inheritance in Python'''
# A Python program to demonstrate inheritance
# Base or Super class. Note object in bracket.
# (Generally, object is made ancestor of all classes)
# In Python 3.x "class Person" is
# equivalent to "class Person(object)"
class Person:    #(object):
    # Constructor
    def __init__(self, name):
        self.name = name

    # To get name
    def getName(self):
        return self.name

    # To check if this person is employee
    def isEmployee(self):
        return False


# Inherited or Sub class (Note Person in bracket)
class Employee(Person):
    # Here we return true
    def isEmployee(self):
        return True

# Test code
def test_inheritance():
    emp = Person("Geek1")  # An Object of Person
    print(emp.getName(), emp.isEmployee())

    emp = Employee("Geek2")  # An Object of Employee
    print(emp.getName(), emp.isEmployee())


'''Subclassing (Calling constructor of parent class).'''
# Eg: class subclass_name (superclass_name):
# Python code to demonstrate how parent constructors
# are called.
# parent class
class Person:    #(object):

    # __init__ is known as the constructor
    def __init__(self, name, idnumber):
        self.name = name
        self.idnumber = idnumber

    def display(self):
        print(self.name)
        print(self.idnumber)


# child class
class Employee(Person):
    def __init__(self, name, idnumber, salary, post):
        self.salary = salary
        self.post = post

        # invoking the __init__ of the parent class
        Person.__init__(self, name, idnumber)

    def display_more(self):
        print(self.name)
        print(self.idnumber)
        print(self.salary)
        print(self.post)


def test_subclassing_1():
    # creation of an object variable or an instance
    a = Person('Rahul-1', 886012)
    b = Employee('Rahul-2', 886012-1, 1000, 'HR')

    # calling a function of the class Person using its instance
    a.display()
    b.display()
    b.display_more()


'''If you forget to invoke the __init__() of the parent class then 
its instance variables would not be available to the child class.
The following code produces an error for the same reason.'''
# Python program to demonstrate error if we
# forget to invoke __init__() of parent.
class A:
    def __init__(self, n='Rahul'):
        self.name = n


class B(A):
    def __init__(self, roll):
        A.__init__(self, 'Addded Correction')# added correction
        self.roll = roll


def test_subclassing_2():
    object = B(23)
    print(object.name)


'''Different forms of Inheritance:
1. Single inheritance: When a child class inherits from only one parent class, 
it is called as single inheritance. We saw an example above. 
2. Multiple inheritance: When a child class inherits from multiple parent classes, 
it is called as multiple inheritance.
Unlike Java and like C++, Python supports multiple inheritance. 
We specify all parent classes as comma separated list in bracket.'''
# Python example to show working of multiple
# inheritance
class Base1:     #(object):
    def __init__(self):
        self.str1 = "Geek1"
        print("Base1")


class Base2:    #(object):
    def __init__(self):
        self.str2 = "Geek2"
        print("Base2")


class Derived(Base1, Base2):
    def __init__(self):
        # Calling constructors of Base1
        # and Base2 classes
        Base1.__init__(self)
        Base2.__init__(self)
        print("Derived")

    def printStrs(self):
        print(self.str1, self.str2)


def test_derived_class():
    ob = Derived()
    ob.printStrs()


'''3. Multilevel inheritance: When we have child and grand child relationship.'''
# A Python program to demonstrate inheritance
# Base or Super class. Note object in bracket.
# (Generally, object is made ancestor of all classes)
# In Python 3.x "class Person" is
# equivalent to "class Person(object)"
class Base:         #(object):

    # Constructor
    def __init__(self, name):
        self.name = name

    # To get name
    def getName(self):
        return self.name


# Inherited or Sub class (Note Person in bracket)
class Child(Base):

    # Constructor
    def __init__(self, name, age):
        Base.__init__(self, name)
        self.age = age

    # To get name
    def getAge(self):
        return self.age


# Inherited or Sub class (Note Person in bracket)
class GrandChild(Child):

    # Constructor
    def __init__(self, name, age, address):
        Child.__init__(self, name, age)
        self.address = address

    # To get address
    def getAddress(self):
        return self.address


def test_inherited_class():
    # Driver code
    g = GrandChild("Geek1", 23, "Noida")
    print(g.getName(), g.getAge(), g.getAddress())


'''4. Hierarchical inheritance More than one derived classes are created from a single base.
4. Hybrid inheritance: This form combines more than one form of inheritance. 
Basically, it is a blend of more than one type of inheritance.
Private members of parent class
We don’t always want the instance variables of the parent class to be inherited by the child class 
i.e. we can make some of the instance variables of the parent class private, which won’t be available 
to the child class.
We can make an instance variable by adding double underscores before its name. For example,'''
# Python program to demonstrate private members
# of the parent class
class C:        #(object):
    def __init__(self):
        self.c = 21

        # d is private instance variable
        self.__d = 42


class D(C):
    def __init__(self):
        self.e = 84
        C.__init__(self)

def test_hierarchical_inheritance():
    object1 = D()
    # the following will not error as c is public instance variable
    print(object1.c)
    # the folowing produces an error as d is private instance variable
    # print(object1.d)
#endregion


#region classmethod & staticmethod example
'''Though classmethod and staticmethod are quite similar, 
there's a slight difference in usage for both entities: 
classmethod must have a reference to a class object as 
the first parameter, whereas staticmethod can have 
no parameters at all.'''
'''Example'''
class Date:      #(object):     #again, (object) gives TypeError, probably to do with python 3.x

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        date1 = cls(day, month, year)
        return date1

    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split('-'))
        return day <= 31 and month <= 12 and year <= 3999


def test_classmethod_staticmethod():
    date2 = Date.from_string('11-09-2012')
    is_date = Date.is_date_valid('11-09-2012')
#endregion


#region classmethod & staticmethod explanation
'''Explanation'''
'''This class obviously could be used to store information about 
certain dates (without timezone information; 
let's assume all dates are presented in UTC).

Here we have __init__, a typical initializer of Python 
class instances, which receives arguments as a typical 
instancemethod, having the first non-optional argument 
(self) that holds a reference to a newly created instance.'''

'''Class Method'''
'''We have some tasks that can be nicely done using classmethods.
Let's assume that we want to create a lot of Date class instances 
having date information coming from an outer source encoded 
as a string with format 'dd-mm-yyyy'. Suppose we have to do this 
in different places in the source code of our project.
So what we must do here is:
Parse a string to receive day, month and year as three integer 
variables or a 3-item tuple consisting of that variable.
Instantiate Date by passing those values to the initialization call.
This will look like:
string_date = '11-09-2012'
day, month, year = map(int, string_date.split('-'))
date1 = Date(day, month, year)
For this purpose, C++ can implement such a feature with 
overloading, but Python lacks this overloading. 
Instead, we can use the classmethod from_string (see above). 
Let's create another "constructor".
Let's look more carefully at the above implementation, 
and review what advantages we have here:
We've implemented date string parsing in one place 
and it's reusable now.
Encapsulation works fine here (if you think that you could 
implement string parsing as a single function elsewhere, 
this solution fits the OOP paradigm far better).
cls is an object that holds the class itself, 
not an instance of the class. It's pretty cool 
because if we inherit our Date class, 
all children will have from_string defined also. '''

'''Static method'''
'''What about staticmethod? It's pretty similar to classmethod 
but doesn't take any obligatory parameters 
(like a class method or instance method does).
Let's look at the next use case for the staticmethod is_date_valid (see above)
We have a date string that we want to validate somehow. 
This task is also logically bound to the Date class we've used so far, 
but doesn't require instantiation of it.
Here is where staticmethod can be useful. Let's look at the usage:
is_date = Date.is_date_valid('11-09-2012')
So, as we can see from usage of staticmethod, we don't have any access to 
what the class is---it's basically just a function, called syntactically 
like a method, but without access to the object and its internals 
(fields and another methods), while classmethod does.'''
#endregion


#region simulate annealing (optimization))
from scipy import optimize
import matplotlib
import pandas

# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 16:48:33 2019

@author: author
"""
# from scipy import optimize


params = (2, 3, 7, 8, 9, 10, 44, -1, 2, 26, 1, -2, 0.5)
def f1(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (a * x**2 + b * x * y + c * y**2 + d*x + e*y + f)

def f2(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (-g*np.exp(-((x-h)**2 + (y-i)**2) / scale))

def f3(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return (-j*np.exp(-((x-k)**2 + (y-l)**2) / scale))

def f(z, *params):
    x, y = z
    a, b, c, d, e, f, g, h, i, j, k, l, scale = params
    return f1(z, *params) + f2(z, *params) + f3(z, *params)


def test_simulated_annealing():
    # optimize.anneal is deprecated - claim has been made basinhopping
    # works just like anneal
    # x0 = np.array([2., 2.])     # Initial guess.
    # np.random.seed(555)   # Seeded to allow replication.
    # res = optimize.anneal(f, x0, args=params, schedule='boltzmann',
    #                       full_output=True, maxiter=500, lower=-10,
    #                       upper=10, dwell=250, disp=True)

    minimizer_kwargs = {"method":"L-BFGS-B", "args":params}
    # NOTE, np array give the same results as the list for x0
    x0 = np.array([2., 2.])     # Initial guess.
    np.random.seed(555)   # Seeded to allow replication.
    # x0=[2.,2.]
    ret_params = optimize.basinhopping(
            f, x0, minimizer_kwargs=minimizer_kwargs, niter=200)
    print("simulated annealing - global minimum from params: x = [%.4f, %.4f], f(x0, *params) = %.4f" %
          (ret_params.x[0], ret_params.x[1], ret_params.fun))

    func = lambda x: np.cos(14.5 * x - 0.3) + (x + 0.2) * x
    minimizer_kwargs = {"method": "BFGS"}
    x0=[1.]
    ret_func = optimize.basinhopping(
            func, x0, minimizer_kwargs=minimizer_kwargs, niter=200)
    print("simulated annealing - global minimum from func: x = %.4f, f(x0) = %.4f" %
          (ret_func.x, ret_func.fun))

    def func2d(x):
        f = np.cos(14.5 * x[0] - 0.3) + (x[1] + 0.2) * x[1] + (x[0] + 0.2) * x[0]
        df = np.zeros(2)
        df[0] = -14.5 * np.sin(14.5 * x[0] - 0.3) + 2. * x[0] + 0.2
        df[1] = 2. * x[1] + 0.2
        return f, df
    minimizer_kwargs = {"method":"L-BFGS-B", "jac":True}
    x0 =[1.0, 1.0]
    ret_func2d = optimize.basinhopping(
            func2d, x0, minimizer_kwargs=minimizer_kwargs, niter=200)
    print("simulated annealing - global minimum from func2d: x = [%.4f, %.4f], f(x0) = %.4f" %
          (ret_func2d.x[0], ret_func2d.x[1], ret_func2d.fun))

#endregion


#region Web Framework
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
# NOTE: "from flask.ext.jsonpify import jsonify" gives "ModuleNotFoundError: No module named 'flask.ext'" error,
# use "from flask_jsonpify import jsonify" instead
# from flask.ext.jsonpify import jsonify
from flask_jsonpify import jsonify

import sqlite3#

class Employees(Resource):
    def get(self):
        conn = db_connect.connect()  # connect to database
        query = conn.execute("select * from employees")  # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID


class Tracks(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


class Employees_Name(Resource):
    def get(self, employee_id):
        conn = db_connect.connect()
        query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

def test_web_app():
    db_connect = create_engine('sqlite:///chinook.db')
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Employees, '/employees')  # Route_1
    api.add_resource(Tracks, '/tracks')  # Route_2
    api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3

    if __name__ == '__main__':
        app.run(port='5002')
#endregion


#region Image Manipulation Downsample and Upsample
# using the Python Image Library (PIL) to resize an image
# works with Python27 and Python32
from PIL import Image, ImageFont, ImageDraw

def resize_image(image_filename_param, factor_ratio_param, resize_filter_str_param, other_new_filename_suffix=''):
    import os

    # split image filename into name and extension
    name, ext = os.path.splitext(image_filename_param)
    img_org = Image.open(image_filename_param)
    # get the size of the original image
    width_org, height_org = img_org.size

    # set the resizing factor so the aspect ratio can be retained
    # factor > 1.0 increases size
    # factor < 1.0 decreases size
    factor = 0.75
    width = int(width_org * factor_ratio_param)
    height = int(height_org * factor_ratio_param)

    filter = Image.NEAREST  # default set to use Image.NEAREST filter
    if resize_filter_str_param == 'antialias':
        filter = Image.ANTIALIAS    # best down-sizing filter
    elif resize_filter_str_param == 'nearest':
        filter = Image.NEAREST      # use nearest neighbour
    elif resize_filter_str_param == 'bilinear':
        filter = Image.BILINEAR     # linear interpolation in a 2x2 environment
    elif resize_filter_str_param == 'bicubic':
        filter = Image.BICUBIC      # cubic spline interpolation in a 4x4 environment

    # best down-sizing filter
    img = img_org.resize((width, height), filter)
    # create a new file name for saving the result
    new_image_file = "%s%s_%s%s%s" % (name, str(factor_ratio_param), resize_filter_str_param,
                                      other_new_filename_suffix, ext)
    img.save(new_image_file)
    print('resized image size = ({},{}), resized file saved as {}'.format(img.size[0], img.size[1], new_image_file))

    return True, new_image_file

def test_image_resizing():
    image_file = "Defense.png"
    resized_antialias, new_image_file_antialias = resize_image(image_file, 0.75, 'antialias')
    resized_bilinear, new_image_file_bilinear = resize_image(image_file, 10, 'bilinear')
    resized_bicubic, new_image_file_bicubic = resize_image(image_file, 10, 'bicubic')
    resized_nearest, new_image_file_nearest = resize_image(image_file, 10, 'nearest')

    # one way to show the image is to activate
    # the default viewer associated with the image type
    import webbrowser
    webbrowser.open(new_image_file_nearest)

    # # optional image viewer ...
    # # image viewer  i_view32.exe   free download from:  http://www.irfanview.com/
    # # avoids the many huge bitmap files generated by PIL's show()
    # import os
    # os.system("d:/python24/i_view32.exe %s" % "BILINEAR.png")
#endregion


#region Image Manipulation Imposing Text
# Image: to create an image object for our greeting background
# ImageDraw: creates a drawing context
# ImageFont: font of the text we will be drawing on the greeting
from PIL import Image, ImageDraw, ImageFont

def impose_text_on_image(background_image_filename_param, indexes_texts_pair_dict_param,
                         font_filename_param, font_size_param, text_color_param, new_image_filename_param):
    # create Image object with the input image
    image = Image.open(background_image_filename_param)

    # initialise the drawing context with the image object as background
    draw = ImageDraw.Draw(image)

    # create font object with the font file and specify desired size
    font = ImageFont.truetype(font_filename_param, size=font_size_param)

    # k = index of the pixel where text to be drawn, v = text
    for k, v in indexes_texts_pair_dict_param.items():
        # draw the message on the background
        draw.text(k, v, fill=text_color_param, font=font)

    # save the edited image
    image.save(new_image_filename_param)

def test_impose_text_on_image():
    background_image_filename = 'Defense10_nearest.png'
    indexes_texts_pair_dict = dict()
    font_filename = 'ITCKRIST.TTF'
    font_size = 18
    text_color = 'rgb(0, 0, 0)'  # black color
    # text_color = 'rgb(255, 255, 255)'  # black color

    indexes_texts_pair_dict.clear()
    indexes_texts_pair_dict[(50, 50)] = "map"
    indexes_texts_pair_dict[(200, 300)] = 'vinyl'
    new_image_filename = 'Defense_nearest_impose_text.png'
    impose_text_on_image(background_image_filename, indexes_texts_pair_dict,
                         font_filename, font_size, text_color, new_image_filename)
#endregion


#region Embedding in Tk pseudo code, keeping under def as generaltools are being included wholely into projects
def embedding_in_tk_pseudo():
    import tkinter

    from matplotlib.backends.backend_tkagg import (
        FigureCanvasTkAgg, NavigationToolbar2Tk)
    # Implement the default Matplotlib key bindings.
    from matplotlib.backend_bases import key_press_handler
    from matplotlib.figure import Figure

    import numpy as np


    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


    def on_key_press(event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, canvas, toolbar)


    canvas.mpl_connect("key_press_event", on_key_press)


    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate


    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)

    tkinter.mainloop()
    # If you put root.destroy() here, it will cause an error if the window is
    # closed with the window manager.
#endregion


#region Image Display In Real Time
import tkinter

import matplotlib
# set matplotlib to use 'TKAgg' would make the plot to be in a seperate figure outside the PyCharm IDE
# rather than in "ScieView" to the right side of the IDE - in the "Plots" pane
matplotlib.use('TKAgg')

import matplotlib.pyplot as plt
# from matplotlib.path import Path
# import matplotlib.patches as patches

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

import numpy as np
import time

from skimage.draw import random_shapes
# from skimage import color as skolor # see the docs at scikit-image.org/
# from skimage import measure
# from scipy.ndimage import gaussian_filter

# thw function below is crated primarily for Battleship project
# to display two client players in the same plot
# also usefult for generic purpose
def display_all_images_in_plot(total_rows_in_plot_param, title_img_pairs_param, fig_param,
                               plot_canvas_param, rearrange_sbuplot=False):
    number_images = len(title_img_pairs_param)
    total_rows = total_rows_in_plot_param
    total_cols = int(number_images/total_rows) + (number_images%total_rows)
    # print('title_img_pairs_param={}\nnumber_images={}\ntotal_rows={}\ntotal_cols={}'.format(
    #     title_img_pairs_param, number_images, total_rows, total_cols))

    # if rearrange_sbuplot=True, exiting axes can be removed and new ones added
    # this allows us to have different number of axes in the plot in real time
    ax_list = list(fig_param.axes)
    if (rearrange_sbuplot):
        for ax in ax_list:
            fig_param.delaxes(ax)

            # the code below cearl out the cavas but doesn't re-draw
            plot_canvas_param.flush_events()
            plot_canvas_param.draw()
            plot_canvas_param.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # DO NOT USE plotCanvas.get_tk_widget().delete('all'),
    # it delete everyting but doesn't re-draw.
    # Instead, use plotCanvas.flush_events() below

    for i, (k, v) in enumerate(title_img_pairs_param.items()):
        # time.sleep(0.1)  # introduce a bit of deplay so we can see the animated effect
        # print('refereshing axes: total_rows={}, total_cols={}, i={}'.format(total_rows, total_cols, i))
        # note, subplot index is one-based, hence i+1
        ax = None
        if(len(ax_list) == 0):
            ax = fig_param.add_subplot(total_rows, total_cols, i+1)
        else:
            ax = ax_list[i]
            ax.clear()
        # v is the image
        ax.imshow(v)
        # k is the label for the image
        ax.set_title(k, fontsize=8)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.axis('off')  # removes the axis to leave only the shape

        plot_canvas_param.flush_events()
        plot_canvas_param.draw()
        plot_canvas_param.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)


# the input param, title_img_pairs_list_param, for the function below is
# a list of title_img_pairs, all of images in each title_img_pairs are
# displayed in the plot at any one time.
# the purpose of making a list here is for testing real time rendering
def test_realtime_display_group_of_images(total_rows_in_plot_param,
                                          title_img_pairs_list_param, fig_param, plot_canvas_param):
    while(True):
        for v in title_img_pairs_list_param:
            time.sleep(1)
            display_all_images_in_plot(total_rows_in_plot_param, v, fig_param, plot_canvas_param)


def generate_test_title_img_pairs_list():
    test_title_img_pairs_list = list()

    title_img_pairs = dict()
    loaded_im, rgb_list, img, pix = load_from_image('Defense.png')
    title_img_pairs['Defense.png'] = img
    loaded_im, rgb_list, img, pix = load_from_image('uncleaned_map.png')
    title_img_pairs['uncleaned_map.png'] = img
    test_title_img_pairs_list.append(title_img_pairs)

    title_img_pairs_1 = dict()
    loaded_im, rgb_list, img, pix = load_from_image('cleaned_single_cell_map.png')
    title_img_pairs_1['cleaned_single_cell_map.png'] = img
    loaded_im, rgb_list, img, pix = load_from_image('cleaned_single_cell_and_ingrass_wall_map.png')
    title_img_pairs_1['cleaned_single_cell_and_ingrass_wall_map.png'] = img
    test_title_img_pairs_list.append(title_img_pairs_1)

    return test_title_img_pairs_list


def load_from_image(filename):
    try:
        im = Image.open(filename)  # Can be many different formats, can even be byte buffer
        print('image size = {}'.format(im.size))  # Get the width and hight of the image for iterating over
        rgb_list, pix = get_rgb_list(im)
        # return im and pix for updating pixel values and saving modified image,
        # note, pix is a PixeAccess Class, and it doesn't has size attribute, so,
        # returning im for: 1. access the image size, 2. save any modification to the image
        # also, pix has flopped indexing, so when use simply swap row and col
        return True, rgb_list, im, pix
    except:
        print("No image map file exists")
        return False, None, None, None


def get_rgb_list(im_param):
    pix = im_param.load()  # load pixel RGB value of the image
    rgb_list = [[(0, 0, 0)] * im_param.size[1] for n in range(im_param.size[0])]
    for i in range(im_param.size[0]):
        for j in range(im_param.size[1]):
            # note, rgb_list returned from this function is the same as pix, ie, flopped indexing
            rgb_list[i][j] = pix[i, j]
    return rgb_list, pix  # return pix for updating pixel values


def draw_game_board_on_image(number_of_cells, w, font_szie, grid_texts, grid_colours,
                             is_winner, draw_debug=False):
    # print('function: {}'.format(sys._getframe().f_code.co_name))
    from PIL import Image, ImageDraw, ImageFont, ImageColor

    total_row = number_of_cells
    total_col = number_of_cells
    # grid = [[1] * total_col for n in range(total_row)]
    devision = font_szie / 2
    text_shift = int(w / devision)  # canvas.creat_text centres the text at the coordinate

    # PIL create an empty image and draw object to draw on
    # memory only, not visible
    image1 = Image.new("RGB", (w*number_of_cells, w*number_of_cells), "white")
    draw = ImageDraw.Draw(image1)

    # clear the drawing area
    draw.rectangle((0,0,w*number_of_cells,w*number_of_cells), fill="white", outline="black")

    # set the origin
    x, y = 0, 0

    # font = ImageFont.truetype("arial.ttf", font_szie)
    font = ImageFont.truetype("ITCKRIST.TTF", font_szie)
    winner_font = ImageFont.truetype("ITCKRIST.TTF", 24)
    # font = ImageFont.truetype("MISTRAL.TTF", font_szie)
    fill_black = ImageColor.getrgb('black')
    fill_white = ImageColor.getrgb('white')
    fill_orange = ImageColor.getrgb('orange')
    fill_red = ImageColor.getrgb('red')
    for i in range(total_row):
        for j in range(total_col):
            row_index = int(y / w)
            col_index = int(x / w)
            cell_colour = grid_colours[row_index][col_index]
            cell_text = grid_texts[row_index][col_index]
            if draw_debug:
                print('row_index={}, col_indxe={}, cell_colour={}, cell_image={}'.format(
                    row_index, col_index, cell_colour, cell_text
                ))
            # minuts one is t avoid the last rectange has to outline
            right = x+w
            if j == total_col-1:
                right = x+w-1
            bottom = y+w
            if i == total_row-1:
                bottom = y+w-1
            draw.rectangle((x, y, right, bottom), fill=cell_colour, outline='black')
            text_x = x + text_shift
            text_y = y + text_shift
            if cell_text == 'Hit':
                draw.text((text_x, text_y), text="X", fill=fill_orange, font=font)  # (0, 0, 0, 0)
            elif cell_text == '?':
                draw.text((text_x, text_y), text="?", fill=fill_black, font=font)
            elif cell_text == 'Miss':
                draw.text((text_x, text_y), text="*", fill=fill_black, font=font)
            # NOTE, the following is for game board edges,
            # keep the image name to determine the piece, but simply use text
            elif cell_text == '1':
                draw.text((text_x, text_y), text="1", fill=fill_white, font=font)  # (255, 255, 255, 255)
            elif cell_text == '2':
                draw.text((text_x, text_y), text="2", fill=fill_white, font=font) 
            elif cell_text == '3':
                draw.text((text_x, text_y), text="3", fill=fill_white, font=font)
            elif cell_text == '4':
                draw.text((text_x, text_y), text="4", fill=fill_white, font=font)
            elif cell_text == '5':
                draw.text((text_x, text_y), text="5", fill=fill_white, font=font)
            elif cell_text == '6':
                draw.text((text_x, text_y), text="6", fill=fill_white, font=font)
            elif cell_text == '7':
                draw.text((text_x, text_y), text="7", fill=fill_white, font=font)
            elif cell_text == '8':
                draw.text((text_x, text_y), text="8", fill=fill_white, font=font)
            elif cell_text == '9':
                draw.text((text_x, text_y), text="9", fill=fill_white, font=font)
            elif cell_text == '10':
                draw.text((text_x, text_y), text="10", fill=fill_white, font=font)
            elif cell_text == 'A':
                draw.text((text_x, text_y), text="A", fill=fill_white, font=font)
            elif cell_text == 'B':
                draw.text((text_x, text_y), text="B", fill=fill_white, font=font)
            elif cell_text == 'C':
                draw.text((text_x, text_y), text="C", fill=fill_white, font=font)
            elif cell_text == 'D':
                draw.text((text_x, text_y), text="D", fill=fill_white, font=font)
            elif cell_text == 'E':
                draw.text((text_x, text_y), text="E", fill=fill_white, font=font)
            elif cell_text == 'F':
                draw.text((text_x, text_y), text="F", fill=fill_white, font=font)
            elif cell_text == 'G':
                draw.text((text_x, text_y), text="G", fill=fill_white, font=font)
            elif cell_text == 'H':
                draw.text((text_x, text_y), text="H", fill=fill_white, font=font)
            elif cell_text == 'I':
                draw.text((text_x, text_y), text="I", fill=fill_white, font=font)
            elif cell_text == 'J':
                draw.text((text_x, text_y), text="J", fill=fill_white, font=font)
            x = x + w
        y = y + w
        x = 0
    if is_winner:
        draw.text((w*int(number_of_cells/2-2), w*int(number_of_cells/2-2)), text="WINNER", fill=fill_red, font=winner_font)

    image1.save("test_image_draw.png")
    return image1


# the input param, title_img_pairs_list_param, for the function below is
# a list of title_img_pairs, all of images in each title_img_pairs are
# displayed in the plot at any one time.
# the purpose of making a list here is for testing real time rendering
def test_realtime_display_graphics(number_of_cells,font_szie, w, total_rows_in_plot_param, fig_param, plot_canvas_param,
                                   grid_texts_default_param, grid_colours_default_param, sleep_param):
    import copy
    grid_texts_1 = copy.deepcopy(grid_texts_default_param)
    grid_colours_1 = copy.deepcopy(grid_colours_default_param)
    grid_texts_2 = copy.deepcopy(grid_texts_default_param)
    grid_colours_2 = copy.deepcopy(grid_colours_default_param)
    i = 0
    j = 0
    grid_total_rows = len(grid_texts_default_param)
    grid_total_cols = len(grid_texts_default_param[0])
    while(True):
        m = max(i, j)
        i += 1
        j = i + 2
        m = max(i, j)
        if (i < grid_total_rows and j < grid_total_cols):
            grid_texts_1[i][j] = 'Hit'
            grid_colours_1[i][j] = 'LightSkyBlue'
            grid_texts_2[j][i] = 'Hit'
            grid_colours_2[j][i] = 'LightSkyBlue'
            image_1 = draw_game_board_on_image(number_of_cells, w, font_szie, grid_texts_1, grid_colours_1,
                                               True, draw_debug=False)
            image_title_1 = "hit board"
            image_2 = draw_game_board_on_image(number_of_cells, w, font_szie, grid_texts_2, grid_colours_2,
                                               True, draw_debug=False)
            image_title_2 = "score board"
            pairs = dict()
            pairs[image_title_1] = image_1
            pairs[image_title_2] = image_2
            time.sleep(sleep_param)
            display_all_images_in_plot(total_rows_in_plot_param, pairs, fig_param, plot_canvas_param)
        else:
            i = 0
            j = 0
            grid_texts_1 = copy.deepcopy(grid_texts_default_param)
            grid_colours_1 = copy.deepcopy(grid_colours_default_param)
            grid_texts_2 = copy.deepcopy(grid_texts_default_param)
            grid_colours_2 = copy.deepcopy(grid_colours_default_param)


def update_grid_text_and_color(grid_texts_default_param, grid_colours_default_param,
                               player_knowledge_param):
    import copy
    grid_texts = copy.deepcopy(grid_texts_default_param)
    grid_colours = copy.deepcopy(grid_colours_default_param)
    # NOTE, player_knowledge is 10x10, and we do not update grid top-row and left-column
    # set start=1 in enumerate
    # i = 0
    # j = 0
    grid_total_rows = len(grid_texts_default_param)
    grid_total_cols = len(grid_texts_default_param[0])
    for i, word in enumerate(player_knowledge_param, start=1):
         for j, char in enumerate(word, start=1):
             if char == 'X':
                grid_texts[i][j] = 'Hit'
                grid_colours[i][j] = 'black'
             elif char == '.':
                grid_texts[i][j] = 'Miss'
                grid_colours[i][j] = 'LightSkyBlue'
             elif char == '?':
                grid_texts[i][j] = '?'
                grid_colours[i][j] = 'white'
             else:
                grid_texts[i][j] = 'none'
                grid_colours[i][j] = 'white'

    return grid_texts, grid_colours


# the following three functions may comes handy when doing image analysis
# for example algorithm for moving the bat in Breakout project
def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

def byte_array_to_int_array(bytearray):
    i_result = []
    for b in bytearray:
        i = int.from_bytes(b, byteorder='big', signed=False)
        i_result.append(i)
    return i_result


def matplot_display_setup(figure_width_param, figure_height_param):
    root = tkinter.Tk()
    root.wm_title("Embedding in Tk")

    fig = Figure(figsize=(figure_width_param, figure_height_param), dpi=100)  # set figure size

    plotCanvas = FigureCanvasTkAgg(fig, master=root)  # a tk.DrawingArea.
    plotCanvas.draw()
    plotCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    color = "grey"  # "#ffffff"
    toolbar = NavigationToolbar2Tk(plotCanvas, root)
    toolbar.config(background=color)
    toolbar._message_label.config(background=color)
    toolbar.update()  # toolbar.pack(side=BOTTOM)
    plotCanvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def on_key_press(event):
        print("you pressed {}".format(event.key))
        key_press_handler(event, plotCanvas, toolbar)

    plotCanvas.mpl_connect("key_press_event", on_key_press)

    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate

    button = tkinter.Button(master=root, text="Quit", command=_quit)
    button.pack(side=tkinter.BOTTOM)

    return root, fig, plotCanvas, toolbar, button


#endregion


#region Other Image animation examples
# from matplotlib.animation import FuncAnimation
#
# #######################################################
# fig, ax = plt.subplots()
# xdata, ydata = [], []
# ln, = plt.plot([], [], 'ro')
#
# def init():
#     ax.set_xlim(0, 2 * np.pi)
#     ax.set_ylim(-1, 1)
#     return ln,
#
# def update(frame):
#     xdata.append(frame)
#     ydata.append(np.sin(frame))
#     ln.set_data(xdata, ydata)
#     return ln,
#
# ani = FuncAnimation(fig, update, np.linspace(0, 2 * np.pi, 128),
#                     init_func=init, blit=True)
# plt.show()
#
# #########################################################
# import random
# import time
#
# from matplotlib import animation
#
# class RegrMagic(object):
#     """Mock for function Regr_magic()
#     """
#
#     def __init__(self):
#         self.x = 0
#
#     def __call__(self):
#         time.sleep(random.random())
#         self.x += 1
#         return self.x, random.random()
#
# regr_magic = RegrMagic()
#
# def frames():
#     while True:
#         yield regr_magic()
#
# fig = plt.figure()
#
# x = []
# y = []
#
# def animate(args):
#     x.append(args[0])
#     y.append(args[1])
#     return plt.plot(x, y, color='g')
#
# anim = animation.FuncAnimation(fig, animate, frames=frames, interval=1000)
# plt.show()

###########################################################
# fig = plt.figure()

# fig.addsubplot(...) arguments meanings:
# These are subplot grid parameters encoded as a single integer.For example, "111" means
# "1x1 grid, first subplot" and "234" means "2x3 grid, 4th subplot".
# Alternative form for add_subplot(111) is add_subplot(1, 1, 1)

# ax = fig.add_subplot(111)
# patch = patches.PathPatch(path, facecolor='none', lw=2)
# ax.add_patch(patch)
#
# ax.set_xlim(np.min(verts)*1.1, np.max(verts)*1.1)
# ax.set_ylim(np.min(verts)*1.1, np.max(verts)*1.1)
# ax.axis('off') # removes the axis to leave only the shape

# fig.canvas.draw()
# plt.show()
#endregion


#region system manipulation
def quit_programatically():
    import sys
    sys.exit("Error message")

# NOTE, although not python, other good examples to start/stop programs can be found:
# https://faq.cprogramming.com/cgi-bin/smartfaq.cgi?answer=1044654269&id=1043284392
#endregion
