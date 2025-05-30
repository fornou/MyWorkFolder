export async function getAllCommesse() {
  try {
    const response = await fetch('http://localhost:8000/api/commessa/all');
    const commesse = await response.json();
    createCommessaCards(commesse);
  } catch (error) {
    document.getElementById('spinner').innerHTML = `
      <div class="alert alert-danger w-100" role="alert">
        Errore nel recupero delle commesse. Controlla il server.
      </div>`;
    console.error(error);
  }
}

export async function createCommessaCards(commesse) {
      let currentOpenPopup = null;

      const cont_commesse = document.querySelector('.carousel-inner');
      const indicators = document.getElementById('carousel-indicators');
      const carousel = document.getElementById('carouselExampleDark');
      const spinner = document.getElementById('spinner');

      cont_commesse.innerHTML = '';
      indicators.innerHTML = '';

      const commessePerSlide = 3;
      const numeroSlide = Math.ceil(commesse.length / commessePerSlide);

      for (let i = 0; i < numeroSlide; i++) {
        const slide = document.createElement('div');
        slide.classList.add('carousel-item');
        if (i === 0) slide.classList.add('active');

        const row = document.createElement('div');
        row.classList.add('row', 'justify-content-center', 'gap-3', 'mb-4');

        for (let j = i * commessePerSlide; j < (i + 1) * commessePerSlide && j < commesse.length; j++) {
          const commessa = commesse[j];

          const col = document.createElement('div');
          col.classList.add('col-md-3', 'position-relative'); // Serve per posizionare il popup

          const card = document.createElement('div');
          card.classList.add('card');

          // === TRE PUNTINI + POPUP ===
          const dotsMenu = document.createElement('div');
          dotsMenu.classList.add('dots-menu', 'position-absolute', 'top-0', 'end-0', 'p-2');
          dotsMenu.style.cursor = 'pointer';
          dotsMenu.innerHTML = '<i class="fa-solid fa-ellipsis-vertical"></i>';

          const popupMenu = document.createElement('div');
          popupMenu.classList.add('popup-menu', 'bg-white', 'border', 'rounded', 'p-2', 'shadow-sm');
          popupMenu.style.position = 'absolute';
          popupMenu.style.top = '0px';
          popupMenu.style.right = '20px';
          popupMenu.style.display = 'none';
          popupMenu.style.zIndex = '1000';

          const select = document.createElement('select');
          select.classList.add('form-select');
          select.style.minWidth = '160px';
          select.style.fontSize = '1rem';
          select.style.padding = '6px 10px';
          select.innerHTML = ` 
            <option selected disabled>Seleziona</option>
            <option value="modifica">Modifica</option>
            <option value="elimina">Elimina</option>
          `;


          popupMenu.appendChild(select);

          dotsMenu.appendChild(popupMenu);
          card.appendChild(dotsMenu); // Fuori dal link

          // === GESTIONE CLICK - MENU ===
          dotsMenu.addEventListener('click', (e) => {
            e.stopPropagation();  // Ferma la propagazione dell'evento

            // Chiude il popup precedente se esiste
            if (currentOpenPopup && currentOpenPopup !== popupMenu) {
              currentOpenPopup.style.display = 'none';
            }

            // Toggle visibilità
            popupMenu.style.display = popupMenu.style.display === 'none' ? 'block' : 'none';
            currentOpenPopup = popupMenu.style.display === 'block' ? popupMenu : null;
          });

          // === GESTIONE CLICK - SELEZIONE ===
          select.addEventListener('click', (e) => {
            // Evita la chiusura del popupMenu quando si clicca sulla freccetta del select
            e.stopPropagation();
          });

          // === GESTIONE SELECT ===
          select.addEventListener('change', (e) => {
            const value = e.target.value;
            if (value === 'elimina') {
              console.log(`Elimina ${commessa.ID_Commessa}`);
            } else if (value === 'modifica') {
              console.log(`Modifica ${commessa.ID_Commessa}`);
            }
          });

          // === CARD LINK + CONTENUTO ===
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

      spinner.classList.add("d-none");
      carousel.classList.remove("d-none");
}

export async function searchCommessa() {
  try {
    const title = document.getElementById('search-input').value;
    if(title == "") return getAllCommesse();
    
    const response = await fetch('http://localhost:8000/api/commessa/search/' + encodeURIComponent(title));
    if (!response.ok) throw new Error("Errore nel recupero dati");

    const commesse = await response.json();
    createCommessaCards(commesse);
    
  } catch (error) {
    document.getElementById('spinner').innerHTML = `
      <div class="alert alert-danger w-100" role="alert">
        Errore nel recupero delle commesse. Controlla il server.
      </div>`;
    console.error(error);
  }
}
