document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#newPostForm").addEventListener("submit", newPost);
  loadNav("all");
});

function loadNav(nav) {
  if (nav === "all") {
    fetch("/allPosts", {
      method: "GET",
    })
      .then((response) => response.json())
      .then((json) => {
        const allPosts = document.querySelector("#allPost");
        json.forEach((element) => {
          console.log(element);
          const postDiv = document.createElement("div");
          postDiv.className = "postDiv";
          postDiv.id = `post${element.id}`;
          let likesNumber = element.likes.length;
          postDiv.innerHTML = `
            <div class="postHeader">${element.username} at ${element.timestamp} said:</div>
            <div class="postContent">${element.content}</div>
            <div class="postFooter"><span id="span${element.id}">${likesNumber}</span> likes</div>
          `;
          if (document.querySelector("#username") != null){
            const actualUser = document.querySelector("#username").innerHTML;          
            if (element.likes.includes(actualUser)) {
              const unlikeButton = document.createElement("button");
              unlikeButton.className = "btn btn-danger";
              unlikeButton.innerHTML = "Unlike";
              unlikeButton.addEventListener("click", function () {
                unlikePost(element.id, likesNumber);
              });
              postDiv.append(unlikeButton);
            } else {
              const likeButton = document.createElement("button");
              likeButton.className = "btn btn-primary";
              likeButton.innerHTML = "Like";
              likeButton.addEventListener("click", function () {
                likePost(element.id, likesNumber);
              });
              postDiv.append(likeButton);
            }
          }          
          allPosts.append(postDiv);
        });
      })
      .catch((error) => console.error(error));
  }
}

function newPost (event){
  event.preventDefault();
  const postContent = document.querySelector("#postContent").value;
  console.log(postContent);
  fetch("/newPost", {
    method: "POST",
    body: postContent
  })
}

function likePost(postID, likesNumber) {
  document.querySelector(`#span${postID}`).innerHTML = likesNumber + 1;
  fetch(`/like/${postID}`);
  location.reload()
}

function unlikePost(postID, likesNumber) {
  document.querySelector(`#span${postID}`).innerHTML = likesNumber - 1;
  fetch(`/unlike/${postID}`)
  location.reload()
}
