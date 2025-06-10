import {callAPIwithToken} from './auth.js';

let alertTimeout;

export function showAlert(type, message, spinner = true, persist = false) {
  const messageDiv = document.getElementById('message');
  if (!messageDiv) return;

  const iconMap = {
    success: 'fa-check-circle',
    danger: 'fa-exclamation-triangle',
    warning: 'fa-exclamation-circle',
    info: 'fa-info-circle'
  };

  const icon = iconMap[type] || 'fa-info-circle';

  const spinnerHtml = spinner && type === 'info'
    ? `<i class="fas fa-spinner fa-spin me-2"></i>`
    : `<i class="fas ${icon} me-2"></i>`;

  messageDiv.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show d-flex align-items-center justify-content-between" role="alert">
      <div class="d-flex align-items-center">
        ${spinnerHtml}
        <div>${message}</div>
      </div>
      <button type="button" class="btn-close ms-2" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
  `;

  const closeBtn = messageDiv.querySelector('.btn-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      if (alertTimeout) {
        clearTimeout(alertTimeout);
        alertTimeout = null;
      }
    });
  }

  if (!persist) {
    if (alertTimeout) clearTimeout(alertTimeout);

    alertTimeout = setTimeout(() => {
      const alert = messageDiv.querySelector('.alert');
      if (alert) {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      }
      alertTimeout = null;
    }, 4000);
  }
}



function createDotsMenu(commessa, closeOtherPopupsCallback) {
  const dotsMenu = document.createElement('div');
  dotsMenu.classList.add('dropdown', 'dots-menu', 'position-absolute', 'top-0', 'end-0', 'p-2');

  const btn = document.createElement('button');
  btn.classList.add('btn', 'btn-light', 'btn-sm', 'dropdown-toggle', 'p-1');
  btn.type = 'button';
  btn.setAttribute('data-bs-toggle', 'dropdown');
  btn.setAttribute('aria-expanded', 'false');
  btn.style.minWidth = '30px';
  btn.style.height = '30px';
  btn.style.borderRadius = '50%';
  btn.style.boxShadow = '0 0 5px rgba(0,0,0,0.15)';
  btn.innerHTML = '<i class="fa-solid fa-ellipsis-vertical"></i>';

  const dropdownMenu = document.createElement('ul');
  dropdownMenu.classList.add('dropdown-menu', 'dropdown-menu-end');
  dropdownMenu.style.minWidth = '150px';

  const modificaItem = document.createElement('li');
  const modificaLink = document.createElement('a');
  modificaLink.classList.add('dropdown-item', 'text-dark');
  modificaLink.href = '#';
  modificaLink.textContent = 'Modifica';
  modificaItem.appendChild(modificaLink);

  const eliminaItem = document.createElement('li');
  const eliminaLink = document.createElement('a');
  eliminaLink.classList.add('dropdown-item', 'text-danger');
  eliminaLink.href = '#';
  eliminaLink.textContent = 'Elimina';
  eliminaItem.appendChild(eliminaLink);

  dropdownMenu.appendChild(modificaItem);
  dropdownMenu.appendChild(eliminaItem);

  dotsMenu.appendChild(btn);
  dotsMenu.appendChild(dropdownMenu);

  // Per chiudere altri popup personalizzati (se usi più menu personalizzati)
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    closeOtherPopupsCallback(dropdownMenu);
  });

  // Gestione click item Modifica
  modificaLink.addEventListener('click', (e) => {
    e.preventDefault();
    showAlert('warning', `Funzione di <b>Modifica</b> da implementare.`, true);
  });

  // Gestione click item Elimina
  eliminaLink.addEventListener('click', (e) => {
    e.preventDefault();
    showAlert('warning', `Funzione di <b>Elimina</b> da implementare.`);
  });

  return { dotsMenu, dropdownMenu };
}

export async function createCommessa() {
  const commessa = document.getElementById('commessa').value.trim();
  const descrizione = document.getElementById('descrizione').value.trim();
  const fotoInput = document.getElementById('foto');
  const submitBtn = document.querySelector('button[type="submit"]');

  if (!commessa) {
    showAlert('warning', 'Inserisci un nome per la commessa.');
    return;
  }

  submitBtn.disabled = true;
  showAlert('info', 'Creazione commessa in corso...', true);

  try {
    const formData = new FormData();
    formData.append('commessa', commessa);
    formData.append('descrizione', descrizione);
    if (fotoInput.files.length > 0) {
      formData.append('foto', fotoInput.files[0]);
    }

    const response = await callAPIwithToken('POST', 'http://localhost:8000/api/commessa/create',formData);

    const data = await response.json();
    submitBtn.disabled = false;

    if (response.ok) {
      showAlert('success', `Commessa creata con successo! Nome: ${commessa}`);
      document.getElementById('commessaForm').reset();
    } else {
      let errorMessage = 'Impossibile creare commessa.';
      if (data.detail) {
        if (typeof data.detail === 'string') {
          errorMessage = data.detail;
        } else if (typeof data.detail === 'object' && data.detail.message) {
          errorMessage = data.detail.message;
        } else {
          errorMessage = JSON.stringify(data.detail);
        }
      }
      showAlert('danger', `Errore: ${errorMessage}`);
    }
  } catch (error) {
    submitBtn.disabled = false;
    showAlert('danger', 'Errore durante la richiesta. Riprova.');
    console.error("Errore nella creazione:", error);
  }
}

export async function getAllCommesse() {
  const spinner = document.getElementById('spinner');
  const messageDiv = document.getElementById('message');
  messageDiv.innerHTML = '';
  spinner.classList.remove("d-none");

  try {
    const response = await callAPIwithToken('GET', 'http://localhost:8000/api/commessa/all');
    if (!response.ok) throw new Error("Errore nel recupero dati");
    const commesse = await response.json();
    createCommessaCards(commesse);
  } catch (error) {
    showAlert('danger', 'Errore nel recupero delle commesse. Controlla il server.');
    console.error(error);
  } finally {
    spinner.classList.add("d-none");
  }
}

export function createCommessaCards(commesse) {
  let currentOpenPopup = null;

  const cont_commesse = document.querySelector('.carousel-inner');
  const indicators = document.getElementById('carousel-indicators');
  const carousel = document.getElementById('carouselExampleDark');

  cont_commesse.innerHTML = '';
  indicators.innerHTML = '';

  const commessePerSlide = 3;
  const numeroSlide = Math.ceil(commesse.length / commessePerSlide);

  function closeOtherPopups(openingPopup) {
    if (currentOpenPopup && currentOpenPopup !== openingPopup) {
      currentOpenPopup.style.display = 'none';
    }
    currentOpenPopup = (openingPopup.style.display === 'block') ? openingPopup : null;
  }

  document.addEventListener('click', () => {
    if (currentOpenPopup) {
      currentOpenPopup.style.display = 'none';
      currentOpenPopup = null;
    }
  });

  for (let i = 0; i < numeroSlide; i++) {
    const slide = document.createElement('div');
    slide.classList.add('carousel-item');
    if (i === 0) slide.classList.add('active');

    const row = document.createElement('div');
    row.classList.add('row', 'justify-content-center', 'gap-3', 'mb-4');

    for (let j = i * commessePerSlide; j < (i + 1) * commessePerSlide && j < commesse.length; j++) {
      const commessa = commesse[j];

      const col = document.createElement('div');
      col.classList.add('col-md-3', 'position-relative');

      const card = document.createElement('div');
      card.classList.add('card');

      const { dotsMenu, popupMenu } = createDotsMenu(commessa, closeOtherPopups);

      card.appendChild(dotsMenu);

      const link = document.createElement('a');
      link.href = `commesse/${commessa.ID_Commessa}`;
      link.classList.add('text-decoration-none', 'text-dark');

      const img = document.createElement('img');
      img.src = "/static/img/commesse.jpg";
      img.className = "card-img-top";
      img.alt = "foto_standard_commessa";

      const cardBody = document.createElement('div');
      cardBody.className = "card-body";

      const h5 = document.createElement('h5');
      h5.classList.add('card-title');
      h5.textContent = `Commessa ${commessa.ID_Commessa}`;

      const p = document.createElement('p');
      p.classList.add('card-text');
      p.textContent = commessa.Nome;

      cardBody.appendChild(h5);
      cardBody.appendChild(p);
      link.appendChild(img);
      link.appendChild(cardBody);

      card.appendChild(link);
      col.appendChild(card);
      row.appendChild(col);
    }

    slide.appendChild(row);
    cont_commesse.appendChild(slide);

    const indicator = document.createElement('button');
    indicator.type = "button";
    indicator.setAttribute('data-bs-target', '#carouselExampleDark');
    indicator.setAttribute('data-bs-slide-to', i);
    indicator.setAttribute('aria-label', `Slide ${i + 1}`);
    if (i === 0) {
      indicator.classList.add('active');
      indicator.setAttribute('aria-current', 'true');
    }
    indicators.appendChild(indicator);
  }

  carousel.classList.remove("d-none");
}

export async function searchCommessa() {
  const spinner = document.getElementById('spinner');
  const messageDiv = document.getElementById('message');
  const query = document.getElementById('search-input').value.trim();
  const cardsContainer = document.querySelector('.carousel-inner');
  cardsContainer.innerHTML = ''; // svuota le cards vecchie

  messageDiv.innerHTML = '';
  spinner.classList.remove("d-none");

  if (query === "") {
    window.location.reload();
    return;
  }

  try {
    const response = await callAPIwithToken('GET', `http://localhost:8000/api/commessa/search/${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error("Errore nel recupero dati");
    const commesse = await response.json();

    if (!commesse || commesse.length === 0) {
      showAlert('danger', `Non ci sono commesse contenenti ${query}.`);
    } else {
      createCommessaCards(commesse);
    }
  } catch (error) {
    showAlert('danger', 'Errore nel recupero delle commesse. Controlla il server.');
    console.error(error);
  } finally {
    spinner.classList.add("d-none");
  }
}

