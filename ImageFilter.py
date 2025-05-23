from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk
import PIL.Image
import cv2
from numpy import *
from tkinter import messagebox

#pip install opencv-python
#pip install Pillow
#pip install opencv-python-headless
#pip install numpy

filename=""

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("JPG files",".jpg"),("JPEG files",".jpeg"),("PNG files",".png"),("GIF files",".gif"),("all files",".")))
    label_file_explorer.configure(text="File Opened: "+filename)
    img = ImageTk.PhotoImage(PIL.Image.open(filename).convert("RGB"))  
    canvas.create_image(10, 10, anchor=NW, image=img) 
    canvas.configure(img)
    
def go():
    global filename
    x= temp.get()
    if x == "Default Picture":
        filename = "C:\\Users\\qcc\\Desktop\\college\\SEM 3\\PP\\PP\\project\\New folder\\img3.jpg"
        label_file_explorer.configure(text="File Opened: "+filename)
        img = ImageTk.PhotoImage(PIL.Image.open(filename).convert("RGB"))  
        canvas.create_image(10, 10, anchor=NW, image=img) 
        canvas.configure(img)
    elif x== "Capture Image":
        messagebox.showinfo("To Capture Image:","1. Press SPACE key to capture image\n2. Press ESC key\n3. Close the window")
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("Camera")
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Camera", frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1
        cam.release()
        filename = "C:\\Users\\qcc\\Desktop\\college\\SEM 3\\PP\\PP\\project\\opencv_frame_0.png"
        label_file_explorer.configure(text="File Opened: "+filename)
        img = ImageTk.PhotoImage(PIL.Image.open(filename).convert("RGB"))  
        canvas.create_image(10, 10, anchor=NW, image=img) 
        canvas.configure(img)
        cv2.destroyAllWindows()
    elif x=="Select from your device":
        browseFiles()
    else:
        messagebox.showerror("Please select an Image","Choose from Drop Down Menu!")
    
def grayscale():
    gray = cv2.imread(filename= filename)
    gray_image = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Grayscale Image", gray_image)   
    
def invert():
    inv_img = cv2.imread(filename= filename)
    img_invert = cv2.bitwise_not(inv_img)
    cv2.imshow("Inverted Image", img_invert)   

def blur():
    image = cv2.imread(filename= filename) 
    ksize = (15, 15)
    image = cv2.blur(image, ksize)  
    cv2.imshow("Blurred Image", image) 

def sketch():
    img = cv2.imread(filename= filename)
    dst_gray, dst_color = cv2.pencilSketch(img, sigma_s=60, sigma_r=0.07, shade_factor=0.05) 
    cv2.imshow("Sketch", dst_color)

def water():
    img_water= cv2.imread(filename=filename)
    img_watercolor= cv2.stylization(img_water, sigma_s= 10, sigma_r=0.5)
    cv2.imshow("Water Color", img_watercolor)   

def pencil_sketch():
    image = cv2.imread(filename= filename)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted = 255-gray_image
    blur = cv2.GaussianBlur(inverted, (21, 21), 0)
    invertedblur = 255-blur
    sketch = cv2.divide(gray_image, invertedblur, scale=256.0)
    cv2.imshow("Pencil Sketch", sketch)
    
window = Tk()
window.title('Image Filter')
window.config(background = "BLACK")

#frame 1
frame1=Frame(window, bg="BLACK",highlightbackground="BLACK",highlightthickness=2,relief=RAISED,bd=10)
frame1.grid(row=0,column=0,padx=3,pady=3)

#title label
title_label=Label(frame1, text="IMAGE FILTER",font=("SILVERS PERSONAL USE Regular",40),width= 30,bg="#00a0b0",fg="white")
title_label.grid(row=0,column=0,columnspan=2,padx=2,pady=2)

#frame 2
frame2=Frame(window, bg="BLACK")
frame2.grid(row=1,column=0)

label_file_explorer = Label(frame2,text = "File Address",width = 63, height = 2,fg = "WHITE",border= 5, bg="BLACK",font=("Courier New",11))
label_file_explorer.grid(row=1,column=2)

temp=StringVar()
list_of_options=["Default Picture","Capture Image","Select from your device"]

someStyle=ttk.Style()
someStyle.configure('my.TMenubutton',font=('Courier New',14))

optMenu1 = ttk.OptionMenu(frame2, temp, "Select the location",*list_of_options, style='my.TMenubutton')
optMenu1['menu'].configure(font=('Courier New',14))
optMenu1.config(width=24)
optMenu1.grid(row=1,column=0)

go_button=Button(frame2,text="Go",width=5,font=('Courier New',12,"bold"),bg="#00a0b0",relief=GROOVE,command=go)
go_button.grid(row=1,column=1,padx=2)

#frame 3
frame3=Frame(window,bg="BLACK")
frame3.grid(row=2,column=0,padx=3,pady=3)

button_invert = Button(frame3,text = "Inverted",font=("Quicksand Book",20),fg="white",width=8,height=4,borderwidth=5,bg = "#edc951",relief=RIDGE,command = invert)
button_invert.grid(row=2,column=1,padx=2,pady=2)

button_grayscale = Button(frame3,text = "Gray\nScale",font=("Quicksand Book",20),fg="white",width=8,height=4,borderwidth=5,bg = "#edc951",relief=RIDGE,command = grayscale)
button_grayscale.grid(row=2,column=2,padx=2,pady=2)

button_blur = Button(frame3,text = "Blur",font=("Quicksand Book",20),fg="white",width=8,height=4,borderwidth=5,bg = "#eb6841",relief=RIDGE,command = blur)
button_blur.grid(row=3,column=1,padx=2,pady=2)

button_sketch = Button(frame3,text = "Sketch",font=("Quicksand Book",20),fg="white",width=8,height=4,borderwidth=5,bg = "#eb6841",relief=RIDGE,command = sketch)
button_sketch.grid(row=3,column=2,padx=2,pady=2)

button_water = Button(frame3,text = "Water\nColor",font=("Quicksand Book",20),fg="white",width=8,height=4,borderwidth=5,bg = "#cc2a36",relief=RIDGE,command = water)
button_water.grid(row=4,column=1,padx=2,pady=2)

button_ps = Button(frame3,text = "Pencil\nSketch",font=("Quicksand Book",20),fg="white",width=8,height=4,borderwidth=5,bg = "#cc2a36",relief=RIDGE,command = pencil_sketch)
button_ps.grid(row=4,column=2,padx=2,pady=2)

button_exit = Button(frame3,text = "Exit",font=("Courier New",14),width=26,height=1,borderwidth=5,bg="#00a0b0",relief=GROOVE,command = exit)
button_exit.grid(row=5,column=1,columnspan= 2,padx=2,pady=2)

canvas = Canvas(frame3, width = 715, height = 525,bg="BLACK")  
canvas.grid(row=2,column=0,rowspan=4,padx=15)

window.mainloop()
