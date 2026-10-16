import csv
import string
from flask import Flask, render_template, request, jsonify, session, redirect

app = Flask(__name__)
app.secret_key = "OhioSigma"

# ==========================================
# 1. CONTROLERENDE FUNCTIES UIT ONZE CODE
# ==========================================

def controle_wachtwoord_flask(invoer):
    if not isinstance(invoer, str) or not invoer:
        return False, "Vul een wachtwoord in."

    if len(invoer) < 8:
        return False, "Het wachtwoord moet minstens 8 tekens bevatten."

    if invoer.lower() == invoer:
        return False, "Het wachtwoord moet minstens één hoofdletter bevatten."

    if invoer.upper() == invoer:
        return False, "Het wachtwoord moet minstens één kleine letter bevatten."

    if not any(c.isdigit() for c in invoer):
        return False, "Het wachtwoord moet minstens één cijfer bevatten."

    if not any(c in string.punctuation for c in invoer):
        return False, "Het wachtwoord moet minstens één leesteken bevatten."

    return True, invoer

def controleer_uniek(waarde, kolom_naam, database):
    """Controleert of een waarde al bestaat in Databas.csv."""
    with open(database, "r", newline="", encoding="utf-8") as bestand:
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

@app.route("/WebsiteLeerling")
def Website():
    if session.get("rol") != "leerling":
        return redirect("/loginLeerling")
    return render_template("WebsiteLeerling.html")

@app.route("/WebsiteLeerkracht")
def WebsiteLeerkracht():
    if session.get("rol") != "leerkracht":
        return redirect("/loginLeerkracht")
    return render_template("WebsiteLeerkracht.html")

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

        if controleer_uniek(Gebruikersnaam, "Gebruikersnaam", "Databas.csv"):
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

        if not controleer_uniek(Leerlingnummer, "Leerlingnummer", "Databas.csv"):
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
                        session["gebruiker"] = Gebruikersnaam
                        session["rol"] = "leerling"
                        print(f"MATCH GEVONDEN! Welkom {Gebruikersnaam}")
                        return jsonify(
                            Success=True,
                            Redirect="/WebsiteLeerling",
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
        Gebruikersnaam = request.form.get("username").strip()   
        Wachtwoord = request.form.get("password").strip()

        print(f"\n--- INLOGPOGING ---")
        print(f"Ingevuld: Gebruikersnaam='{Gebruikersnaam}', Wachtwoord='{Wachtwoord}'")

        try:
            with open("DatabasLKR.csv", "r", newline="", encoding="utf-8") as file:  
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
                        session["gebruiker"] = Gebruikersnaam
                        session["rol"] = "leerkracht"
                        print(f"MATCH GEVONDEN! Welkom {Gebruikersnaam}")
                        return jsonify(
                            Success=True,
                            Redirect="/WebsiteLeerkracht",
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
    return render_template("loginLeerkracht.html")


@app.route("/registrerenLeerkracht", methods=["POST", "GET"])
def registrerenLeerkracht():
    if request.method == "POST":

        Voornaam = (request.form.get("Voornaam") or "").strip()
        Achternaam = (request.form.get("Achternaam") or "").strip()
        Email = (request.form.get("Email") or "").strip()
        Vak = (request.form.get("Vak") or "").strip()

        # Controleer of alle gegevens ingevuld zijn.
        if not all([Voornaam, Achternaam, Email, Vak]):
            return jsonify(
                Success=False,
                Message="Vul alle velden in."
            ), 400

        # Controleer of het e-mailadres al bestaat
        # in de database van leerkrachten.
        if not controleer_uniek(
            Email,
            "Email",
            "DatabasLKR.csv"
        ):
            return jsonify(
                Success=False,
                Message="Dit e-mailadres is al geregistreerd."
            ), 400

        # Bewaar de gegevens tijdelijk in de sessie.
        session["registratie_leerkracht"] = {
            "Voornaam": Voornaam,
            "Achternaam": Achternaam,
            "Email": Email,
            "Vak": Vak
        }

        return jsonify(Success=True)

    return render_template("registrerenLeerkracht.html")


@app.route("/MaakAccountLeerkracht", methods=["POST"])
def MaakAccountLeerkracht():

    # Haal de gebruikersnaam en het wachtwoord op.
    Gebruikersnaam = (
        request.form.get("Gebruikersnaam") or ""
    ).strip()

    Wachtwoord = request.form.get("Wachtwoord") or ""

    # Controleer of de eerste registratiestap voltooid is.
    Geg = session.get("registratie_leerkracht")

    if not Geg:
        return jsonify(
            Success=False,
            Message="Je moet eerst de registratiegegevens invullen."
        ), 400

    if not Gebruikersnaam or not Wachtwoord:
        return jsonify(
            Success=False,
            Message="Vul een gebruikersnaam en wachtwoord in."
        ), 400

    # Controleer de sterkte van het wachtwoord.
    Wachtwoord_OK, message = controle_wachtwoord_flask(Wachtwoord)

    if not Wachtwoord_OK:
        return jsonify(
            Success=False,
            Message=message
        ), 400

    # Controleer of de gebruikersnaam al bestaat
    # bij de leerkrachten.
    if not controleer_uniek(
        Gebruikersnaam,
        "Gebruikersnaam",
        "DatabasLKR.csv"
    ):
        return jsonify(
            Success=False,
            Message="Deze gebruikersnaam is al gekozen."
        ), 400

    # Schrijf de gegevens naar de database van leerkrachten.
    with open(
        "DatabasLKR.csv",
        "a",
        newline="",
        encoding="utf-8"
    ) as Bestand:

        Writer = csv.writer(Bestand)

        Writer.writerow([
            Geg["Voornaam"],
            Geg["Achternaam"],
            Geg["Email"],
            Gebruikersnaam,
            Wachtwoord,
            Geg["Vak"]
        ])

    # Verwijder de tijdelijke registratiegegevens.
    session.pop("registratie_leerkracht", None)

    return jsonify(Success=True)




# ==========================================
# 3. DE STARTKNOP
# ==========================================

if __name__ == '__main__':
    # Start de server op poort 5001
    app.run(debug=True, port=5001)
