import sqlite3
import time
from datetime import datetime
from ticket_class import Ticket
conn = sqlite3.connect( 'ticket.db') #'ticket.db' ':memory:'

c = conn.cursor()

############# Table Creator #############
#if table doesn't exist already in DB, un-comment
# c.execute("""CREATE TABLE tickets (
#      last text,
#      date text,
#      act_type text,
#      tl_num text
#      )""")

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
        c.execute("INSERT INTO tickets VALUES ( :last, :date, :act_type, :tl_num)" ,
              { 'last':new_ticket.last,  'date':new_ticket.date,
                'act_type':new_ticket.act_type, 'tl_num' :new_ticket.tl_num })

def delete_ticket(last, date, act_type):
    #Deletes ticket using SQL based on inputs from calling function
    with conn:
        c.execute("DELETE FROM tickets WHERE last =:last AND date =:date AND act_type= :act_type" ,
                  {'last': last, 'date': date, 'act_type': act_type} )

def get_update_inputs():
    last=input('Please enter last name: ')
    date=input('Please enter date: ')
    tl_num=input('Please enter TL number: ')
    update_ticket_tl(last, date, tl_num)

def update_ticket_tl(last, date, tl_num):
    with conn:
        c.execute(
            "UPDATE tickets SET tl_num= :tl_num WHERE last =:last AND date =:date",
            {'tl_num': tl_num, 'last': last, 'date': date})

def get_totals(outer_loop):
    # function that prints out total actions completed by type.
    # recieves a False variable for outer loop. If command not recognized,
    # loop starts again. If recognized, loop ends and prints totals.
    # returns nothing.
    while not outer_loop:
        inp=input('Totals by action type or all? Type return to go back: ')
        inp=inp.lower()
        with conn:
            if inp=='return':
                outer_loop=True
            elif inp=='all':
                c.execute("SELECT COUNT(*) FROM tickets")
                print(str(c.fetchall()[0][0]) + ' total actions completed') # to get to the element in the list tuple
                outer_loop=True

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

def get_insert_inputs():
    #Gets input from the user, then sends inputs to the insert function
    l_name = input('Please enter Last Name: ')

    date = input('Please enter date (YYYY-MM-DD): ')
    if not date_validator(date):
        date = input('Incorrect format. Please enter date (YYYY-MM-DD): ')
        date_validator(date)

    act_type=action_validator()

    if act_type=='pay':
        loop_val=False
        while not loop_val:
            tl_num=input('Enter TL number if you have it, press enter if you do not: ')
            if tl_num.isdigit() or not tl_num:
                sm = Ticket(l_name, date, act_type, tl_num)
                loop_val = True
            else: print('Invalid input. Try again')


    else:
        sm=Ticket(l_name, date, act_type, None) #non-pay action won't have TL number, so set to none
    print(sm.tl_num)
    insert_ticket(sm)

def get_delete_inputs():
    #Gets inputs for the user and then sends those inputs to the delete function
    print("!WARNING! THIS WILL DELETE TICKET BASED ON INFO GIVEN")
    time.sleep(3)
    l_name = input('Please enter Last Name: ')

    date = input('Please enter date (YYYY-MM-DD): ')
    if not date_validator(date):
        date = input('Incorrect format. Please enter date (YYYY-MM-DD): ')
        date_validator(date)

    act_type = action_validator()

    delete_ticket(l_name, date, act_type)

############# Action Loop #############

    #need to add verification
outer_loop=False
while not outer_loop:
    inner_loop=False
    while not inner_loop:
        inp = input("Tell me why you are here. Enter ADD, DELETE, UPDATE TL or TOTALS: ")
        inp = inp.lower()
        if inp=="add":
            get_insert_inputs()
            inner_loop=True
        elif inp=="delete":
            get_delete_inputs()
            inner_loop=True
        elif inp=="totals":
            get_totals(False)
            inner_loop=True
        elif inp=="update tl":
            get_update_inputs()
            inner_loop=True
        else:
            print("Input not recognized. Try again.")
    inp = input("Would you like to complete another action? Y/N: ")
    inp=inp.lower()
    if inp=="n" or inp=="no":
        outer_loop=True
        print("Goodbye")


#
# c.execute("DROP TABLE tickets")

c.execute("SELECT * from tickets")
#
print(c.fetchall())

conn.close()