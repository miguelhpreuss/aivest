function validar() {
  var email = document.forms["loginForm"]["email"].value;
  var senha = document.forms["loginForm"]["senha"].value;
  var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  let ver_senha = senha.length >= 6
  document.getElementById("erro_senha").hidden = ver_senha;

  let ver_email = re.test(email)
  document.getElementById("erro_email").hidden = ver_email;

  document.getElementById("botao-login").disabled = !(ver_senha && ver_email);
}

function login() {
  var email = document.getElementById("email").value;
  var senha = document.getElementById("senha").value;

  fetch('../api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: email,
      senha: senha
    }),
    mode: 'cors'
  })
    .then(response => {
      return response.text()
    })
    .then(data => {
      response = JSON.parse(data);
      let erro = response["error"];
      document.getElementById("erro_email_incorreto").hidden = erro != "Email incorreto";
      document.getElementById("erro_senha_incorreta").hidden = erro != "Senha incorreta";
      if (response.token){
        window.location.href = "ai.html"
      }
    })
    .catch(error => console.error(error));

}

function signup(user, email, name, password) {
  fetch('../api/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      n: name,
      u: user,
      e: email,
      pw: password
    })
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}

function accountRecovery(email) {
  fetch('../api/accountrecovery', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      e: email
    })
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
}

function checkAvailableUsername(username) {

}


