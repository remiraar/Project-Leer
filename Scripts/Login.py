Naam = "string"
Wachtwoord = "string"

x = 1

def CheckDatabase(Naam, Wachtwoord):
    with open("Scripts/Databas.csv", "r") as file:
        for line in file:
            if line.startswith(Naam):
                return True
    return False

def Login(Naam, Wachtwoord):
    if CheckDatabase(Naam, Wachtwoord):
        return True
    else:
        return False
#brol die we nooit gaan gebruiken gebruik OS voor niks

if x == 1:
    Leerlingnummer = input("Leerlingnummer: ")
    Voornaam = input("Voornaam: ")
    Achternaam = input("Achternaam: ")
    Klas = input("Klas: ")
    Email = input("Email: ")
    Gebruikersnaam = input("Gebruikersnaam: ")
    Wachtwoord = input("Wachtwoord: ")
    Vak = input("Vak: ")
    with open("Scripts/Databas.csv", "a") as file:
        file.write(f"{Leerlingnummer},{Voornaam},{Achternaam},{Klas},{Email},{Gebruikersnaam},{Wachtwoord},{Vak}")

elif x == 2:
    with open("Scripts/Databas.csv", "r") as file:
        file.readlines()