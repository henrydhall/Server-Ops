# A reminder system for my to-do lists.
from audioop import add
import re
import sqlite3, datetime

from colorama import Cursor

#TODO: primary key
#https://www.khanacademy.org/computer-programming/sql-create-table-with-a-primary-key/5189331400654848
#as from here

def create_table():
    connection = sqlite3.connect('to_do.db')

    try:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE to_do_items \
            (Name TEXT, due_date DATE, priority REAL, \
            related_people TEXT, reminder_frequency REAL, \
            id INTEGER PRIMARY KEY,\
            completed BOOLEAN DEFAULT 0)')
    except sqlite3.Error:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()

def reset_table():
    connection = sqlite3.connect('to_do.db')
    try:
        cursor = connection.cursor()
        cursor.execute('drop table to_do_items;')
        create_table()
    except sqlite3.Error:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()

def add_item(name, due_date, priority, related_people = None, reminder_frequency = 0):
    connection = sqlite3.connect('to_do.db')

    if related_people is None:
        related_people = 'NULL'
    else:
        related_people = '\"' + related_people + '\"'

    try:
        cursor = connection.cursor()
        add_query = f'INSERT INTO to_do_items (name, due_date, priority, related_people, reminder_frequency) VALUES(\"{name}\", \"{due_date}\", {priority}, {related_people}, {reminder_frequency});'
        print(add_query)
        cursor.execute( add_query )
    except sqlite3.Error:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()

def get_all_items():
    connection = sqlite3.connect('to_do.db')
    try:
        cursor = connection.cursor()
        select_query = f'SELECT * FROM to_do_items;'
        cursor.execute( select_query )
        results = cursor.fetchall()
    except sqlite3.Error:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()
    
    return results

def get_incomplete_items():
    #TODO: order by due date, priority
    connection = sqlite3.connect('to_do.db')
    try:
        cursor = connection.cursor()
        select_query = f'SELECT * FROM to_do_items WHERE completed = 0;'
        cursor.execute( select_query )
        results = cursor.fetchall()
    except sqlite3.Error:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()
    
    return results

def get_incomplete_items_as_string():
    items_string = 'To-do List'.center(40,'*') + '\n'
    items = get_incomplete_items()
    for i in range( len(items) ):
        items_string = items_string + get_item_as_string( items[i] )
        if i != len(items)-1:
            items_string += '\n'
    return items_string

def get_item_as_string(item):
    #Good initial option, I'll do another
    item_string = ''
    item_string = f'{item[0]}: \n\tDue: {item[1]} \n\tPriority: {int(item[2])} \n\tPeople to talk to: {item[3]} \n\tID: {int(item[4])}'
    item_string = ''
    item_string = item_string + item[0] + ':\n'
    item_string = item_string + ('Due: ' + item[1]).ljust(20) + ( 'Priority: ' + str(item[2])).rjust(20) + '\n'
    item_string = item_string + ('ID: ' + str(int(item[4]))).ljust(20) + ('People: ' + str(item[3]) ).rjust(20)
    return item_string

def get_all_items_as_string():
    items_string = 'To-do List'.center(40,'*') + '\n'
    items = get_all_items()
    for i in range( len(items) ):
        items_string = items_string + get_item_as_string( items[i] )
        if i != len(items)-1:
            items_string += '\n'
    return items_string

def seed_items():
    add_item( 'Finish this', str(datetime.date(2022,7,1)) ,'1', related_people=None, reminder_frequency= 0 )
    add_item( 'Make it a web app', str(datetime.date(2022,8,1)) ,'1', related_people=None, reminder_frequency= 0 )
    add_item( 'Get around google', str(datetime.date(2022,9,1)) ,'1', related_people=None, reminder_frequency= 0 )


if __name__ == '__main__':
    pass
    #create_table()
    #reset_table()
    #results = get_all_items() 
    print( get_incomplete_items_as_string() )
    #seed_items()
