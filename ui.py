from tkinter import *
import emoji_identify as em

THEME_COLOR = "#ffc8dd"
NEW_WIN_COLOR = "#cdb4db"


class EmojifyInterface:
    def __init__(self):
        self.ret_label = None
        self.output_text = None
        self.generated_emoji = None
        self.entered_sentence = None
        self.new_window = None

        self.window = Tk()
        self.window.title("Emojify")
        self.window.geometry("920x574")
        self.window.config(bg=THEME_COLOR)

        self.canvas = Canvas(self.window, bg="#FFFFFF", height=574, width=920, bd=0, highlightthickness=0,
                             relief="ridge")
        self.canvas.place(x=0, y=0)
        self.bg_img = PhotoImage(file="images/image_1.png")
        self.image_1 = self.canvas.create_image(460.0, 287.0, image=self.bg_img)
        self.canvas.create_text(224.0, 114.0, anchor="nw", text="Enter a Sentence\n", fill="#745F5F",
                                font=("ComicSansMS", 48 * -1))
        self.textbox_img = PhotoImage(file="images/entry_1.png")
        self.entry_bg = self.canvas.create_image(460.0, 270.5, image=self.textbox_img)
        self.sent_text = Entry(bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0, font=(25))
        self.sent_text.place(x=206.0, y=231.0, width=508.0, height=77.0)
        self.button_img = PhotoImage(file="images/button_1.png")
        self.button_1 = Button(image=self.button_img, borderwidth=0, highlightthickness=0, command=self.pop_up,
                               relief="flat")
        self.button_1.place(x=343.0, y=362.0, width=233.0, height=75.0)
        # self.sent_label = Label(text="Enter a sentence", fg="white", bg=THEME_COLOR, font=(25))
        # self.sent_label.grid(row=0, column=0)

        # self.sent_text = Entry()
        # self.sent_text.grid(row=2, column=0)

        # emojify_img = PhotoImage(file="images/emojifyimg.png")
        # self.emojify_button = Button(image=emojify_img, highlightthickness=0, command=self.pop_up)
        # self.emojify_button.grid(row=4, column=0)

        self.window.mainloop()

    def pop_up(self):
        self.new_window = Toplevel()
        self.new_window.title("Emojified")
        # self.new_window.geometry("500x500")
        self.new_window.config(padx=20, pady=20, bg=NEW_WIN_COLOR)
        self.entered_sentence = self.sent_text.get()
        self.generated_emoji = em.return_emoji(self.entered_sentence)
        self.output_text = Label(self.new_window, text=self.label_text(self.entered_sentence, self.generated_emoji),
                                 bg=NEW_WIN_COLOR,
                                 font=(25))
        self.output_text.grid(row=1, column=1)

    def label_text(self, sent_str, emoji_str):
        self.ret_label = f"Your sentence\n{sent_str}\ndepicts\n{emoji_str}"
        return self.ret_label
