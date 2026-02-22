ac
//ucitavanje stanja igre čim se stranica učita
window.onload = function () {
    ucitajStanje();
};

//dohvaćanje stanja igre svakih 5 sekundi
setInterval(ucitajStanje, 5000);

function ucitajStanje() {

    fetch(`/stanje_igre/${idIgre}`)
        .then(response => response.json())
        .then(data => {

            if (data.status !== "ok") {
                alert(data.poruka);
                return;
            }

            // OSNOVNE INFORMACIJE
            document.getElementById("adut").innerText = data.adut || "-";
            document.getElementById("na-redu").innerText = data.na_redu;


            //REZULTAT RUNDE (bez zvanja)
            document.getElementById("mi-runda").innerText = data.rezultat_runde.mi;
            document.getElementById("vi-runda").innerText = data.rezultat_runde.vi;


            //BODOVI ZVANJA
            document.getElementById("zvanja-mi").innerText = data.zvanja.mi;
            document.getElementById("zvanja-vi").innerText = data.zvanja.vi;


            //UKUPNI REZULTAT IGRE
            document.getElementById("mi-ukupno").innerText = data.rezultat_ukupno.mi;
            document.getElementById("vi-ukupno").innerText = data.rezultat_ukupno.vi;


            //KARTE NA STOLU

            const mojId = data.id_ovog_igraca;
            const red = data.red_igranja;
            const karteNaStolu = data.stol;

            // očisti sve pozicije
            ["dolje", "lijevo", "gore", "desno"].forEach(poz => {
                document.getElementById(poz).innerHTML = "";
            });

            // prolazimo kroz karte redom bacanja
            for (let i = 0; i < karteNaStolu.length; i++) {

                const karta = karteNaStolu[i];
                const igracKojiJeBacio = red[i];

                // izračun relativne pozicije
                const relativna = (igracKojiJeBacio - mojId + 4) % 4;

                let pozicija = "";

                if (relativna === 0) pozicija = "dolje";
                if (relativna === 1) pozicija = "lijevo";
                if (relativna === 2) pozicija = "gore";
                if (relativna === 3) pozicija = "desno";

                const img = document.createElement("img");
                img.src = `/static/img/${karta}.png`;
                img.style.width = "70px";

                document.getElementById(pozicija).appendChild(img);
            }


            // MOJA RUKA

            const rukaDiv = document.getElementById("moja-ruka");
            rukaDiv.innerHTML = "";

            data.karte_igraca.forEach(karta => {

                const img = document.createElement("img");
                img.src = `/static/img/${karta}.png`;
                img.style.width = "70px";
                img.style.margin = "5px";
                img.style.cursor = "pointer";

                img.onclick = function () {
                    odigrajKartu(karta);
                };

                rukaDiv.appendChild(img);
            });

            //ZVANJE ADUTA

            const zvanjeDiv = document.getElementById("zvanje-aduta");

            if (data.faza_igre === "zvanje" &&
                data.na_redu === data.id_ovog_igraca) {

                zvanjeDiv.style.display = "block";

            } else {
                zvanjeDiv.style.display = "none";
            }

        });       
}



//BACANJE KARTE


function odigrajKartu(oznaka) {

    fetch("/odigraj_potez", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_igre: idIgre,
            kliknuta_karta: oznaka
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.status !== "ok") {
            alert(data.poruka);
        }

        ucitajStanje();
    });
}



//ZVANJE ADUTA

function zoviAduta(odluka) {

    fetch("/zovi_aduta", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id_igre: idIgre,
            odluka: odluka
        })
    })
    .then(response => response.json())
    .then(data => {

        if (data.status !== "ok") {
            alert(data.poruka);
        }

        // Nakon zvanja ponovno učitaj stanje
        ucitajStanje();
    });
}