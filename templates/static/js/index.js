import { WebSocketClient } from './api/websocketClient.js';
import { EventBus } from './api/eventBus.js';
import { handleGetRoomsList } from './handlers/getRoomsList.js';
import { handleGetRoom } from './handlers/getRoom.js';
import { handleSendMessage } from './handlers/sendMessage.js';
import { state, showPage } from './state/stateManager.js';



async function init(token) {
    //const token = await Login();
    const wsClient = new WebSocketClient({
        url: 'ws://localhost:8080/ws',
        token
    });

    // Прокидываем сообщения в шину
    wsClient.onMessage(msg => EventBus.publish(msg));

    // Подписываемся на события из спецификации
    EventBus.subscribe('/get_rooms_list', handleGetRoomsList);
    EventBus.subscribe('/get_room', handleGetRoom);
    EventBus.subscribe('/send_message', handleSendMessage);

    wsClient.connect();

    showPage('chats')

    // Пример отправки запроса: получить список комнат
    //wsClient.send('/get_rooms_list', { /* параметры GetRoomsListRequest */ });
};

document.getElementById('login-form').addEventListener('submit', async event => {
    console.log('login start')
    event.preventDefault();
    const form = document.getElementById('login-form');
    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password');
    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, password: password })
        });

        if (res.ok) {
            const user = await res.json()
            console.log(user);
            state.currentUserToken = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1] || '';
            console.log(state.currentUserToken);
            init(state.currentUserToken)
            //showPage('chats');
            //openWS(token);
            //getRoomsList();

        } else {
            const data = await res.json();
            document.getElementById('login-error').innerText = data.error || 'Ошибка авторизации';
        }
    } catch (err) {
        document.getElementById('login-error').innerText = 'Сервер недоступен: ' + err;
    }
});


