
//ucitavanje stanja igre čim se stranica učita
window.onload = function () {
    ucitajStanje();
};

//dohvaćanje stanja igre svakih 5 sekundi
setInterval(ucitajStanje, 500);

function ucitajStanje() {

    fetch(`/stanje_igre/${idIgre}`)
        .then(response => response.json())
        .then(data => {

            if (data.status !== "ok") {
                alert(data.poruka);
                return;
            }

            // OSNOVNE INFORMACIJE
            const adutMap = {
            "H": "Herc",
            "K": "Karo",
            "P": "Pik",
            "T": "Tref"
            };

            if (data.adut && adutMap[data.adut]) {
                document.getElementById("adut").innerText = adutMap[data.adut];
            } else {
                document.getElementById("adut").innerText = "-";
            }
            
            const imena = data.imena_igraca;
            if (imena && imena[data.na_redu]) {
                document.getElementById("na-redu").innerText = imena[data.na_redu];
            } else {
                document.getElementById("na-redu").innerText = data.na_redu;
            }
            
            let rundaMi = data.rezultat_runde.mi;
            let rundaVi = data.rezultat_runde.vi;

            let zvanjaMi = data.zvanja.mi;
            let zvanjaVi = data.zvanja.vi;

            let ukupnoMi = data.rezultat_ukupno.mi;
            let ukupnoVi = data.rezultat_ukupno.vi;

            //Ako je igrač u timu "VI", zamijenimo perspektivu(tim "MI" su igrač 1 i 3 a tim "VI" su igrač 2 i 4)
            if (data.kljuc_tima === "VI") {

                [rundaMi, rundaVi] = [rundaVi, rundaMi];
                [zvanjaMi, zvanjaVi] = [zvanjaVi, zvanjaMi];
                [ukupnoMi, ukupnoVi] = [ukupnoVi, ukupnoMi];
            }

            // REZULTAT RUNDE
            document.getElementById("mi-runda").innerText = rundaMi;
            document.getElementById("vi-runda").innerText = rundaVi;

            // BODOVI ZVANJA
            document.getElementById("zvanja-mi").innerText = zvanjaMi;
            document.getElementById("zvanja-vi").innerText = zvanjaVi;

            // UKUPNI REZULTAT
            document.getElementById("mi-ukupno").innerText = ukupnoMi;
            document.getElementById("vi-ukupno").innerText = ukupnoVi;

            //KARTE NA STOLU

            const mojId = data.id_ovog_igraca;
            const red = data.red_igranja;
            const karteNaStolu = data.stol;           

            // očisti sve pozicije
            ["dolje", "lijevo", "gore", "desno"].forEach(poz => {
                document.getElementById(poz).innerHTML = "";
            });

            // sada dodaj imena
            if(imena){
                Object.keys(imena).forEach(logickiId => {

                    const relativna = (mojId - parseInt(logickiId) + 4) % 4;

                    let pozicija = "";
                    if (relativna === 0) pozicija = "dolje";
                    if (relativna === 1) pozicija = "lijevo";
                    if (relativna === 2) pozicija = "gore";
                    if (relativna === 3) pozicija = "desno";

                    const imeDiv = document.createElement("div");
                    imeDiv.innerText = imena[logickiId];
                    imeDiv.className = "ime-igraca";

                    // Ako sam ja onda ime ide ispod moje ruke
                    if (relativna === 0) {
                        document.getElementById("moje-ime").innerText = imena[logickiId];
                    } 
                    else {
                        document.getElementById(pozicija).prepend(imeDiv);
                    }
                });
            }

            // prolazimo kroz karte redom bacanja
            for (let i = 0; i < karteNaStolu.length; i++) {

                const karta = karteNaStolu[i];
                const igracKojiJeBacio = red[i];

                // izračun relativne pozicije
                const relativna = (mojId - igracKojiJeBacio + 4) % 4;

                let pozicija = "";

                if (relativna === 0) pozicija = "dolje";
                if (relativna === 1) pozicija = "lijevo";
                if (relativna === 2) pozicija = "gore";
                if (relativna === 3) pozicija = "desno";

                const img = document.createElement("img");
                img.src = `/static/${karta}.png`;
                img.style.width = "70px";

                document.getElementById(pozicija).appendChild(img);
            }


            // MOJA RUKA

            const rukaDiv = document.getElementById("moja-ruka");
            rukaDiv.innerHTML = "";

            data.karte_igraca.forEach(karta => {

                const img = document.createElement("img");
                img.src = `/static/${karta}.png`;
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
            const daljeGumb = document.getElementById("gumb-dalje");

            if (data.faza_igre === "zvanje" &&
                data.na_redu === data.id_ovog_igraca) {

                zvanjeDiv.style.display = "block";

                // Ako sam djelitelj (na musu), sakrij gumb dalje
                if (data.id_ovog_igraca === data.djelitelj) {
                    daljeGumb.style.display = "none";
                } else {
                    daljeGumb.style.display = "block";
                }

            } 
            else {
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
            return;
        }
        // Ako je štih gotov, zamrzni ekran 2 sekunde
        if (data.stanje === "stih_gotov") {

            clearInterval(intervalId); // zaustavi auto refresh

            setTimeout(() => {
                ucitajStanje();
                // ponovno pokreni refresh
                intervalId = setInterval(ucitajStanje, 1000);
            }, 2000);
        }
        else {
            ucitajStanje();
        }
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