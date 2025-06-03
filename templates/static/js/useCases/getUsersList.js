import { wsClient } from "../api/websocketClient.js";
import { RequestConstructor } from "../services/requestService.js";
import { state } from "../state/stateManager.js";


export function getUsersList() {
    if (state.currentUser) {
        const message_data = new RequestConstructor('/get_users_list', {id: state.currentUser.id})
        const message = message_data.toJSON()
        console.log("REQUEST", message)
        wsClient.send(message)
    }
};
