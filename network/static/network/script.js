document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector("#username") != null){
    document.querySelector("#newPostForm").addEventListener("submit", newPost);
  }
  loadNav("all");
});

function loadNav(nav) {
  if (nav === "all") {
    fetch(`/${nav}Posts`, {
      method: "GET",
    })
      .then((response) => response.json())
      .then((json) => {
        const allPosts = document.querySelector("#allPost");
        json.forEach((element) => {
          const postDiv = document.createElement("div");
          postDiv.className = "postDiv";
          postDiv.id = `post${element.id}`;
          let likesNumber = element.likes.length;
          postDiv.innerHTML = `
            <div class="postHeader"><a href="/profile/${element.username}">${element.username}</a> at ${element.timestamp} said:</div>
            <div class="postContent">${element.content}</div>
            <div class="postFooter"><span id="span${element.id}">${likesNumber}</span> likes</div>
          `;
          //If a user is logged in:
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
            if(element.username === actualUser){
              const editButton = document.createElement("button")
              editButton.className = "btn btn-primary";
              editButton.innerHTML = "Edit";
              editButton.dataset.toggle = "modal" ;
              editButton.dataset.target = `#editPostModal${element.id}`;
              const editPostModal = document.createElement("div");
              editPostModal.innerHTML = `
                <div class="modal fade" id="editPostModal${element.id}" tabindex="-1" role="dialog">
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title">Edit Post</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                          <span aria-hidden="true">&times;</span>
                        </button>
                      </div>
                      <div class="modal-body">
                        <textarea rows="5" class="form-control" id="textArea_${element.id}">${element.content}</textarea>
                      </div>
                      <div class="modal-footer" id="${element.id}">
                        <button type="button" id="saveChanges${element.id}" class="btn btn-primary">Save changes</button>
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                      </div>
                    </div>
                  </div>
                </div>
              `;
              
              
              postDiv.append(editButton);
              postDiv.append(editPostModal);
              const saveChanges = postDiv.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild.firstElementChild
              saveChanges.addEventListener("click", function(){
                const content = document.querySelector(`#textArea_${element.id}`).value;
                editPost(element.id, content);
              });
              
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
  fetch("/newPost", {
    method: "POST",
    body: JSON.stringify({
      content: postContent,
    })
  }).then(response => location.reload())
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

function editPost(postID, content){
  fetch(`/editPost/${postID}`, {
    method: "PUT",
    body: JSON.stringify({
      content: content,
    })
  }).then(()=>location.reload()) 
}
