const http = require('http');
const cors = require('cors');

const corsOptions = {
    origin: '*',
    credentials: true,
    optionSuccessStatus: 200,
};

const server = http.createServer((req, res) => {
    if (req.method === 'POST') {
        let body = '';
        req.on('data', (chunk) => {
            body += chunk.toString();
        });
        req.on('end', () => {
            console.log(`Received POST request with body: ${body}`);
            res.end('Received POST request');
        });
    } else {
        res.end('Hello World!');
    }
});

const express = require('express');
const app = express();

app.use(cors(corsOptions));
server.listen(8001, () => {
    console.log('Server running on port 8001');
});