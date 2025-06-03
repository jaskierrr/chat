// Здесь логика запроса на сервер и обработка ответа от сервера

import { wsClient } from "../api/websocketClient.js";
import { RequestConstructor } from "../services/requestService.js";

export function getRoomRequest(room_id) {
    // отправить json с
    console.log('START getRoom REQUEST')
    if (room_id) {
        const message_data = new RequestConstructor('/get_room', {id: room_id});
        const message = message_data.toJSON()
        console.log("REQUEST", message)
        wsClient.send(message)
    }
};