export async function getCommessaById() {
  const id = window.location.pathname.split("/").pop();
  const container = document.getElementById("container");
  const spinner = document.getElementById("spinner");

  spinner.style.display = "block";
  container.innerHTML = '';

  try {
    const response = await callAPIwithToken('GET', `http://localhost:8000/api/commessa/${id}`);
    if (!response.ok){ 
      window.location.href = "/404";
      return;
    }
    const commessa = await response.json();

    const avatar = document.createElement("img");
    avatar.src = "/static/img/commesse.jpg";
    avatar.alt = "Avatar Commessa";
    avatar.className = "rounded-circle mb-3";
    avatar.style.width = "80px";
    avatar.style.height = "80px";
    avatar.style.objectFit = "cover";

    const title = document.createElement("h5");
    title.className = "text-center";
    title.textContent = `Commessa ${commessa.ID_Commessa}`;

    const nome = document.createElement("p");
    nome.className = "text-center text-muted";
    nome.textContent = commessa.Nome;

    const researchContainer = document.createElement("div");
    researchContainer.className = "w-100 row g-2";

    const buttonCol = document.createElement("div");
    buttonCol.className = "col-2";

    const loadNewData = document.createElement("button");
    loadNewData.className = "btn btn-primary w-100 align-items-center";
    loadNewData.textContent = "Carica altri dati da un CSV";
    loadNewData.addEventListener("click", () => {
      window.location.href = `http://localhost:8000/commessa/${id}/upload-csv`;
    });
    buttonCol.appendChild(loadNewData);

    const graficoContainer = document.createElement("div");
    graficoContainer.className = "grafico-container";

    await getDashboard(id, graficoContainer);

    container.appendChild(avatar);
    container.appendChild(title);
    container.appendChild(nome);
    container.appendChild(buttonCol);
    container.appendChild(graficoContainer);
  } catch (error) {
    showAlert('danger', 'Errore nel caricamento della commessa.');
    console.error(error);
  } finally {
    spinner.style.display = "none";
  }
}

async function getDashboard(commessaId, graficoContainer) {
  graficoContainer.innerHTML = `
    <div class="text-center py-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Caricamento...</span>
      </div>
    </div>
  `;

  try {
    const response = await callAPIwithToken("GET", `/api/commessa/${encodeURIComponent(commessaId)}/grafico`);
    if (!response.ok) {
      showAlert('warning', 'Grafico non disponibile per questa categoria.');
      graficoContainer.innerHTML = '';
      return;
    }
    const iframeHtml = await response.text();
    graficoContainer.innerHTML = iframeHtml;
  } catch (error) {
    showAlert('danger', 'Errore nel caricamento del grafico.');
    graficoContainer.innerHTML = '';
    console.error(error);
  }
}
