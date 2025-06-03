import { wsClient } from "../api/websocketClient.js";
import { Message } from "../models/message.js";
import { RequestConstructor } from "../services/requestService.js";

export function sendMessage(text) {
    const message = new Message(text)
    if (!message.isEmpty()) {
        const message_data = new RequestConstructor('/send_message', {message})
        const res = message_data.toJSON()
        console.log("REQUEST", res)
        wsClient.send(res)
    }
};
