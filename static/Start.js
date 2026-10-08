const LeerkrachtButton = document.getElementById("LeerkrachtButton");
const LeerlingButton = document.getElementById("LeerlingButton");

function ButtonClick(wat) {
    window.location.href = wat
};
LeerkrachtButton.addEventListener("click", () => ButtonClick("/loginLeerkracht"));
LeerlingButton.addEventListener("click", () => ButtonClick("/loginLeerling"));
/* De ()=> moet er staan want ander wordt de functie direct aangeroepen
als de pagina juist geladen is.*/