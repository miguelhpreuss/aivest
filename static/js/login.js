function login(user, password){
    window.location.href = "ai.html"
    
    fetch('../api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        u: user,
        pw: password
      })
    })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error(error));
}

function signup(user, email, name, password){
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

function accountRecovery(email){
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

function checkAvailableUsername(username){

}


