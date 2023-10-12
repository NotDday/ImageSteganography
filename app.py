from pathlib import Path
from tkinter import Tk, Text, Button, PhotoImage,filedialog,messagebox,Frame,Label
from PIL import Image
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("gui/assets/")
#Steganographer
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +imdata.__next__()[:3]+imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
def encode():
    image = Image.open(img_path, 'r')
    txt=txt_box.get(1.0, "end-1c")
    if (len(txt) == 0):
        messagebox.showerror('Retry','Text is empty')
    newimg = image.copy()
    newimg=image.convert("RGB")
    encode_enc(newimg, txt)
    imn=img_path.split('.')
    name=Path(imn[0]+" - encoded.png")
    new_img_name=name
    if name.is_file():
        while True:
            i=1
            name=Path(imn[0]+f" - encoded({i}).png")
            if name.is_file():
                i+=1
            else:
                new_img_name=name
                break
    newimg.save(new_img_name,"PNG")
def decode():
    image = Image.open(img_path, 'r')
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3]+imgdata.__next__()[:3]+imgdata.__next__()[:3]]
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
def save():
    msg=decode()
    with open(save_path,'w')as f:
        f.write(msg)

# GUI
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)
window = Tk()
window.rowconfigure(0,weight=1)
window.columnconfigure(0,weight=1)
window.title("Image Steganographer")
window.geometry("450x500")
window.configure(bg = "#202020")
window.iconbitmap(relative_to_assets("imagesteganographer.ico"))
ef=Frame(window,bg = "#202020")
df=Frame(window,bg = "#202020")
sf=Frame(window,bg = "#202020")
for frame in(sf,ef,df):
    frame.grid(row=0,column=0,sticky='nsew')

# App Title
title_image = PhotoImage(file=relative_to_assets("title.png"))
title = Label(sf,image=title_image)
title.place(x=120.0,y=37.0,width=214,height=20)
# Encoder
encoder_image = PhotoImage(file=relative_to_assets("encoder.png"))
encoder = Label(ef,image=encoder_image)
encoder.place(x=120.0,y=37.0,width=214,height=20)
# Decoder
decoder_image = PhotoImage(file=relative_to_assets("decoder.png"))
decoder = Label(df,image=decoder_image)
decoder.place(x=120.0,y=37.0,width=214,height=20)

# Function for Selecting Files
img_path=""
img_name=""
def select_img():
    path=filedialog.askopenfilename(title="Select Image",filetypes=[('Image Files',["*.png","*.jpeg","*.jpg",])]).replace("/","\\")
    global img_path,img_name
    img_name = path.split('\\')[len(path.split('\\'))-1]
    if img_name !="":
        img_path=path
        input_img['text']=img_name
txt_path=""
def select_txt():
    path=filedialog.askopenfilename(title="Select Text File",filetypes=[('Text Files',["*.txt","*.text","*.rtf",])]).replace("/","\\")
    txt_name = path.split('\\')[len(path.split('\\'))-1]
    if txt_name !="":
        global txt_path
        txt_path=path
        with open(path)as f:
            txt=f.read()
            txt_box.delete("1.0","end")
            txt_box.insert("end",txt)
        input_txt['text']=txt_name
save_path=""
def select_save():
    path=filedialog.askdirectory().replace("/","\\")
    print(path)
    global save_path
    if path !="":
        save_path=path+"\Decoded_Msg.txt"
        print(save_path)
        save_loc['text']=save_path
