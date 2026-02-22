// UČITAJ STANJE ČIM SE STRANICA OTVORI
window.onload = function () {
    provjeriSobu();
};

// SVAKIH 3 SEKUNDE PROVJERI STANJE SOBE
setInterval(provjeriSobu, 3000);


function provjeriSobu() {

    fetch(`/stanje_sobe/${idSobe}`)
        .then(response => response.json())
        .then(data => {

            if (data.status !== "ok") {
                console.error("Greška kod dohvaćanja sobe.");
                return;
            }

            // AKO JE IGRA POKRENUTA PREBACI NA STOL
            if (data.igra_pokrenuta) {
                window.location.href = `/prikaz_stola/${data.id_igre}`;
                return;
            }

            // INAČE OSTANI U ČEKAONICI I PRIKAŽI TRENUTNO STANJE 
            const div = document.querySelector(".cekaonica");

            div.innerHTML = `
                <h2>Čekaonica - Soba ${idSobe}</h2>
                <p>Broj igrača: ${data.broj_igraca} / 4</p>
                <p>Čekamo da se svi igrači pridruže...</p>
            `;
        })
        .catch(error => {
            console.error("Greška:", error);
        });
}