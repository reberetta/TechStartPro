# -*- coding: utf-8 -*-
"""

Main file

Olist challenge - Work for us

@author: reberetta

"""

import sqlite3
import dbPreparer
import productsHandler

"""

Function: check_option

Parameters: option, DB cursor and connection

Return: void

This function checks option and performs action

"""


def check_option(option, cursor, conn):
    if(option == 1): #Add a product
        answer = 'y'
        while(answer == 'y' or answer == 'Y' ):
            productsHandler.add_product(cursor, conn)
            answer = input('Is there a product to insert? (y/n)')
    elif (option == 2): #Search a product
        answer = 'y'
        while(answer == 'y' or answer == 'Y'):
            productsHandler.search_products(cursor)
            answer = input("Do you want to search for a product? (y/n)")
    elif (option == 3):#Update product
            answer = 'y'
            while(answer == 'y' or answer == 'Y'):
                productsHandler.update_product(cursor, conn)
                answer = input("Do you want to update a product? (y/n)")
    else: #Delete a product
        answer = 'y'
        while(answer == 'y' or answer == 'Y'):
            productsHandler.delete_product(cursor, conn)
            answer = input("Do you want to delete a product? (y/n)")


#Connecting do DB
conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

#Prepares DB
dbPreparer.create_tables(cursor, conn)
dbPreparer.add_categories(cursor, conn)

#Main execution
option = productsHandler.show_menu()

#Loop whille users want a new action
while(option != 0):
    check_option(option, cursor, conn)
    option = productsHandler.show_menu()
    
#Closing BD connection
conn.close()