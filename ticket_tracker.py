import sqlite3
from datetime import datetime
from actiontracker import Ticket
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

def date_validator(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def insert_ticket(new_ticket):
    with conn: #no longer need of commit statment
        c.execute("INSERT INTO ticket VALUES (:first, :last, :rank, :date, :unit, :type)" ,
              {'first':new_ticket.first, 'last':new_ticket.last, 'rank':new_ticket.rank, 'date':new_ticket.date, 'unit':new_ticket.unit, 'type':new_ticket.type })


inp= input("Here to add a ticker? Y/N: ")
inp=inp.lower()

if inp == 'yes' or inp=='y':
    # f_name=input('Please enter First Name: ')
    # l_name = input('Please enter Last Name: ')
    #
    # rank = input('Please enter rank, 3 letter format only: ')# add verifier
    # while len(rank)!=3:
    #     rank = input('Please enter rank, 3 letter format only: ')

    date = input('Please enter date (YYYY-MM-DD): ')
    if not date_validator(date):
        date = input('Please enter date (YYYY-MM-DD): ')
        date_validator(date)


    unit = input('Please enter unit: ')
    act_typ = input('Please enter type of action: ')

    sm=Ticket(f_name, l_name, rank, date, unit, act_typ)
    insert_ticket(sm)

else:
    print("Adios")


# conn.commit()

# sm_1= Ticket('TJ', 'Sorensen', 'SFC', '9/26/22', 405, 'pay')
# print(sm_1.unit)
c.execute("SELECT * from ticket WHERE first='Tyler'")
#
print(c.fetchall())

conn.close()