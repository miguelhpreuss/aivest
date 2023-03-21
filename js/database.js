const mysql = require('mysql2');

// Crie uma conexão com o banco de dados
const connection = mysql.createConnection({
  host: 'localhost',
  user: '<seu_usuario>',
  password: '<sua_senha>',
  database: '<seu_banco_de_dados>'
});

// Conecte-se ao banco de dados
connection.connect((err) => {
  if (err) throw err;
  console.log('Conectado ao banco de dados MySQL!');
});

// Realize uma consulta ao banco de dados
connection.query('SELECT * FROM tabela', (err, rows, fields) => {
  if (err) throw err;

  console.log('Resultado:', rows);
});

// Feche a conexão com o banco de dados
connection.end((err) => {
  if (err) throw err;
  console.log('Conexão encerrada.');
});
