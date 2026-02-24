let intervalId;
let freezeAktivan = false;

window.onload = function () {
    ucitajStanje();
    intervalId = setInterval(ucitajStanje, 1500); // Malo sporije da ne guši server
};

function ucitajStanje() {
    fetch(`/stanje_igre/${idIgre}`)
        .then(res => res.json())
        .then(data => {
            if (data.status !== "ok" || freezeAktivan) return;
            const mojId = data.id_ovog_igraca;


            ["dolje", "desno", "gore", "lijevo"].forEach(p => document.getElementById(`karta-${p}`).innerHTML = "");

            // Postavljanje karata na stol
            data.stol.forEach((karta, i) => {
                const igracId = data.red_igranja[i];
                const rel = (igracId - mojId + 4) % 4;
                const pos = ["dolje", "desno", "gore", "lijevo"][rel];
                document.getElementById(`karta-${pos}`).innerHTML = `<img src="/static/${karta}.png" class="karta-stol">`;
            });

            const adutMap = {"H": "Herc", "K": "Karo", "P": "Pik", "T": "Tref"};
            document.getElementById("adut").innerText = adutMap[data.adut] + " (" + data.imena_igraca[data.igrac_koji_zove] + ")" || "-";
            document.getElementById("na-redu").innerText = data.imena_igraca[data.na_redu] || "-";

            let rMi = data.rezultat_runde.mi, rVi = data.rezultat_runde.vi;
            let uMi = data.rezultat_ukupno.mi, uVi = data.rezultat_ukupno.vi;

            if (data.kljuc_tima === 24) {
                [rMi, rVi] = [rVi, rMi];
                [uMi, uVi] = [uVi, uMi];
            }

            document.getElementById("mi-runda").innerText = rMi;
            document.getElementById("vi-runda").innerText = rVi;
            document.getElementById("mi-ukupno").innerText = uMi;
            document.getElementById("vi-ukupno").innerText = uVi;
            document.getElementById("zvanja-mi").innerText = data.zvanja.mi || 0;
            document.getElementById("zvanja-vi").innerText = data.zvanja.vi || 0;

            // Imena igrača
            Object.keys(data.imena_igraca).forEach(idStr => {
                const logId = parseInt(idStr);
                const rel = (logId - mojId + 4) % 4;
                const pos = ["dolje", "desno", "gore", "lijevo"][rel];
                const el = document.getElementById(`ime-${pos}`);
                if(el) el.innerText = data.imena_igraca[idStr];
            });

            // Moja ruka
            document.getElementById("moja-ruka").innerHTML = data.karte_igraca.map(k =>
                `<img src="/static/${k}.png" class="karta-png" onclick="odigrajKartu('${k}')">`
            ).join("");

            // Zvanje
            const zvanjeDiv = document.getElementById("zvanje-aduta");
            zvanjeDiv.style.display = (data.faza_igre === "zvanje" && data.na_redu === mojId) ? "block" : "none";
            document.getElementById("gumb-dalje").style.display = (mojId === data.djelitelj) ? "none" : "inline-block";

        });
}

function odigrajKartu(oznaka) {
    fetch("/odigraj_potez", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id_igre: idIgre, kliknuta_karta: oznaka})
    })
    .then(res => res.json())
    .then(data => {

        if (data.status !== "ok") {
            alert(data.poruka);
            return;
        }

        if (data.stanje === "stih_gotov") {

            freezeAktivan = true;
            clearInterval(intervalId);

            setTimeout(() => {
                freezeAktivan = false;
                ucitajStanje();
                intervalId = setInterval(ucitajStanje, 1500);
            }, 2000);

        } else {
            ucitajStanje();
        }
    });
}


function zoviAduta(odluka) {
    fetch("/zovi_aduta", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({id_igre: idIgre, odluka: odluka})
    }).then(() => ucitajStanje());
}