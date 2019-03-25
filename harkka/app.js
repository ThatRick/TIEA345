const express = require('express');
const socketIO = require('socket.io');
const SerialPort = require('serialport');
const Readline = require('@serialport/parser-readline')

const app = express();
const server = app.listen(8080);
const io = socketIO(server);

let position = 0;
let throttle = 0;

// Serve public folder
app.use(express.static('public'));

// Setup serial connection
const serialPathMac = '/dev/cu.usbmodem14101';
const serialPathPi = '/dev/ttyACM0';
const port = new SerialPort(serialPathPi, {
    baudRate: 9600,
}, err => {
    if (err) return console.log('Serial open error:', err.message);
    console.log('Serial port opened');
});

const parser = new Readline();
port.pipe(parser);

// Receive line of data
parser.on('data', line => {
    console.log('Received:', line);
    io.emit('monitor', line);
});

// Write data to serial port
function sendSerialData(data) {
    const msg = data.toString() + '\n';
    port.write(msg, err => {
        if (err) return console.log('Serial write error:', err.message);
        console.log('Serial data written:', data);
    });
}

// Handle new client connection
io.on('connection', socket => {
    console.log('New connection:');
    console.log(socket.id);

    // send current position value to new client
    socket.emit('position', position);

    // received new position value from client
    socket.on('position', value => {
        position = value;
        // send new position value to all other clients
        socket.broadcast.emit('position', value);
        // send new value to serial port
        const msg = 'P' + Math.floor(value*10);
        sendSerialData(msg);
    });
    // received new throttle value from client
    socket.on('throttle', value => {
        throttle = value;
        // send new position value to all other clients
        socket.broadcast.emit('throttle', value);
        // send new value to serial port
        const msg = 'T' + Math.floor(value*10);
        sendSerialData(msg);
    });
    // received new command from client
    socket.on('command', value => {
        console.log('New command:', value);
        sendSerialData(value);
    });
});
