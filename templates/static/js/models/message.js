export class Message {
  constructor({ id, sender, content, timestamp }) {
    this.id = id;
    this.sender = new User(sender); // связь с моделью User
    this.content = content;
    this.timestamp = new Date(timestamp);
  }

  formatTime() {
    return this.timestamp.toLocaleTimeString('ru-RU');
  }

  isEmpty() {
    return this.content.trim().length === 0;
  }
}

