from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import time
import PizzaDecorator

# make database and users (if not exists already) table at programme start up
with sqlite3.connect('database.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT NOT NULL ,password TEXT NOT NULL);')
c.execute('CREATE TABLE IF NOT EXISTS orders (username TEXT NOT NULL, order_num  TEXT NOT NULL,price INT);')
db.commit()
db.close()

class main:
    def __init__(self,master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        #Create Widgets
        self.widgets()

    #Login Function
    def login(self):
    	#Establish Connection
        with sqlite3.connect('database.db') as db:
            c = db.cursor()

        find_user = ('SELECT * FROM users WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        if self.username.get()=="admin" and self.password.get()=="admin":
            self.logf.pack_forget()
            self.admin_b_seeorders.place(x=50,y=150)
            self.admin_b_income.place(x=400,y=150)
            
            
        elif result:
            #login page for user
            self.logf.pack_forget()
            self.label_main.place(x=50,y=150)
            self.label2_main.place(x=500,y=150)
            self.p1.place(x=50,y=350)
            self.p2.place(x=500,y=350)
            self.l1.place(x=50,y=410)
            self.b1.place(x=50,y=450)
            self.b2.place(x=50,y=490)
            self.label_extention.place(x=500,y=410)
            self.b_tomato.place(x=500,y=450)
            self.b_cheese.place(x=500,y=490)
            self.b_chicken.place(x=500,y=530)
            self.b_order.place(x=50,y=600)
            self.b_prev.place(x=50,y=638)
            
            
            
        else:
            ms.showerror('Username Not Found.')
    def show_income(self):
        with sqlite3.connect('database.db') as db:
            c=db.cursor()
        result = [x[0] for x in c.execute("SELECT price FROM orders")]
        count=0
        for i in result:
            count+=i
        string="Current income: "+str(count)
        self.admin_l1=Label(self.master,text=string,font=("arial",20))
        self.admin_l1.place(x=225,y=250)
            
    def show_history(self):
        with sqlite3.connect('database.db') as db:
            c=db.cursor()
        result1=[x[0] for x in c.execute('SELECT username FROM orders')]
        result2=[x[0] for x in c.execute('SELECT order_num FROM orders')]
        for i in range(len(result1)):
            print(result1[i],result2[i])
            
    def create_pizza(self,a):
        if a=="Margarita":
            self.pizza=pizza_backend.PizzaBuilder(a)
        elif a=="Barbeque":
            self.pizza=pizza_backend.PizzaBuilder(a)

    def add_remove(self,pizza_type,extention,choice):
        if choice=="add":
            self.pizza.add_extention(extention)
        elif choice=="remove":
            self.pizza.remove_extention(extention)

    def order_price(self,pizza):
        with sqlite3.connect('database.db') as db:
            c=db.cursor()
        insert='INSERT INTO orders(username,order_num,price) VALUES(?,?,?)'
        c.execute(insert,[(self.username.get()),(self.pizza.get_status()),(self.pizza.get_price())])
        db.commit()
        ms.showinfo('Price','Your order is {} manat'.format(self.pizza.get_price()))
        

    def previous_order(self):
        with sqlite3.connect('database.db') as db:
            c=db.cursor()
        find_user=('SELECT * FROM orders WHERE username=?')
        c.execute(find_user,[(self.username.get())])
        result=c.fetchall()
        print("Username is",result[0][0])
        for i in result:
            print("Order:",i[1],end="|")
            print("Price:",i[2],"manat")

    def sign_up(self):
    	#Establish Connection
        with sqlite3.connect('database.db') as db:
            c = db.cursor()

        #Find Existing username if any take proper action
        find_user = ('SELECT * FROM users WHERE username = ?')
        c.execute(find_user,[(self.username.get())])        
        if c.fetchall():
            ms.showerror('This username belongs an user,try another one!')
        else:
            ms.showinfo('Success!','You have sing up!')
            self.log()
        #Create New Account 
        insert = 'INSERT INTO users(username,password) VALUES(?,?)'
        c.execute(insert,[(self.n_username.get()),(self.n_password.get())])
        db.commit()

        #Frame Packing Methords
    def log(self):
        self.username.set('')
        self.password.set('')
        self.reg.pack_forget()
        self.head['text'] = 'Pizza Time - Green Pizza Store'
        self.logf.pack()
    def create_new_account(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create New Account'
        self.reg.pack()

    
        
    def widgets(self):
        self.head = Label(self.master,text = 'Pizza Time - Green Pizza Store',font = ('',35),pady = 10)
        self.head.pack()
        
        self.logf = Frame(self.master,padx =20,pady = 20)
        Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.logf,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid()
        Button(self.logf,text = ' Create New Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.create_new_account).grid(row=2,column=1)
        self.logf.pack()
        
        self.reg = Frame(self.master,padx =10,pady = 10)
        Label(self.reg,text = 'E-mail: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.reg,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.reg,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.reg,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=1,column=1)
        Label(self.reg,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.reg,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=2,column=1)
        Button(self.reg,text = 'Create New Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.sign_up).grid()
        Button(self.reg,text = 'Go to Login',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=3,column=1)

        #main page widgets    
        self.label_main=Label(self.master)
        self.label_main.img=ImageTk.PhotoImage(file="pizza_2.jpg")
        self.label_main.config(image=self.label_main.img)
        self.label_main.pack_forget()

        self.label2_main=Label(self.master)
        self.label2_main.img=ImageTk.PhotoImage(file="pizza_1.jpg")
        self.label2_main.config(image=self.label2_main.img)
        self.label2_main.pack_forget()

        self.p1=Label(self.master,text="Margarita",font=("arial",20),bg="green")
        self.p1.pack_forget()
        self.p2=Label(self.master,text="Barbeque",font=("arial",20),bg="green")
        self.p2.pack_forget()
        self.l1=Label(self.master,text="Choose your order",font=("arial",20))
        self.l1.pack_forget()

        self.v=IntVar()

        self.b1=Radiobutton(self.master,variable=self.v,value=1,text="Margarita",font=('',15),command=lambda:self.create_pizza("Margarita"))
        self.b2=Radiobutton(self.master,variable=self.v,value=2,text="Barbeque",font=('',15),command=lambda:self.create_pizza("Barbeque"))
        self.b1.pack_forget()
        self.b2.pack_forget()
        
        self.label_extention=Label(self.master,text="Add extention",font=("arial",20))
        self.label_extention.pack_forget()
        self.b_tomato=Button(self.master,text="Tomato",bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Tomato","add"))
        self.b_tomato.pack_forget()
        self.b_cheese=Button(self.master,text="Cheese",bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Cheese","add"))
        self.b_cheese.pack_forget()
        self.b_chicken=Button(self.master,text="Chicken",bd=3,font=('',15),command=lambda:self.add_remove(self.pizza,"Chicken","add"))
        self.b_chicken.pack_forget()

        self.b_order=Button(self.master,text="order",bd=3,font=('',15),command=lambda:self.order_price(self.pizza))
        self.b_order.pack_forget()
        self.b_prev=Button(self.master,text="See previous orders",bd=3,font=('',15),command=lambda:self.previous_order())
        self.b_prev.pack_forget()

        self.admin_b_seeorders=Button(self.master,text="See all orders",bd=3,font=('arial',20),bg="green",command=lambda:self.show_history())
        self.admin_b_seeorders.pack_forget()
        self.admin_b_income=Button(self.master,text="Income",bd=3,font=('arial',20),bg="green",command=lambda:self.show_income())
        self.admin_b_income.pack_forget()




    
#create window and application object
root = Tk()
root.geometry("1000x1000")


#root.title("Login Form")
main(root)
root.mainloop()
