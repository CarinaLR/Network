document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#show_posts")
    .addEventListener("click", () => load_posts());
  document
    .querySelector("#edit_profile")
    .addEventListener("click", () => edit_profile());
  document
    .querySelector("#follow_profile")
    .addEventListener("click", () => unfollow_button());
  document
    .querySelector("#edit_post")
    .addEventListener("click", () => edit_post(post_id));
});

function load_posts() {
  // Show more post and hide sample
  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#compose-post").style.display = "none";
}

function edit_profile() {
  // Show more edit profile and hide user profile
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#compose-post").style.display = "block";
}

function unfollow_button() {
  // Show more edit profile and hide user profile
  document.querySelector("#follow_profile").style.display = "none";
}

function edit_post(post_id) {
  console.log("post_id -> ", post_id);
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
  console.log("IDK ->", response);
  // Get post content to populate textarea
  let content_post = response.post_content;
  console.log("content ->", content_post);

  let new_textarea = document.querySelector("#content");
  new_textarea.innerHTML = content_post;

  // Get div where the edit post view will be display
  // const blockDiv = document.querySelector(".compose-edit");

  // Create elements for edit post
  // const newDiv = document.createElement("div");
  // newDiv.className = "newDiv";

  // const titlePage = document.createElement("h3");
  // titlePage.id = "titlePage";
  // titlePage.innerHTML = "Edit Post";

  // const formPost = document.createElement("form");
  // formPost.className = "form-group";
  // formPost.method = "POST";

  // const textarea = document.createElement("textarea");
  // textarea.id = "content";
  // textarea.className = "form-group";
  // textarea.name = "content";
  // textarea.innerHTML = content_post;

  // const break_p = document.createElement("br");

  // const input_edit = document.createElement("input");
  // input_edit.type = "submit";
  // input_edit.id = "post-button";
  // input_edit.className = "btn btn-primary";
  // input_edit.value = "Save";
  // input_edit.name = "save";

  // // Append all children to the main div to display block
  // formPost.appendChild(textarea);
  // formPost.appendChild(break_p);
  // formPost.appendChild(input_edit);

  // newDiv.appendChild(titlePage);
  // newDiv.appendChild(formPost);
  // blockDiv.appendChild(newDiv);

  update_post(response);
}

function update_post(post_obj) {
  let post = post_obj;
  console.log("post -- ", post);

  //Put request to update post.
  // fetch(`/emails/${post_id}`, {
  //   method: "PUT",
  //   body: JSON.stringify({
  //     content: true,
  //   }),
  // });
}
