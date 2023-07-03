function validar() {
  var email = document.forms["loginForm"]["email"].value;
  var senha = document.forms["loginForm"]["senha"].value;
  var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  let ver_senha = senha.length >= 6
  document.getElementById("erro_senha").hidden = ver_senha;

  let ver_email = re.test(email)
  document.getElementById("erro_email").hidden = ver_email;

  document.getElementById("botao-login").disabled = !(ver_senha && ver_email);
  document.getElementById("botao-login").hidden = false

  document.forms["loginForm"]["nome"].style = "margin-top: 2cm;"
}

function validarCadastro() {
  var email = document.forms["loginForm"]["email"].value;
  var senha = document.forms["loginForm"]["senha"].value;
  var nome = document.forms["loginForm"]["nome"].value;
  var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  let ver_senha = senha.length >= 6
  document.getElementById("erro_senha").hidden = ver_senha;

  let ver_nome = nome.length >= 3
  document.getElementById("erro_nome").hidden = ver_nome;

  let ver_email = re.test(email)
  document.getElementById("erro_email").hidden = ver_email;
  document.getElementById("botao-signup").disabled = !(ver_senha && ver_email && ver_nome);

  document.getElementById("botao-login").hidden = true
  document.forms["loginForm"]["nome"].style = "margin-top: 0cm;"
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
        window.location.href = "ai"
      }
    })
    .catch(error => console.error(error));

}

function signup() {
  var email = document.getElementById("email").value;
  var senha = document.getElementById("senha").value;
  var nome = document.getElementById("nome").value;

  fetch('../api/signup', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      nome: nome,
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
      if (response.token){
        window.location.href = "ai"
      }
      let erro = response["error"];
      document.getElementById("erro_email_cadastrado").hidden = erro != "Email já cadastrado";
    })
    .catch(error => console.error(error));

}

function checkAvailableUsername(username) {

}


