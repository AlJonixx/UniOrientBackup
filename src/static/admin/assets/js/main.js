
function checkPassword() {
    var password = document.getElementById("password").value;
    var cPassword = document.getElementById("confirm-password").value;
    var message = document.getElementById("message");
      if (password == cPassword) {
        message.textContent = "Passwords Match";
        message.style.backgroundColor = "green";
      } 
      else{
        message.textContent = "Passwords don't Match";
        message.style.backgroundColor = "red";
      }
  }