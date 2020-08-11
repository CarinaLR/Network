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
  // const query_selector = document.querySelector(".compose-post").click(() => {
  //   let id_post = $(this).data("id");
  //   console.log("id_post -> ", id_post);
  // });
  // console.log("query_selector - ", query_selector);

  if (post_id) {
    // document.querySelector("#titlePage").style.display = "none";
    // document.querySelector("#inputText").style.display = "none";
    // document.querySelector("#timeInfo").style.display = "none";
    // Get value from data-id
    get_class = document.querySelector(".compose-post");
    get_id = get_class.getAttribute("data-id");
    console.log("get_id - ", get_id);
    // Get request by id.
    fetch(`/post/${post_id}`)
      .then((response) => response.json())
      .then((response) => {
        if (response) {
          console.log("response", response);
          post_view(response);
        } else {
          console.log("not found");
        }
      });

    console.log("I'm here");
  }

  // const blockDiv = document.createElement("div");
  // blockDiv.className = "compose-edit";

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

  // const break_p = document.createElement("br");

  // const input_edit = document.createElement("input");
  // input_edit.type = "submit";
  // input_edit.id = "post-button";
  // input_edit.className = "btn btn-primary";
  // input_edit.value = "Save";
  // input_edit.name = "post";

  // formPost.appendChild(textarea);
  // formPost.appendChild(break_p);
  // formPost.appendChild(input_edit);

  // newDiv.appendChild(titlePage);
  // newDiv.appendChild(formPost);

  // // Show textarea post and hide post
  // document.querySelector(".compose-post").style.display = "none";
  // document.querySelector(".compose-edit").style.display = "block";
}

function post_view(post_id) {
  console.log("IDK ->", post_id);
}
