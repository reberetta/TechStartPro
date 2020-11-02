# -*- coding: utf-8 -*-
"""

DB Preparer file

Olist challenge - Work for us

@author: reberetta

"""

import csv

"""

Function: create_tables

Parameters: DB cursor and connection

Return: void

This function creates the DB tables according to
db_diagram file of reference

"""
def create_tables(cursor, conn):
    
    #creates table categories
    cursor.execute("""CREATE TABLE IF NOT EXISTS categories (
                 id INTEGER NOT NULL PRIMARY KEY,
                 name VARCHAR(64) NOT NULL,
                 UNIQUE(name)
               );""")

    #creates table products
    cursor.execute("""CREATE TABLE IF NOT EXISTS products (
                 id INTEGER NOT NULL PRIMARY KEY,
                 name VARCHAR(64) NOT NULL,     
                 description TEXT NOT NULL,     
                 value FLOAT NOT NULL,
                 UNIQUE(name)
             ); """)

    #create table categories_products
    cursor.execute("""CREATE TABLE IF NOT EXISTS categories_products (
                 id_category INT NOT NULL,
                 id_product INT NOT NULL
              );""")              



"""

Function: add_categories

Parameters: DB cursor and connection

Return: void

This function reads a .csv file with 
the categories to be filled in the DB

"""
def add_categories(cursor, conn): 

    #Reading input categories filename
    file = input('Enter file name (Expects a csv file, using  comma as separator): ')

    #Extracting categories from file
    with open(file, newline='') as csvfile:
        reader = list(csv.reader(csvfile, delimiter=","))
        reader.pop(0) #removing row name
     
    #Insert categories into db table IF is UNIQUE
    for row in reader:
        cursor.execute("INSERT OR IGNORE INTO categories(name) VALUES (?)", (row[0],) ) 
    
    conn.commit()
