#!/usr/bin/python

# This file demonstrates some matrix operations in numpy.
# For plotting, I'll provide a separate example.
# A Matlab/Octave version is also available.
#
# I tend to use Python via:
#     ipython --pylab
# which provides a convenient interactive scientific computing environment.
# Simply enter a variable or expression to see the result. No print statements
# required.
#
# Iain Murray, January 2013

# IMPORTANT:
# Data analysis, programming, and mathematics are not spectator sports! You can
# only learn to munge data by doing it. Unless you spend a reasonable amount of
# time per lecture (~2hrs) reproducing the material for yourself, you won't
# really understand it. It's easy to kid yourself otherwise, but you really
# should be writing your own programs to reproduce at least some of the
# figures/numbers/methods discussed.
#
# If you can't do something here, or something related to the material here,
# ask a question on the copy you can find on NB.

# Make lots of common functions available in the current namespace.
# Bad software engineering practice, but convenient for quick jobs.
from numpy import *
from scipy import *
from matplotlib.pyplot import *
# "ipython --pylab" does these imports for you.
#
# The recommended alternative is "import numpy as np". However, if the bulk of
# my code is numerical, accidentally typing sum instead of np.sum or max instead
# of np.max can lead to frustrating bugs or performance problems. Sometimes I
# want to clobber the Python built-ins, so I don't use them by mistake.


# 1D arrays
# ---------

# Create a test list, and numpy array (a vector)
lst = [3, 1, 4, 1, 5, 9, 2]
vec = array([3, 1, 4, 1, 5, 9, 2], dtype='float64')
# Using double floating point numbers (float64) is often a good default.
# Another way to make the array floating point is to put a '.' after one or more
# of the numbers. (All numbers are doubles by default in Matlab.)

# EXERCISE explore a 1D numpy array:
# Load python, import numpy as above, and copy-paste the lst and vec definitions
# OR run "ipython --pylab" and type %run numpy_intro.py"
#
# Then evaluate lst+lst and vec+vec (notice the quite different answers!)
# Also try evaluating vec/2, vec+3, vec*vec, vec**2, etc.
# numpy arrays are specialized for convenient (and fast!) numerical computation.
# Most operators (+,-,*,/,**,etc) and functions (exp,log,sin,etc) work
# element-wise on all the numbers in the array. (For matrix multiplication use
# the dot() function.)
#
# Both variables (lst and vec) support zero-based indexing and slicing.
# (NB Matlab is one-based!)
# Predict and evaluate: lst[0], lst[3:5], lst[-1], vec[0], vec[3:5], vec[-1]
# numpy arrays also let you select a list of indexes:
# Try vec[[0,3,5,2,2]] (normal python lists don't support indexing with lists)
#
# TODO -- have you worked through all the exercises above?


# 2D arrays (used for matrices)
# -----------------------------

# NB numpy does have a separate "matrix" type. I recommend never using numpy's
# "matrices", and using arrays for everything. It will be less confusing, and
# arrays are much more widely used, so probably less buggy.

# Create a numpy array from a list of lists
A = np.array([[ 1, 2, 3],
           [ 4, 5, 6],
           [ 7, 8, 9],
           [10,11,12],
           [13,14,15]], dtype='float64')

B = np.array([[1,2,3,4,5],
            [6,7,8,9,10],
            [11,12,13,14,15]], dtype='float64')

print("\nHere's the whole test array:")
print(A)
print('A is a numpy array with shape ' + repr(A.shape))
print('That means A has %d rows.' % A.shape[0])
print('EXERCISE: print the number of columns in A')
# TODO

print("\nLike a normal list of lists, we can index the rows:")
print("    (NB this behavior is NOT like Matlab's A(1), A(1:3))")
print("A[0] =")
print(A[0])
print("A[0:3] =")
print(A[0:3])

print("\nWe could then clumsily take of the first element of a row:")
print("A[0][0] =")
print(A[0][0])
print("But a neater way to get the 0th row of the 0th column is:")
print("A[0,0] =")
print(A[0,0])

print("\nEXERCISE: print the bottom right element of the array")
# TODO

print('\nRows and columns can be sliced like Python lists:"')
print("A[0:2,:] =")
print(A[0:2,:])

print("\nEXERCISE: print the last column of A:")
# TODO
print("\nEXERCISE: print the first two rows of the last column of A:")
# TODO

print('\nExtracting multiple desired rows and columns:"')
# Sadly more cryptic than the Matlab version. I had to look this up at
# http://www.scipy.org/NumPy_for_Matlab_Users
print("A[ix_([0,3,4],[0,2])] =")
print(A[ix_([0,3,4],[0,2])])
# Another version is "A[[0,3,4]][:,[0,2]]", but that can't be assigned to.


# Work with arrays
# ----------------

# To find the mean of each column of an array you might do:
I, J = A.shape
mu = zeros(J) # allocate space for answer
for i in range(I):
    for j in range(J):
        mu[j] += A[i,j]
mu = mu / I
print('\nMean: ' + repr(mu))
#
# But code with a lot of numerical computations would be cluttered very quickly.
# So you you would create a function called "mean". Except numpy already has
# one:
mu = mean(A, 0) # 0 means sum over the 0th dimension of the array (the rows)
print('Mean: ' + repr(mu))
#
# EXERCISE: print a vector containing the mean of each row of A
# TODO

