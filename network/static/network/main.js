document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#post-button").addEventListener("click", () => {
    const box_post = document.createElement("div");
    box_post.innerHTML = "I'm in All Post view";
  });
});
