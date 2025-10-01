import customtkinter as ctk
from services.emne_service import EmneService
from services.studieplan_service import StudieplanService
from repositories.file_repository import FileRepository
from ui import EmneDialog, StudieplanDialog


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
        
        title = ctk.CTkLabel(main_frame, text="Studieplan Revisjonssystem", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=20)
        
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        buttons = [
            ("1. Lag nytt emne", self.lag_nytt_emne),
            ("2. Legg emne til studieplan", self.legg_til_emne_studieplan),
            ("3. Vis alle emner", self.vis_alle_emner),
            ("4. Vis studieplan", self.vis_studieplan),
            ("5. Valider studieplan", self.valider_studieplan),
            ("6. Lagre til fil", self.lagre_til_fil),
            ("7. Les fra fil", self.les_fra_fil),
            ("8. Avslutt", self.avslutt)
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
        suksess, melding = FileRepository.lagre_data(
            self.emne_service.hent_alle_emner(), 
            self.studieplan_service.studieplan
        )
        self.vis_melding(melding)
    
    def les_fra_fil(self):
        suksess, melding, emner, studieplan = FileRepository.les_data()
        if suksess:
            self.emne_service.emner = emner
            self.studieplan_service.studieplan = studieplan
        self.vis_melding(melding)
    
    def avslutt(self):
        self.root.quit()
    
    def vis_melding(self, melding):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", melding)
    
    def run(self):
        self.root.mainloop()
