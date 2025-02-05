const EXPLOIT = 'EXPLOIT';
const EXPLORE = 'EXPLORE';

const RES_NEGATIVE = 'RES_NEGATIVE';
const RES_FINE = 'RES_FINE';
const RES_BETTER = 'RES_BETTER';
const RES_MORE = 'RES_MORE';
const RES_WOW = 'RES_WOW';
const RES_SAVE = 'RES_SAVE';
const ALL_RESPONSES = [RES_NEGATIVE, RES_FINE, RES_BETTER, RES_MORE, RES_WOW, RES_SAVE];

const DISPLAY = {
  RES_NEGATIVE: ['(N)egative', 'I wish to see no more of this'], 
  RES_FINE: ['(O)k', 'I feel neutral'], 
  RES_BETTER: ['(H)as Value', 'I can enjoy it'],
  RES_MORE: ['(M)ore', 'Show more like this'], 
  RES_WOW: ['(G)ood', 'One of the rare good ones'], 
  RES_SAVE: ['(S)tar', 'Super good. Save to disk'], 
}

const WAITING = 'WAITING';
const EVALING = 'EAVLING';

let stage = WAITING;
const globalObj = {
  doc_id: null, 
}

window.onload = () => {
  const buttonDiv = document.getElementById('buttondiv');
  for (const response of ALL_RESPONSES) {
    const b = document.createElement('button');
    b.innerHTML = DISPLAY[response][0];
    b.setAttribute('title', DISPLAY[response][1]);
    b.setAttribute('accesskey', DISPLAY[response][0][1]);
    b.addEventListener('click', onClick.bind(null, response));
    buttonDiv.appendChild(b);
  }
  askNew();
};

const askNew = () => {
  const xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
      const { doc_id, mode, artists } = JSON.parse(xmlHttp.responseText);
      globalObj.doc_id = doc_id;
      const imgDiv = document.getElementById('imgdiv');
      imgDiv.innerHTML = '';
      const img = document.createElement('img');
      img.src = `img?doc_id=${doc_id}`;
      img.classList.add('center-fit');
      imgDiv.appendChild(img);
      stage = EVALING;

      const h2 = document.getElementById('h2');
      if (mode === EXPLOIT) {
        h2.innerHTML = '';
      } else {
        h2.innerHTML = `${mode} Mode`;
        h2.title = 'This image is randomly sampled';
      }
      const url = `https://nozomi.la/post/${doc_id}.html`
      const link = document.getElementById('link2nozo');
      link.value = url;
      const artistsUl = document.getElementById('artists-name');
      while (artistsUl.firstChild) {
        artistsUl.removeChild(artistsUl.firstChild);
      }
      artists.forEach(artist => {
        const ui = document.createElement('li');
        ui.innerText = artist;
        artistsUl.appendChild(ui);
      });
    }
  }
  xmlHttp.open("GET", `next?rand=${Math.random()}`, true);
  xmlHttp.send(null);
};

const onClick = (response) => {
  if (stage !== EVALING) {
    alert('Too soon.');
    return;
  }
  const xmlHttp = new XMLHttpRequest();
  xmlHttp.onreadystatechange = () => {
    if (xmlHttp.readyState === 4 && xmlHttp.status === 200) {
      // console.log(xmlHttp.responseText);
      stage = WAITING;
      const imgDiv = document.getElementById('imgdiv');
      imgDiv.innerHTML = 'Loading...';
      askNew();
    }
  }
  xmlHttp.open(
    "GET", `response?doc_id=${
      globalObj.doc_id
    }&response=${response}`, true, 
  );
  xmlHttp.send(null);
};
