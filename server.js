// Cargar modulos y crear nueva aplicacion
var express = require("express");
var app = express();
var bodyParser = require('body-parser');
var azure = require('azure');
app.use(bodyParser.json()); // soporte para bodies codificados en jsonsupport
app.use(bodyParser.urlencoded({ extended: true })); // soporte para bodies codificados

var serviceBusService = azure.createServiceBusService("Endpoint=sb://service-bus-queue.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=2JoqjrWyYZMOnHGtFBhtPDfGhauso3y0krQGqA0PpSw=");

//Ejemplo: GET http://localhost:8080/items
app.get('/concierto', function(req, res, next) {
    res.send('Get all');
});


//Ejemplo: POST http://localhost:8080/items
app.post('/concierto', function(req, res) {
    console.log(req.body);
    var data = req.body.num;
    console.log(data);

    var message = {
        //body: JSON.stringify(data)
        body: data
        };
    serviceBusService.sendQueueMessage('queue_so', message, function(error){
        if(!error){
            // message sent
        }
    });

    res.send('Add ' + data);
});

var server = app.listen(8080, function () {
    console.log('Server is running..');
});