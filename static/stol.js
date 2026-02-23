

window.onload = function () {
    ucitajStanje();
};

//dohvaćanje stanja igre svakih 5 sekundi
 
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
            
            //REZULTAT RUNDE (bez zvanja)
            document.getElementById("mi-runda").innerText = data.rezultat_runde.mi;
            document.getElementById("vi-runda").innerText = data.rezultat_runde.vi;

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

                    const relativna = (parseInt(logickiId) - mojId + 4) % 4;

                    let pozicija = "";
                    if (relativna === 0) pozicija = "dolje";
                    if (relativna === 1) pozicija = "lijevo";
                    if (relativna === 2) pozicija = "gore";
                    if (relativna === 3) pozicija = "desno";

                    // ako je to moj igrač, ne prikazujemo ime
                    if (relativna !== 0) {

                        const imeDiv = document.createElement("div");
                        imeDiv.innerText = imena[logickiId];
                        imeDiv.className = "ime-igraca";
                        imeDiv.style.fontWeight = "bold";
                        imeDiv.style.marginBottom = "5px";

                        document.getElementById(pozicija).prepend(imeDiv);
                    }
                });
            }

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
                img.src = `/static/${karta}.png`;
                img.style.width = "70px";

                document.getElementById(pozicija).appendChild(img);
            }
        })

}