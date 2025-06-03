// Здесь логика запроса на сервер и обработка ответа от сервера

import { wsClient } from "../api/websocketClient.js";
import { RequestConstructor } from "../services/requestService.js";
import { state } from "../state/stateManager.js";

export function getRoomsListRequest() {
    // отправить json с
    console.log('START getRoomList REQUEST')
    if (state.currentUser) {
        const message_data = new RequestConstructor('/get_rooms_list', {id: state.currentUser.id});
        const message = message_data.toJSON()
        console.log("REQUEST", message)
        wsClient.send(message)
    }
};
