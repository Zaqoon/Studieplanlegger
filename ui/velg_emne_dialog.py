import customtkinter as ctk


class VelgEmneDialog:
    def __init__(self, parent, emner_liste):
        self.result = None
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Velg emne")
        self.dialog.geometry("360x180")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        frame = ctk.CTkFrame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Velg emne:").pack(pady=5)
        self.emne_var = ctk.StringVar()
        if emner_liste:
            self.emne_menu = ctk.CTkOptionMenu(frame, variable=self.emne_var, values=emner_liste)
            self.emne_menu.pack(pady=5)
        else:
            ctk.CTkLabel(frame, text="Ingen emner registrert").pack(pady=10)
            ctk.CTkButton(frame, text="Lukk", command=self.cancel_clicked).pack(pady=10)
            return

        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="OK", command=self.ok_clicked).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Avbryt", command=self.cancel_clicked).pack(side="left", padx=10)

    def ok_clicked(self):
        valgt = self.emne_var.get()
        if valgt:
            emnekode = valgt.split(":")[0].strip()
            self.result = emnekode
            self.dialog.destroy()

    def cancel_clicked(self):
        self.dialog.destroy()
