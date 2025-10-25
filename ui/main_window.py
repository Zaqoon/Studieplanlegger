import customtkinter as ctk
import os
from tkinter import filedialog as fd
from services.emne_service import EmneService
from services.studieplan_service import StudieplanService
from repositories.file_repository import FileRepository
from ui import (
    EmneDialog,
    StudieplanDialog,
    SlettEmneDialog,
    FjernFraStudieplanDialog,
    VelgEmneDialog,
)
from models.studieplan import Studieplan

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class StudieplanApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Studieplan")
        self.root.geometry("800x600")
        
        self.emne_service = EmneService()
        self.studieplan_service = StudieplanService(self.emne_service)
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(main_frame, text="Studieplan",
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        buttons = [
            ("1. Lag et nytt emne", self.lag_nytt_emne),
            ("2. Legg til et emne i en studieplan", self.legg_til_emne_studieplan),
            ("3. Fjern et emne fra en studieplan", self.fjern_emne_fra_studieplan),
            ("4. Skriv ut ei liste over alle registrerte emner", self.vis_alle_emner),
            ("5. Lag en ny tom studieplan", self.ny_tom_studieplan),
            ("6. Skriv ut en studieplan med hvilke emner som er i hvert semester", self.vis_studieplan),
            ("7. Sjekk om en studieplan er gyldig eller ikke", self.valider_studieplan),
            ("8. Finn hvilke studieplaner som bruker et oppgitt emne", self.finn_planer_med_emne),
            ("9. Lagre emnene og studieplanene til fil", self.lagre_til_fil),
            ("10. Les inn emnene og studieplanene fra fil", self.les_fra_fil),
            ("11. Avslutt", self.avslutt),
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(button_frame, text=text, command=command, width=200, height=40)
            row, col = divmod(i, 2)
            btn.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        self.output_frame = ctk.CTkScrollableFrame(main_frame)
        self.output_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.output_text = ctk.CTkTextbox(self.output_frame, height=300)
        self.output_text.pack(fill="both", expand=True)
    
    def lag_nytt_emne(self):
        dialog = EmneDialog(self.root)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            emnekode, semester, studiepoeng = dialog.result
            if self.emne_service.opprett_emne(emnekode, semester, studiepoeng):
                self.vis_melding(f"Emne {emnekode} opprettet")
            else:
                self.vis_melding(f"Kunne ikke opprette emne {emnekode}")

    def fjern_emne_fra_studieplan(self):
        dialog = FjernFraStudieplanDialog(self.root, self.emne_service.get_emner_list())
        self.root.wait_window(dialog.dialog)

        if dialog.result:
            emnekode, semester_nr = dialog.result
            ok = self.studieplan_service.fjern_emne_fra_semester(emnekode, semester_nr)
            if ok:
                self.vis_melding(f"Fjernet {emnekode} fra semester {semester_nr}.")
            else:
                self.vis_melding(f"Kunne ikke fjerne {emnekode} fra semester {semester_nr}.")
    
    def legg_til_emne_studieplan(self):
        dialog = StudieplanDialog(self.root, self.emne_service.get_emner_list())
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            emnekode, semester_nr = dialog.result
            suksess, melding = self.studieplan_service.legg_til_emne_i_semester(emnekode, semester_nr)
            self.vis_melding(melding)
    
    def vis_alle_emner(self):
        emner_liste = self.emne_service.get_emner_list()
        if emner_liste:
            self.vis_melding("Alle registrerte emner:\n" + "\n".join(emner_liste))
        else:
            self.vis_melding("Ingen emner registrert")
    
    def vis_studieplan(self):
        oversikt = self.studieplan_service.hent_studieplan_oversikt()
        self.vis_melding("\n".join(oversikt))
    
    def valider_studieplan(self):
        er_gyldig, feil = self.studieplan_service.valider_studieplan()
        if er_gyldig:
            self.vis_melding("Studieplanen er gyldig! ✓")
        else:
            self.vis_melding("Studieplanen er ikke gyldig:\n" + "\n".join(feil))
    
    def lagre_til_fil(self):
        rot = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        lagre_mappe = os.path.join(rot, "saved_plans")
        os.makedirs(lagre_mappe, exist_ok=True)
        filnavn = fd.asksaveasfilename(
            title="Lagre emner og studieplan",
            defaultextension=".json",
            filetypes=[("JSON filer", "*.json")],
            initialdir=lagre_mappe,
            initialfile="studiedata.json",
        )
        if not filnavn:
            return
        suksess, melding = FileRepository.lagre_data(
            self.emne_service.hent_alle_emner(),
            self.studieplan_service.studieplan,
            filnavn,
        )
        self.vis_melding(melding)
    
    def les_fra_fil(self):
        rot = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        lagre_mappe = os.path.join(rot, "saved_plans")
        os.makedirs(lagre_mappe, exist_ok=True)
        filnavn = fd.askopenfilename(
            title="Les emner og studieplan fra fil",
            filetypes=[("JSON filer", "*.json")],
            initialdir=lagre_mappe,
        )
        if not filnavn:
            return
        suksess, melding, emner, studieplan = FileRepository.les_data(filnavn)
        if suksess:
            self.emne_service.emner = emner
            self.studieplan_service.studieplan = studieplan
        self.vis_melding(melding)

    def ny_tom_studieplan(self):
        # Slett alle data i minnet og start på nytt
        self.emne_service.emner = {}
        self.studieplan_service.studieplan = Studieplan()
        self.vis_melding("Ny tom studieplan opprettet. Alle emner er slettet fra minnet.")

    def finn_planer_med_emne(self):
        dialog = VelgEmneDialog(self.root, self.emne_service.get_emner_list())
        self.root.wait_window(dialog.dialog)
        if not dialog.result:
            return
        emnekode = dialog.result
        semestre = self.studieplan_service.finn_semestre_for_emne(emnekode)
        if semestre:
            sem_txt = ", ".join(str(s) for s in sorted(semestre))
            self.vis_melding(f"Emnet {emnekode} finnes i studieplanen i semester: {sem_txt}.")
        else:
            self.vis_melding(f"Emnet {emnekode} finnes ikke i studieplanen.")
    
    def avslutt(self):
        self.root.quit()
    
    def vis_melding(self, melding):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", melding)
    
    def run(self):
        self.root.mainloop()
