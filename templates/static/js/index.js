import { initWS, wsClient } from './api/websocketClient.js';
import { EventBus } from './api/eventBus.js';
import { handleGetRoomsList } from './handlers/getRoomsList.js';
import { handleGetRoom } from './handlers/getRoom.js';
import { handleSendMessage } from './handlers/sendMessage.js';
import { state, showPage } from './state/stateManager.js';
import { User } from './models/user.js';
import { getRoomsListRequest } from './useCases/getRoomsList.js';



async function init(token) {
    //const token = await Login();


    initWS(token)

    // Прокидываем сообщения в шину
    wsClient.onMessage(msg => EventBus.publish(msg));

    // Подписываемся на события из спецификации
    EventBus.subscribe('/get_rooms_list', handleGetRoomsList);
    EventBus.subscribe('/get_room', handleGetRoom);
    EventBus.subscribe('/send_message', handleSendMessage);


    console.log('in init')


    wsClient.connect();

    showPage('chats')

    document.getElementById('get-rooms-list')?.addEventListener('click', getRoomsListRequest)
    //link()

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
            const user_data = await res.json()
            state.currentUser = new User(user_data)
            console.log('User:', state.currentUser);
            state.currentUserToken = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1] || '';
            console.log('Token:', state.currentUserToken);
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


