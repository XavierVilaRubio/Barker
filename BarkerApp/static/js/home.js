const root = document.getElementById("root");

const pathname = window.location.pathname;
const pathnameParts = pathname.split("/");
const barkID = pathnameParts[pathnameParts.length - 2];
const authenicatedUsername = JSON.parse(document.getElementById("user_name").textContent);

function getData() {
	$('#username').text("@" + authenicatedUsername);
	$.ajax({
    url: `/api/friends/`,
    headers: {'X-CSRFToken': csrftoken}
  }).done(
    (users) => {
			users.map((user) => {
				const a = $('<a></a>').attr("href", `/${user.username}`).append(`${user.username}`)
				const li = $('<li></li>').attr("class", "list-group-item").append(a)
				$('#connections').append(li)
			})
    }
  )
	$.ajax({
    url: `/api/home/`,
    headers: {'X-CSRFToken': csrftoken}
  }).done(
    async function (barks) {
			barks.map(async (bark) => {
				const barkDiv = await renderBark(bark)
				$('#barks').append(barkDiv)
			})
    }
  )
}

async function getUser(userId) {
  const res = await fetch(`/api/users/${userId}`);
  const user = await res.json();
  return user;
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

getData();