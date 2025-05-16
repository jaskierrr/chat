const pages = {
    login_page: document.getElementById('page-login'),
    chats: document.getElementById('page-chats'),
    chat: document.getElementById('page-chat'),
};
const room_id = 0;
var user = null;
var socket = null;
var token = null;

let currentChatId = null;

function showPage(page) {
    Object.values(pages).forEach(p => p.classList.remove('active'));
    pages[page].classList.add('active');
}

// CHECK TOKEN ON STARTUP
(async function() {
    console.log('Immediate check!');
    await fetch('/token', { method: 'POST' })
        .then(res => {
            if (res.status === 404) {
                console.error('Token invalid (404)');
            } else if (!res.ok) {
                console.error(`Somthing wrong, error: ${res.status}`);
            } else {
                return res.json();
            }
        })
        .then(data => {
            if (data) {
                user = data
                showPage('chats');
                loadChats();
            }
        })
        .catch(err => {
            console.error('Сетевая ошибка или exception:', err);
        });
})();

// LOGIN
document.getElementById('login-form').addEventListener('submit', async e => {
    e.preventDefault();
    const login = document.getElementById('login').value;
    const pass = document.getElementById('password').value;
    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ login: login, password: pass })
        });

        if (res.ok) {
            //console.log(res.json())
            user = await res.json()
            //result
            //    .then(res => {
            //        window.user = res;           // присваиваем значение перемису
            //        console.log(user); // теперь можно работать с userData
            //    })
            //    .catch(error => {
            //        console.error(error);
            //    });
            token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1] || '';
            console.log(token)
            socket = new WebSocket('ws://localhost:8080/ws' + '?token=' + token);
            showPage('chats');
            //loadChats();
        } else {
            const data = await res.json();
            document.getElementById('login-error').innerText = data.error || 'Ошибка авторизации';
        }
    } catch (err) {
        document.getElementById('login-error').innerText = 'Сервер недоступен: ' + err;
    }
});

socket.onmessage = function(event) {
    console.log('START onmessage')
    const message = event.data;
    console.log("RESPONSE", message)
};

function getRooms() {
    // отправить json с
    console.log('START getROOMS')
    if (user.id) {
        message = prepareJson(user.id)
        console.log("REQUEST", message)
        socket.send(message);
    }
}

function prepareJson(user_id) {
    console.log('prepareJson start')

    const jsonData = {
        head: {
            type: "command",
            command: "/get_rooms_list",
            timestamp: new Date().toISOString(),
            token: token
        },
        body: {
            id: user_id
        }
    };

    return JSON.stringify(jsonData)
}

// LOAD CHATS
async function loadChats(chats) {
    //console.log(user.id)
    //var list = ''
    //try {
    //    const res = await fetch('/rooms', {
    //        method: 'POST',
    //        headers: {'Content-Type': 'application/json'},
    //        body: JSON.stringify({id: user.id})
    //    });
    //    list = await res.json();
    //} catch (err) {
    //    alert('Не удалось загрузить список чатов');
    //}

    console.log(chats)
    const ul = document.getElementById('chats-list');
    ul.innerHTML = '';
    //for (let element of list.rooms) {
    //    console.log(element);
    //}
    chats.rooms.forEach(chat => {
        console.log(chat)
        const li = document.createElement('li');
        li.innerText = chat.name;
        li.addEventListener('click', () => selectChat(chat.id, chat.name));
        ul.appendChild(li);
    });
}

// SELECT CHAT
function selectChat(id, name) {
    currentChatId = id;
    document.getElementById('chat-title').innerText = name;
    showPage('chat');
    loadMessages(id);
}

document.getElementById('back-to-chats').addEventListener('click', () => {
    showPage('chats');
});

// LOAD MESSAGES
async function loadMessages(chatId) {
    try {
        const res = await fetch(`/api/chats/${chatId}/messages`);
        const messages = await res.json();
        const container = document.getElementById('messages-container');
        container.innerHTML = '';
        messages.forEach(msg => {
            const div = document.createElement('div');
            div.classList.add('message');
            div.innerHTML = `<div class=\"author\">${msg.author}</div><div class=\"text\">${msg.text}</div>`;
            container.appendChild(div);
        });
        container.scrollTop = container.scrollHeight;
    } catch (err) {
        alert('Не удалось загрузить сообщения');
    }
}

// SEND MESSAGE
document.getElementById('message-form').addEventListener('submit', async e => {
    e.preventDefault();
    const text = document.getElementById('message-input').value;
    if (!text) return;
    try {
        const res = await fetch(`/api/chats/${currentChatId}/messages`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        if (res.ok) {
            document.getElementById('message-input').value = '';
            loadMessages(currentChatId);
        } else {
            alert('Ошибка при отправке сообщения');
        }
    } catch (err) {
        alert('Сервер недоступен');
    }
});
