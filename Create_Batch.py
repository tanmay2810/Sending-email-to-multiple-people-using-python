from BatchName import create_acc_call

def fail_msg():
    from tkinter import messagebox
    messagebox.showerror('Fail','Batch creation Failed')

def success_msg():
    from tkinter import messagebox
    messagebox.showinfo('Success','Batch created successfully')
    

def insert_table_values():
    import mysql.connector
    
    print(records_to_insert, 'insert_table')
    print(batch_name, 'insert_table')
    table_name = batch_name[0]
    try:
        mycon = mysql.connector.connect(host='localhost', charset='utf8', user='root', passwd='root',
                                        database='sirspecial')
        print(mycon)
        query = f'''insert into {table_name}(name, emailid) values(%s,%s)'''
        cur = mycon.cursor()
        cur.executemany(query, records_to_insert)
        print(cur)
    except Exception as e:
        print('Error occured :', e)
        mycon.rollback()
        fail_msg()
    else:
        mycon.commit()
        print('Data insertion success.')
        success_msg()
    finally:
        mycon.close()

def insert_table():
    import mysql.connector
    
    print(records_to_insert,'insert_table')
    print(batch_name,'insert_table')
    table_name = batch_name[0]
    try:
        mycon = mysql.connector.connect(host='localhost', charset='utf8', user='root', passwd='root', database='sirspecial')
        print(mycon)
        query1 = f'''create table {table_name}(
name varchar(25) not null,
emailid varchar(20) not null)'''
        cur = mycon.cursor()
        cur.execute(query1)
        print(cur)
    except Exception as e:
        print('Error occured :',e)
        fail_msg()
        mycon.rollback()
    else:
        mycon.commit()
        print('Data insertion success.')
        insert_table_values()
    finally:
        mycon.close()

def create():
        import pandas as pd
        
        print(batch_sheet)
        filepath = batch_sheet[0]
        df = pd.read_excel(f'{filepath}')
        file = filepath.split('.')[0].split('/')[-1]
        print(file)
        global batch_name
        batch_name.append(file)
        name_std = []
        emailid = []

        for i in df['name']:
            name_std.append(i)

        for i in df['email id']:
            emailid.append(i)

        rowset = []
        tup = ()
        for i in range(0, len(name_std)):
            tup = (name_std[i], emailid[i])
            print(tup)
            rowset.append(tup)
        global records_to_insert
        records_to_insert = rowset
        print(records_to_insert)
        insert_table()

def choose_file():
    from tkinter import filedialog

    sheet = filedialog.askopenfilenames(initialdir='/', title='Select file',filetypes=(("all files", "*.*"), ("executables", "*.exe")))
    sheet = list(sheet)

    path = []
    for i in sheet:
        i = r'{}'.format(i)
        path.append(i)
    global batch_sheet
    batch_sheet = path
    print(batch_sheet[0])
    create()


def create_fun():
    global  branch_sheet
    global  records_to_insert
    global  batch_name
    branch_sheet = []
    records_to_insert = []
    batch_name = []
    choose_file()