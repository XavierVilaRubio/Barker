const root = document.getElementById("root");

const pathname = window.location.pathname;
const pathnameParts = pathname.split("/");
const barkID = pathnameParts[pathnameParts.length - 2];
const username = JSON.parse(document.getElementById("user_name").textContent);

console.log(pathname);
console.log(pathnameParts);
console.log(barkID);

async function getBark(barkID) {
  const res = await fetch(`/api/barks/${barkID}`);
  const bark = await res.json();
  console.log(bark);
  renderBark(bark);
  getUser(bark.author);
  renderDropdown(bark);
}

function renderBark(bark) {
  const div = document.createElement("div");
  div.className = "bark";
  div.innerHTML = `
		<div class="top-row">
    <div class="text">
      <b id="author"></b>
      <p id="date">${bark.date}</p>
    </div>
    <div class="dropwdown" id="dropdown">
      
    </div>
  </div>
  <p>${bark.text}</p>
	${bark.media ? `<img class="img-fluid" src="${bark.media}" alt="" />` : ""}
  <a class="reply" href="/reply_bark/${barkID}">Reply</a>
	`;

  root.appendChild(div);
}

async function getUser(userId) {
  const res = await fetch(`/api/users/${userId}`);
  const user = await res.json();
  const authorElement = document.getElementById("author");
  authorElement.innerText = user.username;
  const dropdownDiv = document.getElementById("dropdown");
  if (username == user.username) {
    dropdownDiv.innerHTML = `
	<a class="author_options_button" type="button" id="author_options" data-bs-toggle="dropdown"
	aria-expanded="false">
		...
	</a>
	<ul class="dropdown-menu" aria-labelledby="author_options">
		<li>
		<a class="dropdown-item" href="/edit_bark/${barkID}">Edit</a>
		</li>
		<li>
		<a class="dropdown-item" href="/delete_bark/${barkID}">Delete</a>
		</li>
	</ul>
	`;
  } else {
    dropdownDiv.remove();
  }
  // fer href al profile
}

function renderDropdown(bark) {
  const dateElement = document.getElementById("date");
  console.log(date);
  dateElement.innerText = bark.date;
}

getBark(barkID);
