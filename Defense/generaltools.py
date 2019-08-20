import sys
import json
import base64
import numpy as np
import random


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

import collections

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

##

# import sys, timeit
# print (sys.version + "\n")
# xs = list(range(10000)) + [999]
# fns = [p for name, p in globals().items() if name.startswith('check_dup')]
# for fn in fns:
#     print ('%50s %.5f' % (fn, timeit.timeit(lambda: fn(xs), number=100)))
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


# Driver code
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

@author: ysu1
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
# web framework stuff has been moved to codekat_neuron under users

# from flask import Flask, request
# from flask_restful import Resource, Api
# from sqlalchemy import create_engine
# from json import dumps
# # NOTE: "from flask.ext.jsonpify import jsonify" gives "ModuleNotFoundError: No module named 'flask.ext'" error,
# # use "from flask_jsonpify import jsonify" instead
# # from flask.ext.jsonpify import jsonify
# from flask_jsonpify import jsonify
#
# import sqlite3
# db_connect = create_engine('sqlite:///chinook.db')
# app = Flask(__name__)
# api = Api(app)
#
#
# class Employees(Resource):
#     def get(self):
#         conn = db_connect.connect()  # connect to database
#         query = conn.execute("select * from employees")  # This line performs query and returns json result
#         return {'employees': [i[0] for i in query.cursor.fetchall()]}  # Fetches first column that is Employee ID
#
#
# class Tracks(Resource):
#     def get(self):
#         conn = db_connect.connect()
#         query = conn.execute("select trackid, name, composer, unitprice from tracks;")
#         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
#         return jsonify(result)
#
#
# class Employees_Name(Resource):
#     def get(self, employee_id):
#         conn = db_connect.connect()
#         query = conn.execute("select * from employees where EmployeeId =%d " % int(employee_id))
#         result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
#         return jsonify(result)
#
#
# api.add_resource(Employees, '/employees')  # Route_1
# api.add_resource(Tracks, '/tracks')  # Route_2
# api.add_resource(Employees_Name, '/employees/<employee_id>')  # Route_3
#
# if __name__ == '__main__':
#     app.run(port='5002')
#endregion