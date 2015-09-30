
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/autoreload');

    //receive details from server
    socket.on('newData', function(msg) {
        console.log("Received html string" + msg.payload);
        $('#st_table').html(msg.payload);
    });
});
