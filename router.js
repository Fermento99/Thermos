const express = require("express");
const dbmanager = require('./dbmanager')
const router = express();

router.use(express.static('build'))

router.get('/', (req, res) => {
    res.sendFile(__dirname + "/build/index.html")
})

router.get('/temp/now', (req, res) => {
    dbmanager.now((response) => {res.json(response);});
})

router.get('/temp/hist/:room/:limit', (req, res) => {
    dbmanager.temp(req.params.room, req.params.limit, (response) => {res.json(response)})
})

router.post('/newtemp', (req, res) => {
    dbmanager.add(req.query, res)
})


router.listen(3001, () => console.log("listening on port 3001"))