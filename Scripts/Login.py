x = 1

#Oefening

import csv
import string
def controle_wachtwoord(invoer_str):
     
    is_geldig = False
    while not is_geldig:
        invoer = input(invoer_str)
        if len(invoer) > 12:
            if invoer.lower() != invoer:
                if invoer.upper() != invoer:
                    if any(c.isdigit() for c in invoer):
                        if any(c in string.punctuation for c in invoer):
                            wachtwoord = invoer
                            is_geldig = True
                        else:
                            print("Het wachtwoord moet minstens één leesteken bevatten.")
                    else: 
                        print("Het wachtwoord moet minstens één cijfer bevatten.")
                else:
                    print("Het wachtwoord moet minstens één kleine letter bevatten.")
            else: 
                print("Het wachtwoord moet minstens één hoofdletter bevatten.")
        else: 
            print("Het wachtwoord moet minstens 12 tekens bevatten.")

    return wachtwoord
from sympy import true

def controle_leeg(invoer_str):
    unieke_gegevens = ["Leerlingnummer: ", "Gebruikersnaam: "]
    is_ok = False
    is_uniek = False

    while not is_ok:
        invoer = input(invoer_str)
        if len(invoer) > 0:
            juiste_invoer = invoer
            is_ok = True
        else:
            print("De invoer mag niet leeg zijn.")

    if invoer_str in unieke_gegevens:
        if invoer_str == "Leerlingnummer: ":
            KolomWaarde = "Leerlingnummer"
        else:
            KolomWaarde = "Gebruikersnaam"

        while not is_uniek:
            bestaat_al = False
            with open("Scripts/Databas.csv", "r", newline="") as bestand:
                lezer = csv.DictReader(bestand)
                for rij in lezer:
                    if rij[KolomWaarde] == juiste_invoer:
                        bestaat_al = True

            if bestaat_al:
                print(f"Deze waarde bestaat al: {juiste_invoer}")
                invoer = input(invoer_str)
                if len(invoer) > 0:
                    juiste_invoer = invoer
                else:
                    print("De invoer mag niet leeg zijn.")
            else:
                is_uniek = True

        return juiste_invoer
    else:
        return juiste_invoer

def KeuzeMenu(tekst):
    while True:
        keuze = input(tekst)
        if keuze in ["1", "2", "3"]:
            return keuze
        else:
            print("Ongeldige keuze. Kies 1, 2 of 3.")

while True:
    x = KeuzeMenu("Wil je:\n1. Registreren\n2. Inloggen\n3. Afsluiten\n")

    if x == "1":
        Leerlingnummer = controle_leeg("Leerlingnummer: ")
        Voornaam = controle_leeg("Voornaam: ")
        Achternaam = controle_leeg("Achternaam: ")
        Klas = controle_leeg("Klas: ")
        Email = controle_leeg("Email: ")
        Gebruikersnaam = controle_leeg("Gebruikersnaam: ")
        Wachtwoord = controle_wachtwoord("Wachtwoord: ")
        Vak = controle_leeg("Vak: ")
        with open("Scripts/Databas.csv", "a") as file:
            file.write(f"\n{Leerlingnummer},{Voornaam},{Achternaam},{Klas},{Email},{Gebruikersnaam},{Wachtwoord},{Vak}")

    if x == "2":
        print("\nKijk als er iemand inzit:\n\n")
        Voornaam = input("Voornaam: ")
        Achternaam = input("Achternaam: ")
        Wachtwoord = input("Wachtwoord: ")

        with open("Scripts/Databas.csv", "r") as file:
            lezer = csv.DictReader(file)

            for i in lezer:
                bestaat = False
                if i["Voornaam"] == Voornaam and i["Achternaam"] == Achternaam and i["Wachtwoord"] == Wachtwoord:
                    print(f"U bent ingelogd, meester {i['Gebruikersnaam']}")
                    print(i)
                    bestaat = True
            if not bestaat:
                print("U bestaat niet in onze database.")
    if x == "3":
        print(20*"\n")