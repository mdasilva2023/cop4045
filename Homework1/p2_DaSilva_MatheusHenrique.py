# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 16:52:47 2026

@author: Matheus Henrique Bijos Da Silva
"""


def find_Pythagorean(n):

    triples = []

    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a ** 2 + b ** 2 == c ** 2:
                    triples.append((a, b, c))

    return triples


# main code

n = int(input("Enter a positive integer (n): "))

result = find_Pythagorean(n)

print("Pythagorean triples (a, b, c) with 0 < a, b, c <=", n, ":")
for triple in result:
    print(triple)