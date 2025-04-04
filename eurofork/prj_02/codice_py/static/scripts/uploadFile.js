document.getElementById("uploadForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    let uploadButton = document.getElementById("uploadButton");
    uploadButton.disabled = true;
    uploadButton.innerText = "Caricamento in corso...";

    let fileInput = document.getElementById("fileInput");
    let file = fileInput.files[0];
    let commessaInput = document.getElementById("commessa").value;


    let formData = new FormData();
    formData.append("file", file);
    formData.append("commessa", commessaInput);

    try {
        let response = await fetch("http://127.0.0.1:8000/upload/", {
                method: "POST",
                body: formData
            });

        if (response.ok) {
            uploadButton.disabled = false;
            uploadButton.innerText = "Invia";
            const blob = await response.blob();  // Ottieni il file risultante come blob
            const downloadUrl = URL.createObjectURL(blob);

            // Ottieni il nome del file senza estensione
            let fileName = file.name.split('.').slice(0, -1).join('.');

            // Crea un link per il download
            const a = document.createElement("a");
            a.href = downloadUrl;
            a.download = fileName + "_elaborato.csv";  // Aggiungi "_elaborato.csv" al nome
            a.click();  // Avvia il download

            document.getElementById("message").innerText = "File elaborato e scaricato con successo!";
        } else {
            const result = await response.json();
            document.getElementById("message").innerText = "Errore: " + result.message;
        }

        
        uploadButton.disabled = false;
        uploadButton.innerText = "Invia";
        document.getElementById("uploadForm").reset();
        document.getElementById("message").classList.add("show");

        setTimeout(() => {
            document.getElementById("message").classList.remove("show");
        }, 3000);

    } catch (error) {
        console.error("Errore nell'invio del file:", error);
        document.getElementById("message").innerText = "Errore nell'invio del file.";
    }
});
