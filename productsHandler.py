# -*- coding: utf-8 -*-
"""

Products Handler file

Olist challenge - Work for us

@author: reberetta

"""

"""

Function: show_menu

Parameters: void

Return: option choosen

This function show the user a menu, 
and returns a valid option

"""
#Show Menu Options
def show_menu():
    
    option = -1
    
    #loop untill a valid option is read
    while(option < 0 or option > 4):
        print()
        print(40*'*')
        option = int(input("""What do you want to do?
                       1 - Add a product
                       2 - Search for a product
                       3 - Edit a product
                       4 - Delete a product
                       0 - Finish 
                       """))
    return option                          
                       
"""

Function: show_Categories

Parameters: DB cursor

Return: void

This function retieves and shows Categories

"""
def show_Categories(cursor):
    
    print('{:>5}'.format('id') + " | Category")

    #Retrieves categories
    allcategories = list(cursor.execute("SELECT * FROM categories"))

    #show categories
    for cat in allcategories:
        print('{:>5}'.format(cat[0]) + " | " + cat[1])
       
"""

Function: add_product

Parameters: DB cursor and connection

Return: void

This function adds a product

"""
def add_product(cursor, conn):
    
    #Read product infos
    print()
    print(20*'-')
    name = input('Enter product name: ')
    description = input('Enter product description: ')
    value = input('Enter product value: ')
    
    #insert product IF name is UNIQUE
    cursor.execute("INSERT OR IGNORE INTO products(name, description, value) VALUES (?,?,?)", (name, description, value) ) 
    #Retieves new product id
    id_product = cursor.lastrowid

    if cursor.rowcount < 1: #if insert was not sucessfull
        print("ERROR! Product " + name + " was not sucessfully inserted! Probably this name product is already in use.")
    else:
        #Show existing categories to relate to product
        show_Categories(cursor)
        print("Please enter the categories ids that this product belongs to: (Enter 0 to finish)")
        set_cats = set()
        idcats = int(input())
    
        #read id categories from user, save if its unique
        while(idcats != 0):
            set_cats.add(idcats)
            idcats = int(input())
    
        #save categories/product relation in DB
        for cat in set_cats:
            cursor.execute("INSERT INTO categories_products(id_product, id_category) VALUES (?,?)", (id_product, cat))
    
        conn.commit()  
    
        print("Product " + name + " sucessfully inserted!")
    
        
"""

Function: search_products

Parameters: DB cursor

Return: void

This function search for a product 
according to its parameters

"""
def search_products(cursor):
    
    #flag for valid option
    searchon = True
    
    answer = int(input("""Choose how do you want to search for a product:
               1 - By name
               2 - By description
               3 - By value
               4 - By category
               5 - Show all products
               """))
            
    if(answer < 1 or answer > 5):
        print("Invalid option!")
        searchon = False
        
    elif(answer == 1): #search by name (that is UNIQUE)   
        key_search = input("Enter the product name you want to search for: ")
        cursor.execute('SELECT * FROM products WHERE name = "'+ key_search + '"')
        
    elif(answer == 2): #search by des cription 
        key_search = input("Enter the product description you want to search for: ")
        cursor.execute('SELECT * FROM products WHERE description = "'+ key_search + '"')
            
    elif(answer == 3): #search by value
        key_search = input("Enter the product value you want to search for: ")
        cursor.execute('SELECT * FROM products WHERE value = "'+ key_search + '"')
    
    elif(answer == 4): #search by category
        show_Categories(cursor)
        key_search = input("Enter the product category you want to search for: ")
        cursor.execute('SELECT name FROM categories WHERE id = ' + key_search)
        cat_name = cursor.fetchall()
        print("Category: " + cat_name[0][0])
        cursor.execute('SELECT * FROM categories_products WHERE id_category = '+ key_search)
             
    elif(answer == 5):
        cursor.execute('SELECT * FROM products')
        
    rows = cursor.fetchall()
    
    if searchon:
        if len(rows) < 1: #if product not found
            print("ERROR! Product not found!")

        else:
            print()
            print("(id, name, description, value)")
            if(answer != 4): #show products
                for row in rows:
                    print(row)
                    print("Categories")
                    cursor.execute('SELECT id_category FROM categories_products WHERE id_product=?', (row[0],))
                    cats = cursor.fetchall()
    
                    for cat in cats:
                        cursor.execute('SELECT name FROM categories WHERE id = ' + str(cat[0]))
                        cat_name = cursor.fetchone()
                        print(cat_name[0])
            else: #retrieve products by category
                for row in rows:
                    cursor.execute('SELECT * FROM products WHERE id = ' + str(row[1]))
                    prod = cursor.fetchone()
                    print(prod)        

    return rows
    
"""

Function: update_product

Parameters: DB cursor and connection

Return: void

This function edits a product

"""
def update_product(cursor, conn):
    
    #select a product to edit
    what_products = search_products(cursor)
    
    if(len(what_products) > 0):
        #read infos
        print()
        print("Current name: " + str(what_products[0][1]))
        name = input("New name: ")
        print()
        print("Current description: " + str(what_products[0][2]))
        description = input("New description: ")
        print()
        print("Current value: " + str(what_products[0][3]))
        value = input("New value: ")
    
        print("Categories")
        cursor.execute('SELECT id_category FROM categories_products WHERE id_product=?', (what_products[0][0],))
        cats = cursor.fetchall()
        cursor.execute('DELETE FROM categories_products WHERE id_product=?', (what_products[0][0],))
        
        for cat in cats:
            cursor.execute('SELECT name FROM categories WHERE id = ' + str(cat[0]))
            cat_name = cursor.fetchone()
            print(cat_name[0])

        show_Categories(cursor)
        print("Please enter the categories ids that this product belongs to: (Enter 0 to finish)")
        set_cats = set()
        idcats = int(input())
    
        #read id categories from user, save if its unique
        while(idcats != 0):
            set_cats.add(idcats)
            idcats = int(input())
    
        #save categories/product relation in DB
        for cat in set_cats:
            cursor.execute("INSERT INTO categories_products(id_product, id_category) VALUES (?,?)", (what_products[0][0], cat))
    
        #update infos
        cursor.execute('UPDATE products SET name = ?, description = ?, value = ? WHERE id = ?', (name, description, value, what_products[0][0]))     
        conn.commit()   
    
"""

Function: delete_product

Parameters: DB cursor and connection

Return: void

This function deletes a product

"""
def delete_product(cursor, conn):
    
    #select a product to delete
    what_products = search_products(cursor)
    
    if(len(what_products) > 0):
        #confirm deletion
        confirmation = input("Are you sure you want to delete this product? (y/n)")
    
        #deletes product and categories associations
        if (confirmation == 'y' or confirmation == 'Y'):
            cursor.execute('DELETE FROM products WHERE id=?', (what_products[0][0],))
            cursor.execute('DELETE FROM categories_products WHERE id_product=?', (what_products[0][0],))
            conn.commit()        

  

