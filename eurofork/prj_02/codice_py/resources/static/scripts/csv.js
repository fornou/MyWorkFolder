import { callAPIwithToken } from './auth.js';
import { showAlert } from './commesse.js';

export async function setPage() {
  const pathSegments = window.location.pathname.split('/').filter(Boolean);
  const commessaValue = pathSegments[1];
  const commessaInput = document.getElementById('commessa');

  if (!commessaInput) {
    console.error("Elemento input con id 'commessa' non trovato.");
    return;
  }
  commessaInput.readOnly = true;
  try {
    const response = await callAPIwithToken("GET", (`http://localhost:8000/api/commessa/${encodeURIComponent(commessaValue)}`));
    if (!response.ok) throw new Error("Errore nella richiesta");

    const data = await response.json();
    commessaInput.value = data?.Nome ?? "Errore";
  } catch (error) {
    console.error("Errore nel fetch della commessa:", error);
    commessaInput.value = "Errore";
  }
}


export async function formattaCsv() {
  const pathSegments = window.location.pathname.split('/').filter(Boolean);
  const commessa = pathSegments[1];  // '3'
  const categoria = document.getElementById('categoria').value.trim(); // es 'micromissioni'

  const fileInput = document.getElementById('file');
  const file = fileInput.files[0];
  const messageDiv = document.getElementById('message');
  const submitBtn = document.querySelector('button[type="submit"]');

  messageDiv.innerHTML = '';

  if (!file) {
    showAlert('warning', 'Seleziona un file prima di continuare.');
    return;
  }

  if (!categoria) {
    showAlert('warning', 'Seleziona una categoria.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    showAlert('info', 'Elaborazione in corso... Attendi.', true, true);
    submitBtn.disabled = true;

    const response = await callAPIwithToken('POST', `http://localhost:8000/api/commessa/${encodeURIComponent(commessa)}/${encodeURIComponent(categoria)}/upload`,formData);

    submitBtn.disabled = false;

    const text = await response.text(); // ✅ Leggi una sola volta

    if (response.ok) {
      showAlert('success', 'Dati formattati e importati nel db');
    } else {
      try {
        const data = JSON.parse(text);
        showAlert('danger', `Errore: ${data.detail || text}`, true, true);
      } catch {
        showAlert('danger', `Errore dal server: ${text}`, true, true);
      }
    }
  } catch (error) {
    console.error("Errore durante l'upload:", error);
    submitBtn.disabled = false;
    showAlert('danger', 'Si è verificato un errore durante la richiesta. Riprova.', true, true);
  }
}

