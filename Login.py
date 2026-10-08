import csv
import string
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "OhioSigma"

# ==========================================
# 1. CONTROLERENDE FUNCTIES UIT ONZE CODE
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
    return render_template('Start.html')

@app.route("/Website")
def Website():
    return render_template("WebsiteLeerling.html")

@app.route("/MaakAccount", methods=["POST"])
def MaakAccount():
    Wachtwoord = request.form.get("Wachtwoord")
    Wachtwoord_OK, message = controle_wachtwoord_flask(Wachtwoord)
    if not Wachtwoord_OK:
        return jsonify(
            Success=False,
            Message=message
        )
    else:
        Gebruikersnaam = request.form.get("Gebruikersnaam")

        Geg = session["registratie"]

        Voornaam = Geg["Voornaam"]
        Achternaam = Geg["Achternaam"]
        Email = Geg["Email"]
        Klas = Geg["Klas"]
        Leerlingnummer = Geg["Leerlingnummer"]
        Vak = Geg["Vak"]

        if controleer_uniek(Gebruikersnaam, "Gebruikersnaam"):
            with open("Databas.csv", "a", newline="", encoding="utf-8") as Bestand:
                Writer = csv.writer(Bestand)

                Writer.writerow([
                    Leerlingnummer,
                    Voornaam,
                    Achternaam,
                    Klas,
                    Email,
                    Gebruikersnaam,
                    Wachtwoord,
                    Vak
                ])
            session.pop("registratie", None)
            return jsonify(Success=True)
        
        return jsonify(
            Success=False,
            Message="Gebruikersnaam is al gekozen."
        )




@app.route('/registrerenLeerling', methods=["POST","GET"])
def registrerenLeerling():
    if request.method == "POST":
        Voornaam = request.form.get("Voornaam").strip()
        Achternaam = request.form.get("Achternaam").strip()
        Email = request.form.get("Email").strip()
        Klas = request.form.get("Klas").strip()
        Leerlingnummer = request.form.get("Leerlingnummer").strip()
        Vak = request.form.get("Vak").strip()

        if not controleer_uniek(Leerlingnummer, "Leerlingnummer"):
            print("FOUT: Leerlingnummer zit al in systeem.")
            return jsonify(
                Success=False,
                Message="Dit leerlingnummer is al in gebruik, log in."
            ), 500

        session["registratie"] = {
            "Voornaam": Voornaam,
            "Achternaam": Achternaam,
            "Email": Email,
            "Klas": Klas,
            "Leerlingnummer": Leerlingnummer,
            "Vak": Vak 
        }

        return jsonify(Success=True)
    return render_template("registrerenLeerling.html")
    

@app.route('/loginLeerling', methods=["POST", "GET"])
def loginLeerling():
    if request.method == "POST":
        Gebruikersnaam = request.form.get("username").strip()   
        Wachtwoord = request.form.get("password").strip()

        print(f"\n--- INLOGPOGING ---")
        print(f"Ingevuld: Gebruikersnaam='{Gebruikersnaam}', Wachtwoord='{Wachtwoord}'")

        try:
            with open("Databas.csv", "r", newline="", encoding="utf-8") as file:  
                lezer = csv.DictReader(file)
                
                # Controleer of de CSV headers wel gelezen kunnen worden
                if not lezer.fieldnames:
                    print("FOUT: De CSV-database heeft geen kolommen of is leeg!")
                    return jsonify(
                        Success=False,
                        Message="Er is een probleem opgetreden."
                    ), 500

                for i in lezer:
                    db_gebruikersnaam = (i.get("Gebruikersnaam") or "").strip()
                    db_wachtwoord = (i.get("Wachtwoord") or "").strip()

                    if db_gebruikersnaam == Gebruikersnaam and db_wachtwoord == Wachtwoord:
                        print(f"MATCH GEVONDEN! Welkom {Gebruikersnaam}")
                        return jsonify(
                            Success=True,
                            Redirect="/Website",
                            CurrentUser=Gebruikersnaam
                        )
        except Exception as e:
            print(f"Er ging iets mis bij het openen van het bestand: {e}")
            return jsonify(
                Success=False,
                Message=f"Interne databasefout: {e}"
            ), 500
                    
        print("GEEN MATCH GEVONDEN IN DATABASE.")
        return jsonify(
            Success=False,
            Message="Gebruikersnaam of wachtwoord is fout."
        ), 401
    return render_template("loginLeerling.html")

@app.route("/loginLeerkracht", methods=["POST", "GET"])
def loginLeerkracht():
    if request.method == "POST":
        print("post")
    return render_template("loginLeerkracht.html")

@app.route("/registrerenLeerkracht", methods=["POST", "GET"])
def registrerenLeerkracht():
    if request.method == "POST":
        print("POST")
    return render_template("registrerenLeerkracht.html")


# ==========================================
# 3. DE STARTKNOP
# ==========================================

if __name__ == '__main__':
    # Start de server op poort 5001
    app.run(debug=True, port=5001)
