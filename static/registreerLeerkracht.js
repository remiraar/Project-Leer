const RegistratieForm = document.getElementById("RegistratieForm");
const Foutmelding = document.getElementById("Foutmelding");
const SubmitKnop = document.getElementById("SubmitKnop");

let stap = 1;
let WWInput1;
let WWInput2;

RegistratieForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (stap===1) {
        const Gegevens = new FormData(RegistratieForm);

        const Antw = await fetch("/registrerenLeerkracht", {
            method: "POST",
            body: Gegevens
        });

        const Resultaat = await Antw.json();
        if (Resultaat.Success) {
            document.querySelectorAll(".InputBlok").forEach(Element => Element.remove());

            const WachtwoordDiv = document.createElement("div");
            WachtwoordDiv.className = "InputDiv2";
            
            const Gebruikersnaam = document.createElement("input");
            Gebruikersnaam.type = "text";
            Gebruikersnaam.placeholder = "Gebruikersnaam";
            Gebruikersnaam.name = "Gebruikersnaam";

            WWInput1 = document.createElement("input");
            WWInput1.type = "password";
            WWInput1.placeholder = "Wachtwoord";
            WWInput1.name = "Wachtwoord";

            WWInput2 = document.createElement("input");
            WWInput2.type = "password";
            WWInput2.placeholder = "Herhaal wachtwoord";

            SubmitKnop.textContent = "Registreer";
            WachtwoordDiv.append(Gebruikersnaam, WWInput1, WWInput2);
            RegistratieForm.prepend(WachtwoordDiv);
            
            stap = 2;
        } else {
            Foutmelding.textContent = Resultaat.Message;
        }
    
    } else if (stap===2) {
        if (WWInput1.value !== WWInput2.value) {
            Foutmelding.textContent = "De wachtwoorden zijn niet hetzelfde.";
            return;
        }

        const Geg = new FormData(RegistratieForm);

        const Antw = await fetch("/MaakAccountLeerkracht", {
            method: "POST",
            body: Geg
        });

        const Resultaat = await Antw.json();

        if (Resultaat.Success) {
            window.location.href = "/loginLeerkracht";
        } else {
            Foutmelding.textContent = Resultaat.Message;
        }
    }
})
