import csv
import string
from flask import Flask, render_template, request

app = Flask(__name__)

# ==========================================
# 1. DE CONTROLERENDE FUNCTIES UIT JOUW CODE
# ==========================================

def controle_wachtwoord_flask(invoer):  
    """Jouw originele wachtwoordcontrole."""
    if len(invoer) >= 8:
        if invoer.lower() != invoer:
            if invoer.upper() != invoer:
                if any(c.isdigit() for c in invoer):
                    if any(c in string.punctuation for c in invoer):
                        return True, invoer
                    else:
                        return False, "Het wachtwoord moet minstens één leesteken bevatten."
                else: 
                    return False, "Het wachtwoord moet minstens één cijfer bevatten."
            else:
                return False, "Het wachtwoord moet minstens één kleine letter bevatten."
        else: 
            return False, "Het wachtwoord moet minstens één hoofdletter bevatten."
    else: 
        return False, "Het wachtwoord moet minstens 8 tekens bevatten."

def controleer_uniek(waarde, kolom_naam):
    """Controleert of een waarde al bestaat in Databas.csv."""
    with open("Databas.csv", "r", newline="", encoding="utf-8") as bestand:
        lezer = csv.DictReader(bestand)
        for rij in lezer:
            if rij.get(kolom_naam) == waarde:
                return False 
    return True 


# ==========================================
# 2. INLOG-LOGICA (Alleen Gebruikersnaam + Wachtwoord)
# ==========================================

@app.route('/')
def home():
    """Toont de inlogpagina."""
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    Gebruikersnaam = request.form.get('username', '').strip()   
    Wachtwoord = request.form.get('password', '').strip()

    print(f"\n--- INLOGPOGING ---")
    print(f"Ingevuld: Gebruikersnaam='{Gebruikersnaam}', Wachtwoord='{Wachtwoord}'")

    try:
        with open("Databas.csv", "r", newline="", encoding="utf-8") as file:  
            lezer = csv.DictReader(file)
            
            # Controleer of de CSV headers wel gelezen kunnen worden
            if not lezer.fieldnames:
                print("FOUT: De CSV-database heeft geen kolommen of is leeg!")
                return "<h1>Databasefout</h1>", 500

            for i in lezer:
                db_gebruikersnaam = (i.get("Gebruikersnaam") or "").strip()
                db_wachtwoord = (i.get("Wachtwoord") or "").strip()

                if db_gebruikersnaam == Gebruikersnaam and db_wachtwoord == Wachtwoord:
                    print(f"MATCH GEVONDEN! Welkom {Gebruikersnaam}")
                    return render_template('Website.html', gebruikersnaam=Gebruikersnaam)
    except Exception as e:
        print(f"Er ging iets mis bij het openen van het bestand: {e}")
        return f"<h1>Interne Serverfout: {e}</h1>", 500
                
    print("GEEN MATCH GEVONDEN IN DATABASE.")
    return "<h1>U bestaat niet in onze database of het wachtwoord is onjuist.</h1>", 401



# ==========================================
# 3. DE STARTKNOP
# ==========================================

if __name__ == '__main__':
    # Start de server op poort 5001
    app.run(debug=True, port=5001)
