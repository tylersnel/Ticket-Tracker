import sqlite3
import time
from datetime import datetime
from ticket_class import Ticket
conn = sqlite3.connect(':memory:') #'ticket.db'

c = conn.cursor()

c.execute("""CREATE TABLE ticket (
    first text,
    last text,
    rank text,
    date text,
    unit integer,
    type text
    )""")

############# Input Validators #############
def date_validator(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def action_validator():
    n=-1
    while True:
        if n<0:
            act_type = input('Please enter type of action. Pay, admin or iPERMS: ')
            act_type = act_type.lower()
            if act_type == 'pay' or act_type == 'admin' or act_type == 'iperms':
                return act_type
            else:
                n+=1
        else:
            act_type = input('Input must be Pay, admin or iPERMS only. Please try again: ')
            act_type = act_type.lower()
            if act_type == 'pay' or act_type == 'admin' or act_type == 'iperms':
                return act_type

############# SQL #############
def insert_ticket(new_ticket):
    with conn: #no longer need of commit statment
        c.execute("INSERT INTO ticket VALUES (:first, :last, :rank, :date, :unit, :type)" ,
              {'first':new_ticket.first, 'last':new_ticket.last, 'rank':new_ticket.rank, 'date':new_ticket.date, 'unit':new_ticket.unit, 'type':new_ticket.type })

def delete_ticket(ticket):
    with conn:
        c.execute()


inp= input("Here to add a ticker? Y/N: ")
inp=inp.lower()

if inp == 'yes' or inp=='y':
    f_name=input('Please enter First Name: ')
    l_name = input('Please enter Last Name: ')

    rank = input('Please enter rank, 3 letter format only: ')
    while len(rank)!=3:# verify length. 3 letter format only
        rank = input('Incorrect format. Please enter rank, 3 letter format only: ')

    date = input('Please enter date (YYYY-MM-DD): ')
    if not date_validator(date):
        date = input('Incorrect format. Please enter date (YYYY-MM-DD): ')
        date_validator(date)


    unit = input('Please enter unit: ')

    act_type=action_validator()


    sm=Ticket(f_name, l_name, rank, date, unit, act_type)
    insert_ticket(sm)

elif inp == 'no' or inp=='n':
    inp = input('Are you here to delete a ticket?: Y/N: ')
    inp = inp.lower()

    if inp == 'yes' or inp == 'y':
        print("!WARNING! THIS WILL DELETE TICKET BASED ON INFO GIVEN")
        time.sleep(3)
        f_name = input('Please enter First Name: ')
        l_name = input('Please enter Last Name: ')

        rank = input('Please enter rank, 3 letter format only: ')
        while len(rank) != 3:  # verify length. 3 letter format only
            rank = input('Incorrect format. Please enter rank, 3 letter format only: ')

        date = input('Please enter date (YYYY-MM-DD): ')
        if not date_validator(date):
            date = input('Incorrect format. Please enter date (YYYY-MM-DD): ')
            date_validator(date)

        unit = input('Please enter unit: ')

        act_type = action_validator()


# conn.commit()

# sm_1= Ticket('TJ', 'Sorensen', 'SFC', '9/26/22', 405, 'pay')
# print(sm_1.unit)
c.execute("SELECT * from ticket WHERE first='Tyler'")
#
print(c.fetchall())

conn.close()