$(document).ready(() => {
    $('#form-send-msg').on('submit', (e) => {
        e.preventDefault();
    });

    const socket = io.connect('http://127.0.0.1:5000');
    const username = $('#username').text();
    socket.on('connect', () => {
        socket.send({'username': 'Service message', 'msg':'User' + username + ' has connected!'});
    });

    $('#send-msg').on('click', () => {
        socket.send({
            'msg': $('#message-input').val(),
            'username':username
        });
        $('message-input').val('')
    });

    socket.on('message', data => {
        if(data.msg.length > 0){
            if(data.username === 'Service message'){
                $('#messages').append(`<li class="text-muted"><strong>${data.username}:</strong> ${data.msg}</li>`);
            } else{
                $('#messages').append(`<li><strong>${data.username}:</strong> ${data.msg}</li>`);
            }
            console.log('Получено сообщение')
        }
    });
});