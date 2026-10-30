const RegistratieForm = document.getElementById("RegistratieForm");
const Foutmelding = document.getElementById("Foutmelding");
const SubmitKnop = document.getElementById("SubmitKnop");

let stap = 1;
let NuWWInput1;
let NuWWInput2;

RegistratieForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    if (stap===1) {
        const Gegevens = new FormData(RegistratieForm);

        const Antw = await fetch("/registrerenLeerling", {
            method: "POST",
            body: Gegevens
        });

        const Resultaat = await Antw.json();
        if (Resultaat.Success) {
            const NuWWInput1 = document.getElementById("VoornaamInput");
            NuWWInput1.name = "Wachtwoord";
            NuWWInput1.type = "password";
            NuWWInput1.placeholder = "Wachtwoord";
            NuWWInput1.value = "";

            const NuWWInput2 = document.getElementById("AchternaamInput");
            NuWWInput2.name = "";
            NuWWInput2.type = "password";
            NuWWInput2.placeholder = "Herhaal wachtwoord";
            NuWWInput2.value = "";

            const NuLeerCode = document.getElementById("EmailInput");
            NuLeerCode.name = "LeerCode";
            NuLeerCode.type = "text";
            NuLeerCode.placeholder = "Unieke verificatiecode";
            NuLeerCode.value = ""

            stap = 2;
        } else {
            Foutmelding.textContent = Resultaat.Message;
        }
    
    } else if (stap===2) {
        if (NuWWInput1.value !== NuWWInput2.value) {
            Foutmelding.textContent = "De wachtwoorden zijn niet hetzelfde.";
            return;
        }

        const Geg = new FormData(RegistratieForm);

        const Antw = await fetch("/MaakAccountLeerling", {
            method: "POST",
            body: Geg
        });

        const Resultaat = await Antw.json();

        if (Resultaat.Success) {
            window.location.href = "/loginLeerling";
        } else {
            Foutmelding.textContent = Resultaat.Message;
        }
    }
})
