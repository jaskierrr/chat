const pages = {
    login_page: document.getElementById('page-login'),
    chats: document.getElementById('page-chats'),
    chat: document.getElementById('page-chat'),
};
const room_id = 0;
var user = null;
var room = null;
var socket = null;
var token = null;

let currentChatId = null;
//
// function showPage(page) {
//     Object.values(pages).forEach(p => p.classList.remove('active'));
//     pages[page].classList.add('active');
// }

// CHECK TOKEN ON STARTUP
//(async function() {
//    console.log('Immediate check!');
//    await fetch('/token', { method: 'POST' })
//        .then(res => {
//            if (res.status === 404) {
//                console.error('Token invalid (404)');
//            } else if (!res.ok) {
//                console.error(`Somthing wrong, error: ${res.status}`);
//            } else {
//                return res.json();
//            }
//        })
//        .then(data => {
//            if (data) {
//                user = data
//                showPage('chats');
//                loadRooms();
//            }
//        })
//        .catch(err => {
//            console.error('Сетевая ошибка или exception:', err);
//        });
//})();
//
// NEW WS CONNECTION
function openWS(token) {
    socket = new WebSocket('ws://localhost:8080/ws' + '?token=' + token);

    socket.onopen = function() {
        console.log('Соединение установлено');
    };

    socket.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            console.log('Распарсенные данные:', data);
            // Дополнительная обработка данных
            checkWSCommand(data)
        } catch (error) {
            console.error('Ошибка при разборе JSON:', error);
        }
    };
}

function checkWSCommand(msg) {
    if (msg.head.type == 'response' && msg.head.command == '/get_rooms_list') {
        loadRooms(msg)
    }
}

// LOGIN
//document.getElementById('login-form').addEventListener('submit', async e => {
async function Login(event) {
    event.preventDefault();
    const form = document.getElementById('login-form');
    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password');
    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login: username, password: password })
        });

        if (res.ok) {
            user = await res.json()
            token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1] || '';
            console.log(token);
            showPage('chats');
            openWS(token);
            getRoomsList();

        } else {
            const data = await res.json();
            document.getElementById('login-error').innerText = data.error || 'Ошибка авторизации';
        }
    } catch (err) {
        document.getElementById('login-error').innerText = 'Сервер недоступен: ' + err;
    }
}
//});

//socket.onmessage = function(event) {
//    console.log('START onmessage')
//    const message = event.data;
//    console.log("RESPONSE", message)
//};
//
function getRoomsList() {
    // отправить json с
    console.log('START getRoomList')
    if (user.id) {
        message = prepareJson('command', '/get_rooms_list', { id: user.id })
        console.log("REQUEST", message)
        socket.send(message);
    }
}

function getRoom() {
    // отправить json с
    console.log('START getRoom')
    if (currentChatId) {
        message = prepareJson('command', '/get_room', { id: currentChatId })
        console.log("REQUEST", message)
        socket.send(message);
    }
}

function sendMessage(message_text) {
    // отправить json с
    console.log('START sendMessage')
    if (currentChatId) {
        message = prepareJson('command', '/send_message', { room_id: currentChatId, text: message_text })
        console.log("REQUEST", message)
        socket.send(message);
    }
}



function prepareJson(type, command, body) {
    const jsonData = {
        head: {
            type: type,
            command: command,
            timestamp: new Date().toISOString(),
            token: token
        },
        body: body
    };

    return JSON.stringify(jsonData)
}

// LOAD ROOMS
//async function loadRooms(chats) {
//    //console.log(chats)
//    const ul = document.getElementById('chats-list');
//    ul.innerHTML = '';
//    chats.body.rooms.forEach(chat => {
//        const li = document.createElement('li');
//        li.innerText = chat.name;
//        li.addEventListener('click', () => selectChat(chat.id, chat.name));
//        ul.appendChild(li);
//    });
//}

// SELECT CHAT
function selectChat(id, name) {
    currentChatId = id;
    document.getElementById('chat-title').innerText = name;
    showPage('chat');
    loadMessages();
}

document.getElementById('back-to-chats').addEventListener('click', () => {
    showPage('chats');
});

// LOAD MESSAGES
async function loadMessages() {
    getRoom()
    //try {
    //    const res = await fetch(`/api/chats/${chatId}/messages`);
    //    const messages = await res.json();
    //    const container = document.getElementById('messages-container');
    //    container.innerHTML = '';
    //    messages.forEach(msg => {
    //        const div = document.createElement('div');
    //        div.classList.add('message');
    //        div.innerHTML = `<div class=\"author\">${msg.author}</div><div class=\"text\">${msg.text}</div>`;
    //        container.appendChild(div);
    //    });
    //    container.scrollTop = container.scrollHeight;
    //} catch (err) {
    //    alert('Не удалось загрузить сообщения');
    //}
}

// SEND MESSAGE
document.getElementById('message-form').addEventListener('submit', async e => {
    e.preventDefault();
    const text = document.getElementById('message-input').value;
    if (!text) return;
    sendMessage(text)
    //try {
    //    const res = await fetch(`/api/chats/${currentChatId}/messages`, {
    //        method: 'POST',
    //        headers: { 'Content-Type': 'application/json' },
    //        body: JSON.stringify({ text })
    //    });
    //    if (res.ok) {
    //        document.getElementById('message-input').value = '';
    //        loadMessages(currentChatId);
    //    } else {
    //        alert('Ошибка при отправке сообщения');
    //    }
    //} catch (err) {
    //    alert('Сервер недоступен');
    //}
});
