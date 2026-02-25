let intervalId;
let freezeAktivan = false;

window.onload = function () {
    ucitajStanje();
    intervalId = setInterval(ucitajStanje, 1500);
};

function ucitajStanje() {
    fetch(`/stanje_igre/${idIgre}`)
        .then(res => res.json())
        .then(data => {
            if (data.status !== "ok") return;
            if (data.faza_igre === "kraj") {
                clearInterval(intervalId)
                alert("Kraj igre! Netko je prešao 1001 bod. Vraćamo vas u sobu...");
                window.location.href = "/soba/" + data.id_sobe;
                return; 
            }

            prikaziStol(data);
            prikaziInfo(data);
            prikaziRezultate(data);
            prikaziImenaIgraca(data);
            prikaziMojuRuku(data);
            prikaziZvanjeUI(data);
            prikaziTablicuTimova(data);
            prikaziZvanja(data);
        });
}
            
function prikaziStol(data) {
    const mojId = data.id_ovog_igraca;

    ["dolje", "desno", "gore", "lijevo"].forEach(p =>
        document.getElementById(`karta-${p}`).innerHTML = ""
    );

    data.stol.forEach((karta, i) => {
        const igracId = data.red_igranja[i];
        const rel = (igracId - mojId + 4) % 4;
        const pos = ["dolje", "desno", "gore", "lijevo"][rel];

        document.getElementById(`karta-${pos}`).innerHTML =
            `<img src="/static/${karta}.png" class="karta-stol">`;
    });
}

function prikaziInfo(data) {
    const adutMap = { H: "Herc", K: "Karo", P: "Pik", T: "Tref" };

    document.getElementById("adut").innerText =
        adutMap[data.adut] + " (" + data.imena_igraca[data.igrac_koji_zove] + ")" || "-";

    document.getElementById("na-redu").innerText =
        data.imena_igraca[data.na_redu] || "-";
}

function prikaziRezultate(data) {
    document.getElementById("mi-runda").innerText = data.rezultat_runde.mi;
    document.getElementById("vi-runda").innerText = data.rezultat_runde.vi;
    document.getElementById("mi-ukupno").innerText = data.rezultat_ukupno.mi;
    document.getElementById("vi-ukupno").innerText = data.rezultat_ukupno.vi;
    document.getElementById("zvanja-mi").innerText = data.zvanja.mi || 0;
    document.getElementById("zvanja-vi").innerText = data.zvanja.vi || 0;

    if (data.pobjede_ukupno) {
        const pobjedeTd = document.querySelectorAll(".pobjede-red td");
        pobjedeTd[0].innerText = `Pobjede: ${data.pobjede_ukupno.mi}`;
        pobjedeTd[1].innerText = `Pobjede: ${data.pobjede_ukupno.vi}`;
    }
}

function prikaziImenaIgraca(data) {
    const mojId = data.id_ovog_igraca;

    Object.keys(data.imena_igraca).forEach(idStr => {
        const logId = parseInt(idStr);
        const rel = (logId - mojId + 4) % 4;
        const pos = ["dolje", "desno", "gore", "lijevo"][rel];

        const el = document.getElementById(`ime-${pos}`);
        if (el) el.innerText = data.imena_igraca[idStr];
    });
}

function prikaziMojuRuku(data) {
    document.getElementById("moja-ruka").innerHTML =
        data.karte_igraca
            .map(k =>
                `<img src="/static/${k}.png" class="karta-png" onclick="odigrajKartu('${k}')">`
            )
            .join("");
}

function prikaziZvanjeUI(data) {
    const mojId = data.id_ovog_igraca;

    const zvanjeDiv = document.getElementById("zvanje-aduta");
    zvanjeDiv.style.display =
        (data.faza_igre === "zvanje" && data.na_redu === mojId)
            ? "block"
            : "none";

    document.getElementById("gumb-dalje").style.display =
        (mojId === data.djelitelj)
            ? "none"
            : "inline-block";
}  


function prikaziTablicuTimova(data) {
    const timMi = [];
    const timVi = [];

    Object.keys(data.imena_igraca).forEach(idStr => {
        const id = parseInt(idStr);

        if (id === 1 || id === 3) {
            timMi.push(data.imena_igraca[idStr]);
        } else if (id === 2 || id === 4) {
            timVi.push(data.imena_igraca[idStr]);
        }
    });

    const tablicaTd = document.querySelectorAll(".tablica-timovi td");
    if (tablicaTd.length >= 2) {
        tablicaTd[0].innerHTML = timMi.join("<br>");
        tablicaTd[1].innerHTML = timVi.join("<br>");
    }
}



function prikaziZvanja(data) {
    const zvanjaKontejner = document.querySelector(".zvanja-obavijest");
    const naslov = zvanjaKontejner.querySelector("h3");
    const hr = zvanjaKontejner.querySelector("hr");

    zvanjaKontejner.innerHTML = "";
    zvanjaKontejner.appendChild(naslov);
    zvanjaKontejner.appendChild(hr);

    let imaZvanja = false;

    if (data.popisi_zvanja) {
        Object.keys(data.popisi_zvanja).forEach(idIgraca => {
            const lista = data.popisi_zvanja[idIgraca];

            if (lista.length > 0) {
                imaZvanja = true;
                const ime = data.imena_igraca[idIgraca] || "Igrač " + idIgraca;

                lista.forEach(z => {
                    const div = document.createElement("div");
                    div.className = "zvanje-stavka";
                    div.innerHTML =
                        `<strong>${ime}:</strong> (${z.karte}) - ${z.bodovi}`;
                    zvanjaKontejner.appendChild(div);
                });
            }
        });
    }

    if (!imaZvanja) {
        const prazno = document.createElement("div");
        prazno.style.fontSize = "0.85em";
        prazno.style.textAlign = "center";
        prazno.style.marginTop = "10px";
        prazno.innerText = "Trenutno nema zvanja";
        zvanjaKontejner.appendChild(prazno);
    }
}

function odigrajKartu(oznaka) {
    fetch("/odigraj_potez", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_igre: idIgre, kliknuta_karta: oznaka })
    })
    .then(res => res.json())
    .then(data => {

        if (data.status !== "ok") {
            alert(data.poruka);
            return;
        }

        if (data.stanje === "stih_gotov") {

            const pos = "dolje";
            document.getElementById(`karta-${pos}`).innerHTML =
                `<img src="/static/${oznaka}.png" class="karta-stol">`;

            freezeAktivan = true;
            clearInterval(intervalId);

            setTimeout(() => {
                freezeAktivan = false;
                ucitajStanje();
                intervalId = setInterval(ucitajStanje, 1500);
            }, 2000);

        } 

        else if (data.stanje === "kraj_igre") {
            clearInterval(intervalId)
            alert("Kraj igre! Bodovi su prešli 1001. Vraćamo vas u sobu...");
            window.location.href = "/soba/" + data.id_sobe;
        } 

        else {
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