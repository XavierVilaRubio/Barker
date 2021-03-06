const root = document.getElementById("root");

const pathname = window.location.pathname;
const pathnameParts = pathname.split("/");
const barkID = pathnameParts[pathnameParts.length - 2];
const authenicatedUsername = JSON.parse(document.getElementById("user_name").textContent);

console.log(pathname);
console.log(pathnameParts);
console.log(barkID);
console.log(authenicatedUsername);

async function getBark(barkID) {
  const res = await fetch(`/api/barks/${barkID}`);
  const bark = await res.json();
  return bark;
}

async function renderBark(bark) {
  const author = await getUser(bark.author);
  const div = document.createElement("div");
  div.className = "bark";
  div.id = `bark-${bark.id}`;
  div.innerHTML = `
		<div class="top-row">
    <div class="text">
      <b id="author">${author.username}</b>
      <p id="date">${new Date(bark.date).toLocaleString('en-US')}</p>
    </div>
  ${authenicatedUsername === author.username ? `<div class="dropwdown" id="dropdown">
      <a class="author_options_button" type="button" id="author_options" data-bs-toggle="dropdown"
        aria-expanded="false">
        ...
      </a>
      <ul class="dropdown-menu" aria-labelledby="author_options">
        <li>
          <a class="dropdown-item" href="/edit_bark/${bark.id}">Edit</a>
        </li>
        <li>
          <button class="dropdown-item" onclick="deleteBark(${bark.id})">Delete</button>
        </li>
      </ul>
    </div>` : ""}
  </div>
  <p>${bark.text}</p>
	${bark.media ? `<img class="img-fluid" src="${bark.media}" alt="" />` : ""}
  <a class="reply" href="/reply_bark/${barkID}">Reply</a>
  <script>
    $('#bark-${bark.id}').css('cursor', 'pointer');
    $('#bark-${bark.id}').on("click", () => {
      if("${pathname}" != "/bark/${bark.id}/") {
        document.location.href = "/bark/${bark.id}/"
      }
    });
  </script>
	`;

  return div;
}

function deleteBark(barkID) {
  $.ajax({
    url: `/api/barks/${barkID}/`,
    method: 'DELETE',
    headers: {'X-CSRFToken': csrftoken}
  }).done(
    () => {
      history.go(-1);
    }
  )
}

async function getUser(userId) {
  const res = await fetch(`/api/users/${userId}`);
  const user = await res.json();
  return user;
}

async function render() {
  let mainBark = await getBark(barkID);
  let barkDiv = await renderBark(mainBark);
  $('#root').append(barkDiv);

  let bark = mainBark;
  // Parents
  let i = 0;
  while(bark.reply_to && i < 4) {
    bark = await getBark(bark.reply_to);
    barkDiv = await renderBark(bark);
    $('#parent').prepend(barkDiv);
    i++;
  }

  // Replies
  i = 0;
  for(i = 0; i < 4 && i < mainBark.replies.length; i++) {
    bark = await getBark(mainBark.replies[i]);
    barkDiv = await renderBark(bark);
    $('#replies').append(barkDiv);
  }
}

render()