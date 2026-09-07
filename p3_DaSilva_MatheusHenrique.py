# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 17:17:13 2026

@author: Matheus Henrique Bijos Da Silva
"""


def find_dup_str(s, n):

    for i in range(len(s) - n + 1):
        substring = s[i:i + n]

        for j in range(i + n, len(s) - n + 1):
            if s[j:j + n] == substring:
                return substring

    return ""



s = input("Enter a string: ")
n = int(input("Enter a length n: "))

result = find_dup_str(s, n)
print("Duplicated substring of length", n, ":", result)


def find_max_dup(s):

    max_length = len(s) // 2

    for length in range(max_length, 0, -1):
        found = find_dup_str(s, length)
        if found != "":
            return found

    return ""


s = input("Enter a string: ")

result = find_max_dup(s)
print("Longest duplicated substring:", result)