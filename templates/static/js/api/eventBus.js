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
    const { channel, payload } = message;
    const hs = this.handlers[channel] || [];
    hs.forEach(h => h(payload));
  }
};

