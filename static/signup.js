document.getElementById("signupForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const username = document.getElementById("signupUsername").value;
  const email = document.getElementById("signupEmail").value;

  localStorage.setItem("username", username);
  localStorage.setItem("email", email);

  window.location.href = "index.html";
});
