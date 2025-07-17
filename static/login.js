document.getElementById("loginForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;

  localStorage.setItem("username", username);
  localStorage.setItem("email", email);

  window.location.href = "index.html";
});
