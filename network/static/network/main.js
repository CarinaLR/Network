document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#edit_profile")
    .addEventListener("click", () => edit_profile());
  document
    .querySelector("#edit_post")
    .addEventListener("click", () => edit_post(post_id));
  document
    .querySelector("#like-button")
    .addEventListener("click", () => like_button());
});

function edit_profile() {
  // Show more edit profile and hide user profile
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#compose-post").style.display = "block";
}

function edit_post(post_id) {
  post_id = post_id;
  // Block to get info from post
  if (post_id) {
    // Get value from data-id
    get_class = document.querySelector(".compose-post");
    get_id = get_class.getAttribute("data-id");

    // Get request by id.
    fetch(`/post/${post_id}`)
      .then((response) => response.json())
      .then((response) => {
        if (response) {
          post_view(response);
        } else {
          console.log("not found");
        }
      });
  }
}

function post_view(response) {
  // Get post content to populate textarea
  let content_post = response.post_content;

  let new_textarea = document.querySelector("#content");
  new_textarea.innerHTML = content_post;
  // Pass information to update_post function.
  update_post(response);
}

function update_post(post_obj) {
  let post = post_obj;

  let post_id = post.post_id;

  // On submit send information to update post.
  document.querySelector("#post-form").onsubmit = () => {
    // Get value from input to update content.
    let new_content = document.getElementById("content").value;

    fetch(`/edit_post/${post_id}`, {
      method: "PUT",
      body: JSON.stringify({
        content: new_content,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        console.log("result ->", result);
      });

    //Once the post has been submitted, return false to prevent reload.
    return false;
  };
}

function like_button(post_id) {
  // Get request by id.
  fetch(`/like_post/${post_id}`)
    .then((response) => response.json())
    .then((response) => {
      console.log("The response -", response);
    });
  // Prevent reloading the page.
  return false;
}
