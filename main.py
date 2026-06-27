import customtkinter as ctk

app = ctk.CTk()
app.geometry("600x700")



gameframe = ctk.CTkFrame(app,fg_color="#FFFFFF")

def createmainmenu():
    global mainframe

    gameframe.pack_forget()
    mainframe = ctk.CTkFrame(
        master=app,
        width=600,
        height=700,
        corner_radius=15,
        fg_color="#212121"
    )
    mainframe.pack(fill="both", expand=True)

    headinglabel = ctk.CTkLabel(
    master=mainframe,
    text="Space Warrior!",
    font=("Zero Bots", 80, "bold"),
    text_color="#FFFFFF")

    headinglabel.pack(pady = 100)

    playbutton = ctk.CTkButton(
        master=mainframe,
        width=100,
        height=80,
        text="Play",
        font=("Zero Bots", 30, "bold"),
        text_color="#FFFFFF",
        fg_color="transparent",
        border_width=2,
        border_color="#FFFFFF",
        hover_color="#FFFFFF",
        command=creategame)
    # Mouse enters the button
    playbutton.bind("<Enter>", lambda e: playbutton.configure(text_color="black", fg_color="#FFFFFF", border_color="#000000", border_width=2))

    # Mouse leaves the button
    playbutton.bind("<Leave>", lambda e: playbutton.configure(text_color="#FFFFFF", fg_color="transparent", border_color="#FFFFFF"))
    
    headinglabel.pack(pady = 100)
    playbutton.pack(pady= 40)

def creategame():
    global gameframe

    mainframe.pack_forget()
    gameframe = ctk.CTkFrame(app,fg_color="#FFFFFF")
    gameframe.pack(fill="both", expand=True)

    backbutton = ctk.CTkButton(
        master=gameframe,
        width=100,
        height=80,
        text="Back",
        font=("Zero Bots", 30, "bold"),
        text_color="#000000",
        fg_color="transparent",
        border_width=2,
        border_color="#000000",
        hover_color="#000000",
        command=mainmenu)
    

    backbutton.bind("<Enter>", lambda e: backbutton.configure(text_color="#FFFFFF", fg_color="#000000", border_color="#FFFFFF", border_width=2))
    backbutton.bind("<Leave>", lambda e: backbutton.configure(text_color="#000000", fg_color="transparent", border_color="#000000"))
    backbutton.pack(anchor = "nw",pady= 20,padx = 20)


def mainmenu():
    gameframe.pack_forget()
    mainframe.pack(fill="both", expand=True)

def maingame():
    pass


createmainmenu()

app.mainloop()


