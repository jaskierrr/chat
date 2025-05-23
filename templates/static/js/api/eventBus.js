// Шина событий
export const EventBus = {
  handlers: {},

  subscribe(channel, handler) {
    if (!this.handlers[channel]) {
      this.handlers[channel] = [];
    }
    this.handlers[channel].push(handler);
  },

  publish(message) {
    console.log('in publish func')
    console.log(message)
    const { head, body } = message;
    const hs = this.handlers[head.event] || [];
    hs.forEach(h => h(body));
  }
};

