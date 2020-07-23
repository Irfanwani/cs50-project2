document.addEventListener("DOMContentLoaded", () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        //Join a channel message
        socket.emit("joined");
    
        //Sending a message
        document.querySelector("#snd").onsubmit = (e) => {
            e.preventDefault();
            const message = document.querySelector("#msg").value;

            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();

            socket.emit('send message', {'message': message, 'timestamp': timestamp});
            document.querySelector("#msg").value = '';
        };

        //Leaving a channel message 
        document.querySelector("#leave").onclick = () => {
            socket.emit("left");
        };

    });

    //Showing a message send 
    socket.on('show message', data => {
        const p = document.createElement('p');
        p.className = 'mes';
        p.innerHTML = '<' + `${data.timestamp}` + '>-' + '[' + `${data.user}` + ']: ' + `${data.message}`;
        let ul = document.querySelector("#messages");
        document.querySelector("#messages").insertBefore(p, ul.childNodes[0]);

        document.querySelector("#msg").value = '';
    });

    //Showing a joining message
    socket.on('join msg', data => {
        let timestamp = new Date;
        timestamp = timestamp.toLocaleTimeString();

        const li = document.createElement('p');
        li.innerHTML ='<' + `${timestamp}` + '>' + `${data.msg}`;
        li.className = "mes";

        let ul = document.querySelector("#messages");
        document.querySelector("#messages").insertBefore(li, ul.childNodes[0]);
    });

    //showing a channel leaving message
    socket.on("channel left", data => {
        let timestamp = new Date;
        timestamp = timestamp.toLocaleTimeString();

        const li = document.createElement('p');
        li.innerHTML ='<' + `${timestamp}` + '>' + `${data.msg}`;
        li.className = 'mes';

        let ul = document.querySelector("#messages");
        document.querySelector("#messages").insertBefore(li, ul.childNodes[0]);
    });

  });
