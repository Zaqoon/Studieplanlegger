import customtkinter as ctk
from tkinter import messagebox

class SlettEmneDialog:
    def __init__(self, parent, emne_service, studieplan_service, on_change=None):
        self.result = None
        self.emne_service = emne_service
        self.studieplan_service = studieplan_service
        self.on_change = on_change

        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Slett emne")
        self.dialog.geometry("400x180")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        frame = ctk.CTkFrame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Velg emne å slette:").pack(pady=5)

        self.emne_var = ctk.StringVar()
        emner_liste = self.emne_service.get_emner_list()
        if emner_liste:
            self.emne_menu = ctk.CTkOptionMenu(frame, variable=self.emne_var, values=emner_liste)
            self.emne_menu.pack(pady=5)
        else:
            ctk.CTkLabel(frame, text="Ingen emner registrert").pack(pady=10)
            button_frame = ctk.CTkFrame(frame, fg_color="transparent")
            button_frame.pack(pady=20, fill="x")
            ctk.CTkButton(button_frame, text="Lukk", command=self.cancel_clicked, width=120).pack()
            return

        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(pady=20, fill="x")

        ok_btn = ctk.CTkButton(button_frame, text="Slett emne", command=self.ok_clicked, width=120, fg_color="red")
        ok_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(button_frame, text="Avbryt", command=self.cancel_clicked, width=120)
        cancel_btn.pack(side="right", padx=10)

    def ok_clicked(self):
        valgt = self.emne_var.get()
        if not valgt:
            return
        emnekode = valgt.split(":")[0].strip()
        for s in range(1, 7):
            self.studieplan_service.fjern_emne_fra_semester(emnekode, s)
        ok = self.emne_service.slett_emne(emnekode)
        if not ok:
            messagebox.showerror("Feil", "Klarte ikke å slette emnet.")
            return
        self.result = emnekode
        if self.on_change:
            self.on_change()
        self.dialog.destroy()

    def cancel_clicked(self):
        self.dialog.destroy()
