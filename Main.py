import tkinter as tk
from tkinter import filedialog, Text
from Create_Batch import create_fun
import os

def startup():
    root = tk.Tk()
    root.title('Sir Special')
    root.geometry("600x650")
    root.resizable(0, 0)

    def addfiles():
        for widget in frame.winfo_children():
            widget.destroy()

        filename = filedialog.askopenfilenames(initialdir='/', title='Select file',
                                              filetypes=(("all files", "*.*"), ("executables", "*.exe")))
        filename = list(filename)

        for i in filename:
            i = r'{}'.format(i)
            files.append(i)

        for file in files:
            lable = tk.Label(frame, text=file, bg='white')
            lable.pack()

    def get_batch():
        import mysql.connector

        try:
            mycon = mysql.connector.connect(host='localhost', charset='utf8', user='root', passwd='root',
                                            database='sirspecial')
            query = '''show tables'''
            cur = mycon.cursor()
            cur.execute(query)
            record = cur.fetchall()
            for rec in record:
                for r in rec:
                    batches.append(r)
        except Exception as e:
            print('Error occured :', e)
        finally:
            mycon.close()

    def choose_batch():
        import tkinter as tk
        from tkinter import ttk
        batch = []
        def table():
            batch.append(name_of_batches.get())
            global send_files_to
            send_files_to = batch
            print(send_files_to[0])

            window.destroy()

        window = tk.Tk()
        window.title('Batches')
        window.geometry('500x250')
        window.resizable(0,0)
        ttk.Label(window, text="Vowtech Batches",
                  background='green', foreground="white",
                  font=("Times New Roman", 15)).grid(row=0, column=1)

        get_batch()
        
        ttk.Label(window, text="Select the Batch :",
                  font=("Times New Roman", 10)).grid(column=0,
                                                     row=5, padx=10, pady=25)

        n = tk.StringVar()
        name_of_batches = ttk.Combobox(window, width=27, textvariable=n)

        name_of_batches['values'] = batches

        name_of_batches.grid(column=1, row=5)
        name_of_batches.current()
        openfile = tk.Button(window, text='Select Batch', padx=10, pady=5, fg='white', bg='#263D42', command=table)
        openfile.grid()
        window.mainloop()

    def get_emails():
        import mysql.connector
        print(send_files_to)
        try:
            mycon = mysql.connector.connect(host='localhost', charset='utf8', user='root', passwd='root',
                                            database='sirspecial')
            query = f'SELECT emailid FROM {send_files_to[0]}'
            cur = mycon.cursor()
            cur.execute(query)
            record = cur.fetchall()
            for rec in record:
                for r in rec:
                    email_ids.append(r)

        except Exception as e:
            print('Error occured :', e)
        finally:
            mycon.close()

    def send_email():
        
        def success_msg():
            from tkinter import messagebox
            messagebox.showinfo('Success','Mail send successfully')
        
        def fail_msg():
            from tkinter import messagebox
            messagebox.showerror('Fail','Mail send failed')
        
        import os
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        from email.mime.base import MIMEBase
        from email import encoders
        import func_support

        email_user = 't.kabade07@gmail.com'
        email_password = func_support.password
        get_emails()
        reciver_list = email_ids
        email_send = ''
        print(reciver_list)
        for i in range(0, len(reciver_list)):
            if i == 0:
                email_send += reciver_list[i]
            else:
                email_send += ','
                email_send += reciver_list[i]
        print(email_send)
        subject = 'email using python'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = 'Hi there, sending this email from Python!'
        msg.attach(MIMEText(body, 'plain'))

        for file in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(file, 'rb').read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % os.path.basename(file))
            msg.attach(part)

        text = msg.as_string()
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send.split(','), text)
        except Exception as e:
            print('Error',e)
            fail_msg()
        else:
            print('send success')
            success_msg()
            server.quit()
            


    canvas = tk.Canvas(root, height=600, width=600, bg="dim gray")
    canvas.pack()

    frame = tk.Frame(root, bg='#263D42')
    frame.place(relwidth=0.8, relheight=0.75, relx=0.1, rely=0.1)

    create = tk.Button(root, text='Create a Batch', padx=10, pady=5, fg='white', bg='#263D42', command=create_fun).place(x=45,y=610)
    openfile = tk.Button(root, text='Open file', padx=10, pady=5, fg='white', bg='#263D42', command=addfiles).place(x=205,y=610)
    batch = tk.Button(root, text='Batches', padx=10, pady=5, fg='white', bg='#263D42', command=choose_batch).place(x=345, y=610)
    send_mail = tk.Button(root, text='Send mail', padx=10, pady=5, fg='white', bg='#263D42', command=send_email).place(x=475, y=610)


    root.mainloop()

if __name__=='__main__':
    send_files_to = []
    files = []
    batches = []
    email_ids = []
    batch_sheet = []
    startup()