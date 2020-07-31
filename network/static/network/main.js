document.addEventListener("DOMContentLoaded", function () {
  document
    .querySelector("#show_posts")
    .addEventListener("click", () => load_posts());
});

function load_posts() {
  // Show more post and hide sample
  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#compose-post").style.display = "none";

  // if (mailbox === "inbox") {
  //   // Load inbox emails
  //   fetch("/emails/inbox")
  //     .then((response) => response.json())
  //     .then((emails) => {
  //       emails.forEach(add_emailsInbox);
  //     });
  // }
  // if (mailbox === "sent") {
  //   // Load sent emails
  //   fetch("/emails/sent")
  //     .then((response) => response.json())
  //     .then((emails) => {
  //       emails.forEach(add_emailsSent);
  //     });
  // }
  // if (mailbox === "archive") {
  //   // Load archive emails
  //   fetch("/emails/archive")
  //     .then((response) => response.json())
  //     .then((emails) => {
  //       emails.forEach(add_emailsArchive);
  //     });
  // }
}
