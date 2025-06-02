import { wsClient } from "../api/websocketClient.js";
import { RequestConstructor } from "../services/requestService.js";
import { state } from "../state/stateManager.js";

export function sendMessage(message) {
    if (message) {
        console.log(message)
        const message_data = new RequestConstructor('/send_message', {message})
        const res = message_data.toJSON()
        console.log("REQUEST", res)
        // wsClient.send(message)
    }
};
