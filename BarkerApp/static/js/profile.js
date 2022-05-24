const root = document.getElementById('root')

const pathname = window.location.pathname;
const pathnameParts = pathname.split('/')
const username = pathnameParts[1]
const authenicatedUsername = JSON.parse(document.getElementById("user_name").textContent);

console.log(pathname)
console.log(pathnameParts)
console.log(username)

async function getProfileInfo() {
	const profileRes = await fetch(`/api/profiles/${username}`);
	const { user, profile, barks } = await profileRes.json();
	console.log(user)
	console.log(profile)
	console.log(barks)
	fillInfoCard(user, profile)
	renderBarks(barks, user)
}

function fillInfoCard(user, profile) {
	if(authenicatedUsername === user.username) {
		var tag = $('<a></a>').attr("href", "/edit_profile/").append("Edit profile");
	} else {
		var tag = $('<a></a>').attr("href", "/{{status}}/{{user}}").append("Status");
	}
	tag.insertBefore("#card");

	if(profile.avatar != null) {
		$('#avatar').src(profile.avatar);
	} else {
		$('#avatar').remove();
	}
	$('#username').text("@" + user.username);
	$('#usernameToo').text("@" + user.username);
	$('#card_username').text(user.username);
	$('#card_email').text(user.email);
	if(user.first_name != "") {
		$('#first_name').text(user.first_name);
	} else {
		$('#first_name').remove();
	}
	if(user.last_name != "") {
		$('#last_name').text(user.last_name);
	} else {
		$('#last_name').remove();
	}
	$('#bio').text(profile.bio);

}

async function renderBarks(barks, user) {
	console.log("los barks: ", user.username)
	barks.map(async (bark) => {
		const barkDiv = await renderBark(bark, user);
		$('#barks').append(barkDiv);
	})
}

async function renderBark(bark, author) {
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
  <a class="reply" href="/reply_bark/${bark.id}">Reply</a>
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

getProfileInfo()