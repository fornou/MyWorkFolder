function getToken() {
  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = "/login";
    return;
  }
  return token;
}


async function callAPIwithToken(method, url) {
  try{ 
    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${getToken()}`
      },
      credentials: 'include'
    });

    return response;

  } catch (err) {
    console.error("Errore durante la richiesta API:", err);
    throw err;
  }
}

export async function isLogged(callbackOnSuccess) {
  try {
    const response = await callAPIwithToken("GET", "http://localhost:8000/api/utente/me");

    if (!response || !response.ok) {
      console.log("Non autenticato");
      localStorage.removeItem('token');
      window.location.href = "/login";
      return;
    }

    const user = await response.json();
    window.currentUser = user;

    // Mostra iniziali/email
    const initial = user.Email?.charAt(0).toUpperCase() || '?';
    document.getElementById('user-initial').innerText = initial;
    document.getElementById('user-email').innerText = user.Email;

    if (typeof callbackOnSuccess === 'function') {
      callbackOnSuccess();
    }
  } catch (err) {
    console.error("Errore durante la verifica login:", err);
    localStorage.removeItem('token');
    window.location.href = "/login";
  }
}

export async function logout() {
  try {
    const response = await callAPIwithToken("POST", "http://localhost:8000/api/auth/logout");

    if (!response || !response.ok) {
      throw new Error("Logout fallito");
    }else{
      console.log("Logout effettuato con successo");
    }

    localStorage.removeItem('token');
    window.location.href = "/login";
  } catch (err) {
    console.error("Errore durante il logout:", err);
    localStorage.removeItem('token');
    window.location.href = "/login";
  }
}