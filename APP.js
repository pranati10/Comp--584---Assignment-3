const express = require('express');
const mysql = require('mysql2');

const app = express();
app.use(express.json());

const connection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'example',
  database: 'assign',
  port: 13313
});

// Middleware to handle database connection errors
app.use((req, res, next) => {
  if (connection && connection.state === 'disconnected') {
    res.status(500).send('Database connection was lost');
  } else {
    next();
  }
});

app.get('/businesses', (req, res) => {
  const { page = 1, limit = 25, name, city, category } = req.query;

  let query = 'SELECT * FROM business WHERE 1=1';
  if (name) query += ` AND name LIKE '%${name}%'`;
  if (city) query += ` AND city LIKE '%${city}%'`;
  if (category) query += ` AND categories LIKE '%${category}%'`;

  const offset = (page - 1) * limit;
  query += ` LIMIT ${offset}, ${limit}`;

  connection.query(query, (error, results) => {
    if (error) {
      return res.status(500).send('Error retrieving data from the database');
    }
    res.json(results);
  });
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