# To make each column zero-mean, we could laboriously subtract off the mean:
A_shift = copy(A) # without copy, would modify A when modify A_shift
for i in range(I):
    for j in range(J):
        A_shift[i,j] -= mu[j]
print('Cols centered:\n' + repr(A_shift))
# But we can subtract arrays of the same shape in numpy, so can take
# the mean row off each row in one operation per row:
A_shift = copy(A)
for i in range(A.shape[0]):
    A_shift[i] -= mu
print('Cols centered:\n' + repr(A_shift))
# And in fact numpy works out what we want with the obvious expression:
A_shift = A - mu
print('Cols centered:\n' + repr(A_shift))
print('Check the columns are centered: ' + repr(mean(A_shift, 0)))

# To make the rows zero mean:
row_mu = mean(A, 1)
mu = mean(A,0)
# A_rshift = A - row_mu # this line wouldn't work
# You could loop over the array. But if you learn about "broadcasting" you can
# write faster and neater code:
#
# numpy will subtract arrays if every element of their shapes match.
# Optionally any element of the shape of either array can be 1.
# In this example:
#     row_mu.shape == (5,)
# It's a vector of length 5. We can make it a 5x1 array with the special
# indexing syntax: row_mu[:,newaxis]
# This new 5x1 array can now be subtracted from any 5xD array. The column array
# will be subtracted from each of the D columns.
A_rshift = A - row_mu[:,newaxis]
# EXERCISE: check that this answer had the intended effect.
# TODO

# EXERCISE A.T is the matrix transpose of the array. You could also make the
# rows zero mean by transposing the array, making the columns zero-mean, and
# transposing back. This transpose dance is inelegant, but would not require
# using newaxis. Have a go.
# TODO

# EXERCISE: make a standardized version of array A where each column has zero
# mean and standard deviation of one. And check your answer. The sample standard
# deviation is provided by std. (Optional keyword argument ddof=1 gives the
# unbiased estimator.)
# TODO

A_ubi = np.copy(A)


# EXERCISE: make a standardized version of array A where each row has zero mean
# and standard deviation of one. And check your answer.
# TODO


# Finding and sorting
# -------------------

print('\nFinding and Sorting:')
people = ['jim', 'alice', 'ali', 'bob']
height_cm = array([180, 165, 165, 178])

# The laborious, procedural programming way:
largest_height = -Inf
tallest_person = ''
for (i,h) in enumerate(height_cm):
    if h > largest_height:
        largest_height = h
        tallest_person = people[i]
print('largest_height = %g' % largest_height)
print('tallest_person = %s' % tallest_person)
# Of course there's a standard routine built in:
largest_height = max(height_cm)
print('largest_height = %g' % largest_height)
# alternatively we can ask for the location of the largest element:
idx = argmax(height_cm)
largest_height = height_cm[idx]
tallest_person = people[idx]
print('largest_height = %g' % largest_height)
print('tallest_person = %s' % tallest_person)

# What about the shortest person?
smallest_height = min(height_cm)
idx = argmin(height_cm)
smallest_person = people[idx]
# Except actually, that's just the first one, there is a tie:
ids = argwhere(height_cm == smallest_height)
smallest_people = [people[i] for i in ids]
print('smallest_people: ' + repr(smallest_people))
#
# For future reference: to get indexes to index numpy arrays, we normally use
# "nonzero" or "where". But for the code above I'd need to extract the indexes
# by appending "[0]", which I thought was ugly:
#ids = nonzero(height_cm == smallest_height)[0]
#ids = where(height_cm == smallest_height)[0]

# sort(height_cm) sorts the list. Again, a second argument will give the indexes
# of the corresponding items.
sorted_heights = sort(height_cm)
print('sorted_heights: ' + repr(sorted_heights))
ids = argsort(height_cm)
sorted_heights = height_cm[ids]
# The previous line wouldn't work with a normal list, but numpy arrays allow a
# list of indexes. The python list of people needs a list comprehension:
people_in_height_order = [people[i] for i in ids]
print('sorted_heights: ' + repr(sorted_heights))
print('people_in_height_order: ' + repr(people_in_height_order))


# Turning maths in matrix operations "vectorization"
# --------------------------------------------------

# Mathematical expressions can often be computed with terse array-based
# expressions. The most important thing is to have working, correct code. So
# don't be afraid to accumulate your answers in for loops, at least as first.
# However, where you can spot standard matrix operations, your code will be
# shorter, sometimes clearer, and faster.

# Given a mathematical expression like:
# result = \sum_{i=1}^I fn(x_i, x_j) val(z_i)
# The results of fn could be put in an IxJ matrix, and the results of val in a
# length-I vector. The sum is then a matrix-vector multiply:
# result = dot(fn.T, val)

# Given another expression:
# result_j = \sum_{i=1}^I fn(x_i, x_j) weights(z_i, z_j)
# The result is a vector. We can do the multiplication inside the sum for all i
# and j at once, and then sum out the index i: results = sum(fn*weights, 0)

# Sometimes a newaxis index expression is required to make a vector be a Dx1 or
# 1xD matrix so that an elementwise operator can combine it with a matrix (using
# "broadcasting").

# There are no exercises here for now. If you see code that involves tricks you
# don't understand, try to write a for-loop version based on what you think it
# should do, and see if you get the same answer. If you are writing code with
# lots of for loops, keep going, but then afterwards try to replace parts of it
# with a "vectorized" version, checking that your answers don't change.
