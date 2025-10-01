import customtkinter as ctk


class StudieplanDialog:
    def __init__(self, parent, emner_liste):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Legg til emne i studieplan")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        frame = ctk.CTkFrame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Velg emne:").pack(pady=5)
        self.emne_var = ctk.StringVar()
        if emner_liste:
            emne_menu = ctk.CTkOptionMenu(frame, variable=self.emne_var, values=emner_liste)
            emne_menu.pack(pady=5)
        else:
            ctk.CTkLabel(frame, text="Ingen emner registrert").pack(pady=5)
            return

        ctk.CTkLabel(frame, text="Semester:").pack(pady=5)
        self.semester_var = ctk.StringVar(value="1")
        semester_menu = ctk.CTkOptionMenu(frame, variable=self.semester_var,
                                          values=["1", "2", "3", "4", "5", "6"])
        semester_menu.pack(pady=5)

        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="OK", command=self.ok_clicked).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Avbryt", command=self.cancel_clicked).pack(side="left", padx=10)

    def ok_clicked(self):
        emne_info = self.emne_var.get()
        if emne_info:
            emnekode = emne_info.split(":")[0]
            semester_nr = int(self.semester_var.get())
            self.result = (emnekode, semester_nr)
            self.dialog.destroy()

    def cancel_clicked(self):
        self.dialog.destroy()
