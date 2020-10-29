# -*- coding: utf-8 -*-

import csv

file = input('Enter file name:')


with open(file, newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print(row['nome'])
