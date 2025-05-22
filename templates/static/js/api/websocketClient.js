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
      let msg;
      try { msg = JSON.parse(evt.data); }
      catch (e) { console.error('Invalid JSON', evt.data); return; }
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
    this.listeners.push(callback);
  }

  send(channel, payload) {
    const data = { channel, payload };
    this.socket.send(JSON.stringify(data));
  }
}

