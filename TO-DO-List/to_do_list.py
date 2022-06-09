# A reminder system for my to-do lists.
import sqlite3, datetime

#TODO: primary key
#https://www.khanacademy.org/computer-programming/sql-create-table-with-a-primary-key/5189331400654848
#as from here

def create_table():
    connection = sqlite3.connect('to_do.db')

    try:
        cursor = connection.cursor()
        cursor.execute('CREATE TABLE to_do_items \
            (Name TEXT, due_date DATE, priority REAL, \
            related_people TEXT, reminder_frequency REAL, id INTEGER)')
    except sqlite3.Error:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()

def add_item(name, due_date, priority, related_people = None, reminder_frequency = 0):
    connection = sqlite3.connect('to_do.db')

    try:
        cursor = connection.cursor()
        add_query = f'INSERT INTO to_do_items (name, due_date, priority, related_people, reminder_frequency) VALUES(\"{name}\", \"{due_date}\", {priority}, \"{related_people}\", {reminder_frequency});'
        #TODO: figure out how to insert null items...the python to sql jump catches me.
        print(add_query)
        cursor.execute( add_query )
    except sqlite3.Error:
        connection.rollback()
        raise
    else:
        connection.commit()
    finally:
        connection.close()

if __name__ == '__main__':
    add_item( 'finish this', str(datetime.date(2022,7,1)) ,'1', related_people=None, reminder_frequency= 0 )