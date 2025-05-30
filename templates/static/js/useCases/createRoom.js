import { wsClient } from "../api/websocketClient.js";
import { RequestConstructor } from "../services/requestService.js";
import { state } from "../state/stateManager.js";

export function createRoom(users) {
    if (state.currentUser && users) {
        console.log(users)
        const message_data = new RequestConstructor('/create_room', {src_user_id: state.currentUser.id, other_users_ids: users})
        const message = message_data.toJSON()
        console.log("REQUEST", message)
        wsClient.send(message)
    }
};
