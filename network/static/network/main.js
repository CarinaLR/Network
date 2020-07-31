document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#show_posts")
    .addEventListener("click", () => load_posts());
});

function load_posts(userposts) {
  // Show more post and hide sample
  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#compose-post").style.display = "none";

  if (userposts === "userposts") {
    // Load inbox emails
    fetch("/posts/userposts")
      .then((response) => response.json())
      .then((posts) => {
        posts.forEach(add_posts);
      });
  }
}
