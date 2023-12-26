// Get the page number (Not using Django templates)
const queryString = window.location.search.split('=');
let page = queryString[1];
// if there is no route paramaeters means this is the first load of post (either all or following)
if (page === undefined){
  page = 1
} else {
  page = parseInt(page)
}

document.addEventListener("DOMContentLoaded", function () {
  if (document.querySelector("#username") != null){
    document.querySelector("#newPostForm").addEventListener("submit", newPost);
  }
  // Get the type of posts to load
  const type = document.querySelector("#type").innerHTML;
  loadNav(type);
});

function loadNav(nav) {  
  //Fetch posts
  fetch(`/${nav}Posts?page=${page}`)
    .then((response) => response.json())
    .then((json) => {
      const allPosts = document.querySelector("#allPost");
      const navigator = document.createElement("div");
      json.posts.forEach((element) => {
        //Creating each post div
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
          // If user already likes current post, create an unlike button        
          if (element.likes.includes(actualUser)) {
            const unlikeButton = document.createElement("button");
            unlikeButton.className = "btn btn-danger";
            unlikeButton.innerHTML = "Unlike";
            unlikeButton.addEventListener("click", function () {
              unlikePost(element.id, likesNumber);
            });
            postDiv.append(unlikeButton);
            // else create like button
          } else {
            const likeButton = document.createElement("button");
            likeButton.className = "btn btn-primary";
            likeButton.innerHTML = "Like";
            likeButton.addEventListener("click", function () {
              likePost(element.id, likesNumber);
            });
            postDiv.append(likeButton);
          }
          // If user is author of the post, create edit button
          if(element.username === actualUser){
            const editButton = document.createElement("button")
            editButton.className = "btn btn-primary";
            editButton.innerHTML = "Edit";
            editButton.dataset.toggle = "modal" ;
            editButton.dataset.target = `#editPostModal${element.id}`;
            const editPostModal = document.createElement("div");
            //Modal for popup edit of a post
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
            //never resolved  why saveChanges = document.querySelector(`#saveChanges${element.id}`); didnt fetch the button element
            const saveChanges = postDiv.lastElementChild.lastElementChild.lastElementChild.lastElementChild.lastElementChild.firstElementChild
            saveChanges.addEventListener("click", function(){
              const content = document.querySelector(`#textArea_${element.id}`).value;
              editPost(element.id, content);
            });
            
          }
        } 
        allPosts.append(postDiv);        
      });
      // if this is the first and last page of pagination, dont show any buttons
      if (json.lastPage && page === 1) {
        console.log(json.lastPage && page === 1);
      } else if (page === 1){
        navigator.innerHTML= `
        <nav aria-label="Page navigation example">
          <ul class="pagination">
            <li class="page-item"><a class="page-link" href="?page=${page+1}">Next</a></li>
          </ul>
        </nav>
        `
      //If is last page show only the previous button
      } else if (json.lastPage){
        navigator.innerHTML= `
        <nav aria-label="Page navigation example">
          <ul class="pagination">
            <li class="page-item"><a class="page-link" href="?page=${page-1}">Previous</a></li>
          </ul>
        </nav>
      `
      //If is first page, only show next button
      } else {
        navigator.innerHTML= `
        <nav aria-label="Page navigation example">
          <ul class="pagination">
            <li class="page-item"><a class="page-link" href="?page=${page-1}">Previous</a></li>
            <li class="page-item"><a class="page-link" href="?page=${page+1}">Next</a></li>
          </ul>
        </nav>
      `
      }
      allPosts.append(navigator)
    })
    .catch((error) => console.error(error));
}

//Function for creating a new post
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

//Function for liking a new post
function likePost(postID, likesNumber) {
  document.querySelector(`#span${postID}`).innerHTML = likesNumber + 1;
  fetch(`/like/${postID}`);
  location.reload()
}

//Function for unliking a new post
function unlikePost(postID, likesNumber) {
  document.querySelector(`#span${postID}`).innerHTML = likesNumber - 1;
  fetch(`/unlike/${postID}`)
  location.reload()
}

//Function for editing a new post
function editPost(postID, content){
  fetch(`/editPost/${postID}`, {
    method: "PUT",
    body: JSON.stringify({
      content: content,
    })
  }).then(()=>location.reload()) 
}
