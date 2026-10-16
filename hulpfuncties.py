

import csv
import string

from flask import jsonify, request, session


def controle_wachtwoord_flask(invoer):
    if not isinstance(invoer, str) or not invoer:
        return False, "Vul een wachtwoord in."

    if len(invoer) < 8:
        return False, "Het wachtwoord moet minstens 8 tekens bevatten."

    if invoer.lower() == invoer:
        return False, "Het wachtwoord moet minstens één hoofdletter bevatten."

    if invoer.upper() == invoer:
        return False, "Het wachtwoord moet minstens één kleine letter bevatten."

    if not any(teken.isdigit() for teken in invoer):
        return False, "Het wachtwoord moet minstens één cijfer bevatten."

    if not any(teken in string.punctuation for teken in invoer):
        return False, "Het wachtwoord moet minstens één leesteken bevatten."

    return True, invoer


def controleer_uniek(waarde, kolom_naam, database):
    """Controleert of een waarde al voorkomt in een CSV-database."""
    with open(database, "r", newline="", encoding="utf-8") as bestand:
        lezer = csv.DictReader(bestand)

        for rij in lezer:
            if rij.get(kolom_naam) == waarde:
                return False

    return True


def controleer_login(database, rol, bestemming):
    """Controleert de login en stelt de sessie in als de gegevens kloppen."""
    gebruikersnaam = (request.form.get("username") or "").strip()
    wachtwoord = (request.form.get("password") or "").strip()

    try:
        with open(database, "r", newline="", encoding="utf-8") as bestand:
            lezer = csv.DictReader(bestand)

            if not lezer.fieldnames:
                return jsonify(
                    Success=False,
                    Message="Er is een probleem opgetreden."
                ), 500

            for rij in lezer:
                db_gebruikersnaam = (
                    rij.get("Gebruikersnaam") or ""
                ).strip()
                db_wachtwoord = (rij.get("Wachtwoord") or "").strip()

                if (
                    db_gebruikersnaam == gebruikersnaam
                    and db_wachtwoord == wachtwoord
                ):
                    session["gebruiker"] = gebruikersnaam
                    session["rol"] = rol

                    return jsonify(
                        Success=True,
                        Redirect=bestemming,
                        CurrentUser=gebruikersnaam
                    )

    except Exception:
        return jsonify(
            Success=False,
            Message="Er is een probleem met de database."
        ), 500

    return jsonify(
        Success=False,
        Message="Gebruikersnaam of wachtwoord is fout."
    ), 401