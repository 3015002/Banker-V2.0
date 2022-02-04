import tkinter as tk
import numpy as np
import time as time
import pandas as pd
from pandastable import Table, TableModel


BookGUI = tk.Tk()
BookGUI.title('Millionaire Banker GUI V0.1')
BookGUI.geometry('810x600')
BookGUI.configure(background='white')


def SaveData():
    time_touse = time.strftime("%Y%m%d%H", time.localtime(time.time()))
    Info_toShow =  'Bank Data Saved to '+'BankData'+time_touse+'.csv'
    InfoLabel_toShow.set(Info_toShow)
    table_toshow.to_csv('BankData'+time_touse+'.csv')
    
def ShowSelection():
    PayerID = int(PayerButton.get())
    PayeeID = int(PayeeButton.get())
    Payer = PlayerList[PayerID]
    Payee = PlayerList[PayeeID]
    print(Payer) 
    print(Payee) 
    
def ResetBalance():
    # Reset balance of every one to initial amount
    msgbox_reset_response = tk.messagebox.askokcancel(title='Reset Balance', message="Are You Sure To Reset Balance?")
    # if confirmed to go ahead
    if msgbox_reset_response:
        table_toshow[:] = Init_Amt
        print(table_toshow)
        pt.model.pd = table_toshow
        pt.redraw()
        #pt = Table(frame, dataframe=table_toshow,width=600, height=150)
        #pt.show()
        #pt.showIndex()
    
        
def calculate_positions():
    # Get inputs
    PayerID = int(PayerButton.get())
    PayeeID = int(PayeeButton.get())
    Payer = PlayerList[PayerID]
    Payee = PlayerList[PayeeID]
    DoubleConfirm = Ckbox_Confirm.get()
    # Get amount to pay
    if not Amt2PayBox_K.get():
        Amt2Pay_K = 0
    else:
        Amt2Pay_K = int(Amt2PayBox_K.get())
            
    Info_toShow = Payer + ' just paid ' + Payee + " " + str(Amt2Pay_K) 
    Info2Show_0 = Payer + ' to pay ' + Payee + " " + str(Amt2Pay_K)  + "?" 
          
    if Payer == 'Everyone':
        if Payee == 'Everyone':
            # payer payee not valid
            tk.messagebox.showwarning(title='Wrong Payee/Payer', message="Choose Payer/Payee Again")
        else:
            # check balance, if anyone not enough balance
            if any(table_toshow.loc[PlayerList[1:5],'Balance'] < Amt2Pay_K):
                ListBroke = np.where(table_toshow.loc[PlayerList[1:5],'Balance'] <Amt2Pay_K)[0]
                NameListBorke = " ".join(table_toshow.index[ListBroke+1])
                tk.messagebox.showwarning(title='Not Enough Balance', message=NameListBorke +" Not Enough Balance, Try Mortgage")
            else:
                # calculate payment
                # if double confirm is required
                if DoubleConfirm == 1:
                    msgbox_compute_response = tk.messagebox.askokcancel(title='Transfer Details', message=Info2Show_0)
                
                    if msgbox_compute_response:                
                        table_toshow['Initial'] = table_toshow['Balance']
                        table_toshow.loc[PlayerList[1:5],'Balance'] -=Amt2Pay_K
                        table_toshow.loc[Payee,'Balance'] +=Amt2Pay_K*NumPlayer
                                        
                        pt.model.pd = table_toshow
                        pt.redraw() 
                        InfoLabel_toShow.set(Info_toShow)
                else:
                    table_toshow['Initial'] = table_toshow['Balance']
                    table_toshow.loc[PlayerList[1:5],'Balance'] -=Amt2Pay_K
                    table_toshow.loc[Payee,'Balance'] +=Amt2Pay_K*NumPlayer
                                    
                    pt.model.pd = table_toshow
                    pt.redraw()       
                    InfoLabel_toShow.set(Info_toShow)

                
    elif Payee == 'Everyone':
        # check balance
        if table_toshow.loc[Payer,'Balance'] < Amt2Pay_K*NumPlayer:
            tk.messagebox.showwarning(title='Not Enough Balance', message="Not Enough Balance, Try Mortgage")
        else:
            # calculate payment
            # if double confirm is required
            if DoubleConfirm == 1:
                msgbox_compute_response = tk.messagebox.askokcancel(title='Transfer Details', message=Info2Show_0)
                if msgbox_compute_response:                
                    table_toshow['Initial'] = table_toshow['Balance']
                    table_toshow.loc[Payer,'Balance'] -=Amt2Pay_K*NumPlayer
                    table_toshow.loc[PlayerList[1:5],'Balance'] +=Amt2Pay_K
                    
                    pt.model.pd = table_toshow
                    pt.redraw()                       
                    InfoLabel_toShow.set(Info_toShow)
            else:
                table_toshow['Initial'] = table_toshow['Balance']
                table_toshow.loc[Payer,'Balance'] -=Amt2Pay_K*NumPlayer
                table_toshow.loc[PlayerList[1:5],'Balance'] +=Amt2Pay_K
                
                pt.model.pd = table_toshow
                pt.redraw()   
                InfoLabel_toShow.set(Info_toShow)
                    
    else:
        if table_toshow.loc[Payer,'Balance'] < Amt2Pay_K:
            tk.messagebox.showwarning(title='Not Enough Balance', message="Not Enough Balance, Try Mortgage")
        else:           
            Info2Show_0 = Payer + ' to pay ' + Payee + " " + str(Amt2Pay_K)  + "?" 
            if DoubleConfirm == 1:
                
                msgbox_compute_response = tk.messagebox.askokcancel(title='Transfer Details', message=Info2Show_0)
                if msgbox_compute_response:                
                    table_toshow['Initial'] = table_toshow['Balance']
                    table_toshow.loc[Payer,'Balance'] -=Amt2Pay_K
                    table_toshow.loc[Payee,'Balance'] +=Amt2Pay_K
            
                    pt.model.pd = table_toshow
                    pt.redraw()   
                    InfoLabel_toShow.set(Info_toShow)
            else:
                table_toshow['Initial'] = table_toshow['Balance']
                table_toshow.loc[Payer,'Balance'] -=Amt2Pay_K
                table_toshow.loc[Payee,'Balance'] +=Amt2Pay_K
            
                pt.model.pd = table_toshow
                pt.redraw()   

                InfoLabel_toShow.set(Info_toShow)
    #return positions

