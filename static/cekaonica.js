// UČITAJ STANJE ČIM SE STRANICA OTVORI
window.onload = function () {
    provjeriSobu();
    socket.emit('join_room', {id_sobe: idSobe});
    socket.on('osvjezi_cekaonicu', function() {
        provjeriSobu();
    });
    socket.on('igra_krenula', function(data){
        window.location.href = `/prikaz_stola/${data.id_igre}`;
    });
};

function provjeriSobu() {
    fetch(`/stanje_sobe/${idSobe}`)
        .then(response => response.json())
        .then(data => {
            if (data.status !== "ok") return;

            if (data.igra_pokrenuta) {
                window.location.href = `/prikaz_stola/${data.id_igre}`;
                return;
            }

            // Praznimo sve kartice
            for (let i = 1; i <= 4; i++) {
                const el = document.getElementById(`igrac-${i}`);
                el.innerText = "Čekanje...";
                el.classList.remove("igrac-popunjen");
            }

            // Punimo s onima koji su tu
            data.igraci.forEach((igrac, index) => {
                const el = document.getElementById(`igrac-${index + 1}`);
                if (el) {
                    // Ako je igrac objekt koristi igrac.username, ako je string koristi samo igrac
                    el.innerText = typeof igrac === 'object' ? igrac.username : igrac;
                    el.classList.add("igrac-popunjen");
                }
            });

            // Omogući gumb samo ako su 4 igrača
            const gumb = document.getElementById("gumb-start");
            if (data.broj_igraca === 4) {
                gumb.disabled = false;
                document.getElementById("poruka-status").innerText = "Spremni za početak!";
            } else {
                gumb.disabled = true;
                document.getElementById("poruka-status").innerText = `Čekamo još ${4 - data.broj_igraca} igrača...`;
            }
        });
}