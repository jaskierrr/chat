// Сетап запросов на сервер
//
//
// body это dict

import { state } from "../state/stateManager.js";

export class RequestConstructor {
    constructor(event, body) {
        this.head = new RequestHead(event);
        this.body = body;

    }

    toJSON() {
        return {
            head: this.head,
            body: this.body,
        }
    }

}

export class RequestHead {
    constructor(event) {
        this.event = event;
        this.timestamp = new Date().toISOString();
        this.token = state.currentUserToken
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