# Image Selection
input_img=Label(sf,bg="#202020",fg="white",text="Open Image")
input_img.place(x=38,y=95.0)
input_img=Label(sf,bg="#2d2d2d",fg="#737373",text='Select an Image File.',anchor="w",padx=10)
input_img.place(x=38,y=120.0,width=348,height=32)
# Image Selection Button
select_btn = PhotoImage(file=relative_to_assets("file.png"))
image_btn = Button(sf,image=select_btn,borderwidth=0, highlightthickness=0,command=select_img,activebackground="#202020",cursor="target",relief="flat")
image_btn.place(x=402.0,y=130.4,width=16.0,height=15.2)
# Text File Selection
input_txt=Label(ef,bg="#202020",fg="white",text="Open text file or Type a message to encode below")
input_txt.place(x=38,y=95.0)
input_txt=Label(ef,bg="#2d2d2d",fg="#737373",text='Select a Text File.',anchor="w",padx=10)
input_txt.place(x=38,y=120.0,width=348,height=32)
# Text Selection Button
txt_btn = Button(ef,image=select_btn,borderwidth=0, highlightthickness=0,command=select_txt,activebackground="#202020",cursor="target",relief="flat")
txt_btn.place(x=402.0,y=130.4,width=16.0,height=15.2)
# Input Text
txt_box = Text(ef,bd=0,bg="#2D2D2D",fg="white",font=("Roboto Medium", 14 * -1),highlightthickness=0,padx=5,pady=5)
txt_box.place( x=38.0,y=200.0, width=375.0, height=200.0)
# Save location
save_loc=Label(df,bg="#202020",fg="white",text="Choose location")
save_loc.place(x=38,y=95.0)
save_loc=Label(df,bg="#2d2d2d",fg="#737373",text='Select location to save decoded message.',anchor="w",padx=10)
save_loc.place(x=38,y=120.0,width=348,height=32)
# Text Selection Button
save_sel = Button(df,image=select_btn,borderwidth=0, highlightthickness=0,command=select_save,activebackground="#202020",cursor="target",relief="flat")
save_sel.place(x=402.0,y=130.4,width=16.0,height=15.2)
# Decoded Message
dec_msg=Label(df,bg="#202020",fg="white",text="Decoded Message")
dec_msg.place(x=38,y=160.0)
msg_box = Text(df,bd=0,bg="#2D2D2D",fg="white",font=("Roboto Medium", 14 * -1),highlightthickness=0,padx=5,pady=5)
msg_box.place( x=38.0,y=200.0, width=375.0, height=200.0)

# Function for Controling Button Presses
def handle_btn_press(option):
    if option=="ef":
        if img_path=="":
            messagebox.showerror("Retry","Please Select an Image")
        else:
            ef.tkraise()
    elif option=="df":
        if img_path=="":
            messagebox.showerror("Retry","Please Select an Image")
        else:
            df.tkraise()
            msg=decode()
            msg_box.configure(state="normal")
            msg_box.delete("1.0","end")
            msg_box.insert('end',msg)
            msg_box.configure(state="disable")
    elif option=="back":
        sf.tkraise()
    elif option=="encode":
        encode()
        messagebox.showinfo("Success", "Image Encoded")
    elif option=="save":
        if save_path=="":
            messagebox.showerror("Retry","Please Select Save Location")
        else:
            save()
            messagebox.showinfo("Success", "File Saved")
# Decode Button
decode_btn_image = PhotoImage(file=relative_to_assets("df.png"))
decode_btn = Button(sf,image=decode_btn_image,borderwidth=0,highlightthickness=0,command=lambda : handle_btn_press("df"),activebackground= "#202020",relief="flat")
decode_btn.place(x=235.0,y=220.0,width=205.0,height=47.0)
# Encode Frame Button
ef_button_image = PhotoImage(file=relative_to_assets("ef.png"))
ef_btn = Button(sf,image=ef_button_image,borderwidth=0,highlightthickness=0,command=lambda : handle_btn_press("ef"),activebackground= "#202020",relief="flat")
ef_btn.place(x=12.0,y=220.0,width=205.0,height=47.0)
# Back Button
back_image = PhotoImage(file=relative_to_assets("back.png"))
backef = Button(ef,image=back_image,borderwidth=0,highlightthickness=0,activebackground= "#202020",command=lambda : handle_btn_press("back"),relief="flat")
backef.place(x=20.0,y=21.0,width=30.0,height=30.0)
backdf = Button(df,image=back_image,borderwidth=0,highlightthickness=0,activebackground= "#202020",command=lambda : handle_btn_press("back"),relief="flat")
backdf.place(x=20.0,y=21.0,width=30.0,height=30.0) 
# Encode Button
encode_button_image = PhotoImage(file=relative_to_assets("encode.png"))
encode_btn = Button(ef,image=encode_button_image,borderwidth=0,highlightthickness=0,command=lambda : handle_btn_press("encode"),activebackground= "#202020",relief="flat")
encode_btn.place(x=18.0,y=420.0,width=414.0,height=47.0)
# Save Button
save_button_image = PhotoImage(file=relative_to_assets("save.png"))
save_btn = Button(df,image=save_button_image,borderwidth=0,highlightthickness=0,command=lambda : handle_btn_press("save"),activebackground= "#202020",relief="flat")
save_btn.place(x=18.0,y=420.0,width=414.0,height=47.0)

window.resizable(False, False)
window.mainloop()

# End of GUI Code
