const express = require('express');
const server = express();


server.listen(8217);

server.use('/getData',(req,res)=>{
	res.send([Math.random()*9000,Math.random()*9000,Math.random()*9000])

});

server.use(express.static('./'));