NumPlayer = 4
PlayerList = ["Banker","Player 1","Player 2",'Player 3',"Player 4","Everyone"]

# Initial amt    
Init_Amt_Player = 15000
Init_Amt_Banker = 10000000
Init_Amt = [[Init_Amt_Banker,Init_Amt_Banker],[Init_Amt_Player,Init_Amt_Player],[Init_Amt_Player,Init_Amt_Player],[Init_Amt_Player,Init_Amt_Player],[Init_Amt_Player,Init_Amt_Player]]

PayerButton = tk.StringVar(BookGUI, "1")
PayeeButton = tk.StringVar(BookGUI, "1")
  
# Dictionary to create multiple buttons
values = {"Banker" : 0,"Player 1" : 1,"Player 2" : 2,"Player 3" : 3,"Player 4" : 4, "Everyone":5}
 
# Loop is used to create multiple Radiobuttons
# rather than creating each button separately

# Payer List and Button
Payer_Label = tk.Label(BookGUI,bg='white',text='Payer',font=("Arial", 12)).place(x=10,y=90)
mypady = 120
for (text, value) in values.items():
    tk.Radiobutton(BookGUI, text = text, variable = PayerButton,
                value = value, indicator = 0,height=1, width=10,
                background = "light blue",).place(x=10,y=mypady)
    mypady += 25
Payer_Selected = PayerButton.get()

# Payee List and Button
Payee_Label = tk.Label(BookGUI,bg='white',text='Payee',font=("Arial", 12)).place(x=200,y=90)
mypady = 120
for (text, value) in values.items():
    tk.Radiobutton(BookGUI, text = text, variable = PayeeButton,
                value = value, indicator = 0,height=1, width=10,
                background = "light blue",).place(x=200,y=mypady)
    mypady += 25

# Checkbox for double confirmation
Ckbox_Confirm = tk.IntVar()
tk.Checkbutton(BookGUI, text="Double Confirm", variable=Ckbox_Confirm).place(x=600,y=5)

# Amount to pay
Amt2Pay_K = tk.IntVar()
Amt2PayLabel = tk.Label(BookGUI,bg='white',text='Amount to Pay',font=("Arial", 12)).place(x=220,y=5)
Amt2PayBox_K = tk.Entry(BookGUI)
Amt2PayBox_K.place(x=220,y=35) 
Amt2PayBox_K_Label = tk.Label(BookGUI,bg='white',text='K',font=("Arial", 12)).place(x=420,y=35)
# Info label (to show what just been paid to whom)
InfoLabel_toShow=tk.StringVar()
Info_Label = tk.Label(BookGUI,bg='white',textvariable=InfoLabel_toShow).place(x=220,y=65)
           
# Compute Button
calculate_btn = tk.Button(BookGUI,text = 'Pay', bg ='light grey', height=3,width=10,\
                          command=calculate_positions)
    
calculate_btn.place(x=10,y=5)

# Balance to show in table
table_toshow = pd.DataFrame(Init_Amt,index=PlayerList[0:5])
table_toshow.index.name = 'Player'
table_toshow.columns = ['Initial','Balance']

frame = tk.Frame(BookGUI)
frame.pack(fill='both', expand=True)
frame.place(x=350,y=90)

pt = Table(frame, dataframe=table_toshow,width=160, height=120)
pt.show()
pt.showIndex()

#print(table_toshow)
# Exit Button to close program
tk.Button(BookGUI,text='Exit',command=lambda:BookGUI.destroy()).place(x=750,y=5)
# Button to reset balance to initial amount
tk.Button(BookGUI,text='Reset',command=ResetBalance).place(x=50,y=500)
tk.Button(BookGUI,text='Save Data',command=SaveData).place(x=50,y=550)
BookGUI.mainloop()