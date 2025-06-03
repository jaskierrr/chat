export let wsClient = null;


export function initWS(token) {
    wsClient = new WebSocketClient({
        url: 'ws://localhost:8080/ws',
        token
    });
}

export class WebSocketClient {
    constructor({ url, token }) {
        this.url = url;
        this.token = token;
        this.socket = null;
        this.listeners = [];
    }

    connect() {
        const wsUrl = `${this.url}?token=${this.token}`;
        console.log('wsURL')
        console.log(wsUrl)
        this.socket = new WebSocket(wsUrl);

        this.socket.addEventListener('open', () => {
            console.log('WS connected');
        });

        this.socket.addEventListener('message', evt => {
            console.log('message event')
            let msg;
            try { msg = JSON.parse(evt.data); }
            catch (e) { console.error('Invalid JSON', evt.data); return; }
            console.log(msg)
            this.notifyListeners(msg);
        });

        //this.socket.addEventListener('close', () => {
        //  console.log('WS closed, reconnecting in 3s...');
        //  setTimeout(() => this.connect(), 3000);
        //});
    }

    notifyListeners(message) {
        this.listeners.forEach(cb => cb(message));
    }

    onMessage(callback) {
        console.log('onMessage')
        this.listeners.push(callback);
    }

    send(payload) {
        //const data = { channel, payload };
        console.log('send:', payload)
        this.socket.send(JSON.stringify(payload));
    }
}

