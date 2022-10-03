import sqlite3
import time
from datetime import datetime
from ticket_class import Ticket
conn = sqlite3.connect( 'ticket.db') #'ticket.db' ':memory:'

c = conn.cursor()

############# Table Creator #############
#if table doesn't exist already in DB, un-comment
# c.execute("""CREATE TABLE tickets (
#     first text,
#     last text,
#     rank text,
#     date text,
#     unit integer,
#     act_type text
#     )""")

############# Input Validators #############
def date_validator(date_text):
    #validates that date is in correct format
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def action_validator():
    #validates that action is one of 4 types only
    n=-1 # helps track if loop is in first iteration or not
    while True:
        if n<0: # first interation of loop
            act_type = input('Please enter type of action. Pay, Epat, iPERMS or admin: ')
            act_type = act_type.lower()
            if act_type == 'pay' or act_type == 'admin' or act_type == 'iperms' or act_type=='epat':
                return act_type
            else:
                n+=1
        else: #not first iteration of loop. Means not valid input from first loop on
            act_type = input('Input must be pay, Epat, iPERMS or admin only. Please try again: ')
            act_type = act_type.lower()
            if act_type == 'pay' or act_type == 'admin' or act_type == 'iperms' or act_type=='epat':
                return act_type

############# SQL #############
def insert_ticket(new_ticket):
    #Inserts ticket into ticket table based off inputs from calling fuction
    with conn: #no longer need of commit statment
        c.execute("INSERT INTO tickets VALUES (:first, :last, :rank, :date, :unit, :act_type)" ,
              {'first':new_ticket.first, 'last':new_ticket.last, 'rank':new_ticket.rank, 'date':new_ticket.date,
               'unit':new_ticket.unit, 'act_type':new_ticket.act_type })

def delete_ticket(first,last, rank,date, unit, act_type):
    #Deletes ticket using SQL based on inputs from calling function
    with conn:
        c.execute("DELETE FROM tickets WHERE first=:first AND last =:last AND rank = :rank AND date =:date AND unit = :unit AND act_type= :act_type" ,
                  {'first': first, 'last': last, 'rank': rank, 'date': date,
                   'unit': unit, 'act_type': act_type} )


def get_insert_inputs():
    #Gets input from the user, then sends inputs to the insert function
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

def get_delete_inputs():
    #Gets inputs for the user and then sends those inputs to the delete function
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

    delete_ticket(f_name, l_name, rank, date, unit, act_type)

def get_totals(outer_loop):
    while not outer_loop:
        inp=input('Totals by unit, action type or all?: ')
        inp=inp.lower()
        with conn:
            if inp=='all':
                c.execute("SELECT COUNT(*) FROM tickets")
                print(str(c.fetchall()[0][0]) + ' total actions completed') # to get to the element in the list tuple
                outer_loop=True

            elif inp== 'unit':
                unit=input('Please under unit ID: ')
                c.execute("SELECT COUNT(*) FROM tickets WHERE unit = :unit ", {'unit': unit})
                print(str(c.fetchall()[0][0]) + ' from the ' + str(unit))
                outer_loop = True

            elif inp== 'action type':
                loop_token=False
                while not loop_token:
                    act_type=input('Please enter pay, admin, iPERMS or Epat: ')
                    act_type=act_type.lower()
                    if act_type == 'pay' or act_type == 'admin' or act_type == 'iperms' or act_type == 'epat':
                        c.execute("SELECT COUNT(*) FROM tickets WHERE act_type = :act_type ", {'act_type': act_type})
                        print(str(c.fetchall()[0][0]) + ' ' + act_type + ' actions')
                        loop_token=True
                        outer_loop = True
                    else:
                        print('Action type not recognized, please try again.')

            else:
                print('Action type not recognized, please try again.')




############# Action Loop #############
token=-1 # used to track if first action or not
#need to add verification
while token<0:
    inp=input("Tell me why you are here. Enter ADD, DELETE, TOTALS: ")
    inp=inp.lower()
    if inp=="add":
        get_insert_inputs()
    elif inp=="delete":
        get_delete_inputs()
    elif inp=="totals":
        get_totals(False)
    inp = input("Would you like to complete another action? Y/N: ")
    inp=inp.lower()
    if inp=="n" or inp=="no":
        token+=1
print('Goodbye')


c.execute("SELECT * from tickets")
#
print(c.fetchall())

conn.close()