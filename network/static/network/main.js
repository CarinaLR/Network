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
