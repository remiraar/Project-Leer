import csv
from hulpfuncties import (
    controle_wachtwoord_flask, 
    controleer_uniek, 
    controleer_login
)
from flask import Flask, render_template, request, jsonify, session, redirect

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = "OhioSigma"



# ==========================================
# 1. INLOG-LOGICA (Alleen Gebruikersnaam + Wachtwoord)
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
        Gebruikersnaam = (request.form.get("Gebruikersnaam") or "").strip()

        if not Gebruikersnaam:
            return jsonify(
                Success=False,
                Message="Vul een gebruikersnaam in."
            ), 400  
        Geg = session.get("registratie")

        if not Geg:
            return jsonify(
                Success=False,
                Message="Je moet eerst je registratiegegevens invullen."
            ), 400

        Voornaam = Geg["Voornaam"]
        Achternaam = Geg["Achternaam"]
        Email = Geg["Email"]
        Klas = Geg["Klas"]
        Leerlingnummer = Geg["Leerlingnummer"]

        if not all([Voornaam, Achternaam, Email, Klas, Leerlingnummer]):
            return jsonify(
                Success=False,
                Message="Vul alle velden in."
            ), 400

        if controleer_uniek(Gebruikersnaam, "Gebruikersnaam", str(BASE_DIR / "Databas.csv")):
            with open(str(BASE_DIR / "Databas.csv"), "a", newline="", encoding="utf-8") as Bestand:
                Writer = csv.writer(Bestand)

                Writer.writerow([
                    Leerlingnummer,
                    Voornaam,
                    Achternaam,
                    Klas,
                    Email,
                    Gebruikersnaam,
                    Wachtwoord
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


        if not controleer_uniek(Leerlingnummer, "Leerlingnummer", str(BASE_DIR / "Databas.csv")):
            print("FOUT: Leerlingnummer zit al in systeem.")
            return jsonify(
                Success=False,
                Message="Dit leerlingnummer is al in gebruik, log in."
            ), 400

        session["registratie"] = {
            "Voornaam": Voornaam,
            "Achternaam": Achternaam,
            "Email": Email,
            "Klas": Klas,
            "Leerlingnummer": Leerlingnummer,
        }

        return jsonify(Success=True)
    return render_template("registrerenLeerling.html")
    

@app.route('/loginLeerling', methods=["POST", "GET"])
def loginLeerling():
    if request.method == "POST":
        return controleer_login(
            str(BASE_DIR / "Databas.csv"),
            "leerling",
            "/WebsiteLeerling"
        )

    return render_template("loginLeerling.html")


@app.route("/loginLeerkracht", methods=["POST", "GET"])
def loginLeerkracht():
    if request.method == "POST":
        return controleer_login(
            str(BASE_DIR / "DatabasLKR.csv"),
            "leerkracht",
            "/WebsiteLeerkracht"
        )

    return render_template("loginLeerkracht.html")


@app.route("/registrerenLeerkracht", methods=["POST", "GET"])
def registrerenLeerkracht():
    if request.method == "POST":

        Voornaam = (request.form.get("Voornaam") or "").strip()
        Achternaam = (request.form.get("Achternaam") or "").strip()
        Email = (request.form.get("Email") or "").strip()

        # Controleer of alle gegevens ingevuld zijn.
        if not all([Voornaam, Achternaam, Email]):
            return jsonify(
                Success=False,
                Message="Vul alle velden in."
            ), 400

        # Controleer of het e-mailadres al bestaat
        # in de database van leerkrachten.
        if not controleer_uniek(
            Email,
            "Email",
            str(BASE_DIR / "DatabasLKR.csv")
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
        str(BASE_DIR / "DatabasLKR.csv")
    ):
        return jsonify(
            Success=False,
            Message="Deze gebruikersnaam is al gekozen."
        ), 400

    # Schrijf de gegevens naar de database van leerkrachten.
    with open(
        str(BASE_DIR / "DatabasLKR.csv"),
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
            Wachtwoord
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
