# Studieplan App

En enkel og modulær applikasjon for å administrere emner og studieplaner. Bygget med **Python** og **CustomTkinter**, organisert i et utvidbart prosjektoppsett med `models/`, `services/`, `core/`, `repositories/` og `ui/`.

## Funksjoner
- Opprett og slett emner (kode, semester, studiepoeng).
- Legg emner inn i en studieplan (6 semestre).
- Validering av studieplan (30 studiepoeng pr. semester, riktige semestre).
- Lagre og lese data til/fra JSON.
- Moderne UI med **CustomTkinter**, støtte for mørk/lys-modus og skalering.

## Screenshots
Legg til skjermbilder av UI her:

![Main Window](docs/screenshots/main_window.png)
![Emne Dialog](docs/screenshots/emne_dialog.png)
![Studieplan Dialog](docs/screenshots/studieplan_dialog.png)

(Opprett en mappe `docs/screenshots/` og legg bildene der.)

## Installasjon

### Klon prosjektet
```bash
git clone https://github.com/Zaqoon/Studieplanlegger.git
cd Studieplanlegger
```

### Opprett virtuelt miljø (anbefalt)
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

### Installer avhengigheter
```bash
pip install -r requirements.txt
```

### Viktige pakker
- `customtkinter` (UI)
- `pydantic` (modeller)
- `tkinter` (følger med Python, men krever `python3-tk` på Linux)

## Kjøring
Start applikasjonen med:

```bash
python main.py
```

## Prosjektstruktur
```
core/             # Forretningslogikk / validering
models/           # Pydantic-modeller (Emne, Studieplan, etc.)
repositories/     # Lagring (f.eks. fil/JSON)
services/         # Service-lag for emner og studieplan
ui/               # CustomTkinter-baserte brukergrensesnitt
requirements.txt  # Avhengigheter
main.py           # Inngangspunkt
```

## Lisens
Se [LICENSE](LICENSE) for detaljer.
