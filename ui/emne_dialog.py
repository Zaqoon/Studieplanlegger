import customtkinter as ctk
from tkinter import messagebox


class EmneDialog:
    def __init__(self, parent):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Lag nytt emne")
        self.dialog.geometry("400x340")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        frame = ctk.CTkFrame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Emnekode:").pack(pady=5)
        self.emnekode_entry = ctk.CTkEntry(frame)
        self.emnekode_entry.pack(pady=5)

        ctk.CTkLabel(frame, text="Semester:").pack(pady=5)
        self.semester_var = ctk.StringVar(value="høst")
        semester_menu = ctk.CTkOptionMenu(frame, variable=self.semester_var, values=["høst", "vår"])
        semester_menu.pack(pady=5)

        ctk.CTkLabel(frame, text="Studiepoeng:").pack(pady=5)
        self.studiepoeng_entry = ctk.CTkEntry(frame)
        self.studiepoeng_entry.pack(pady=5)

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")

        ok_btn = ctk.CTkButton(button_frame, text="Opprett emne", command=self.ok_clicked, width=120)
        ok_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Avbryt", command=self.cancel_clicked, width=120)
        cancel_btn.pack(side="right", padx=10)

    def ok_clicked(self):
        try:
            emnekode = self.emnekode_entry.get().strip()
            semester = self.semester_var.get()
            studiepoeng = int(self.studiepoeng_entry.get())

            if emnekode and studiepoeng > 0:
                self.result = (emnekode, semester, studiepoeng)
                self.dialog.destroy()
        except ValueError:
            messagebox.showerror("Feil", "Studiepoeng må være et tall")

    def cancel_clicked(self):
        self.dialog.destroy()