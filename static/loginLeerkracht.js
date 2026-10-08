const LoginForm = document.getElementById("LoginForm");
const Foutmelding = document.getElementById("Foutmelding");

var CurrentUser = ""
LoginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const Gegevens = new FormData(LoginForm);
    const Antw = await fetch("/login", {
        method: "POST",
        body: Gegevens
    });

    const Resultaat = await Antw.json();
    if (Resultaat.Success) {
        window.location.href = Resultaat.Redirect;
        CurrentUser = Resultaat.CurrentUser;

    } else {
        Foutmelding.textContent = Resultaat.Message;
    }
})
