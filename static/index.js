document.addEventListener("DOMContentLoaded", () => {
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        document.querySelector("#snd").onsubmit = (e) => {
            e.preventDefault();
            const message = document.querySelector("#msg").value;
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();

            socket.emit('send message', {'message': message, 'timestamp': timestamp});
            document.querySelector("#msg").value = '';
        };
    });

    socket.on('show message', data => {
        const li = document.createElement('li');
        li.innerHTML = '<' + `${data.timestamp}` + '>-' + '[' + `${data.user}` + ']:____' + `${data.message}`;
        let ul = document.querySelector("#messages");
        document.querySelector("#messages").insertBefore(li, ul.childNodes[0]);

        document.querySelector("#msg").value = '';
    });
  });
