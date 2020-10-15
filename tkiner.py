from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from PIL import ImageTk, Image
import brain
import classify
def data():
    global filename
    filename = askopenfilename(initialdir='C:\\',title = "Select file")
    x = ImageTk.PhotoImage(Image.open(filename).resize((180, 218), Image.ANTIALIAS))
    w1 = Label(window, image=x).pack(side=TOP, padx=2, pady=2)
    window.mainloop()
    return(filename)
def result():
    
    if(int(brain.predict(filename)[0][0]*100)>=88):
        showinfo("Result ", 'this sick patient has a tumor! \nhis tumor type is: \n'+str(classify.classify(filename)))
    else:
        showinfo("Result",'the sick patient has not a tumor!')
        
window = Tk()

window.title("Tumor Detection")
window.geometry('500x500')
window['background']='#856ff8'
lbl = Label(window, text="Welcome",bg='#856ff8', fg='white', font=("Arial Bold", 25))

lbl.pack(side=TOP, padx=5, pady=5)
x = ImageTk.PhotoImage(Image.open("brain_PNG98.png").resize((180, 218), Image.ANTIALIAS))
w1 = Label(window, image=x,bg='#856ff8').pack(side="bottom", padx=2, pady=2)
Button(window, text ='Select RMI Image ',command=data,bg='green', fg='white').pack(side=LEFT, padx=5, pady=5)
Button(window, text ='Get result', command=result,bg='green', fg='white').pack(side=RIGHT, padx=5, pady=5)
window.mainloop()
