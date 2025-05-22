export class Room {
  constructor({ id, name, messages = [], participants = [] }) {
    this.id = id;
    this.name = name;
    this.messages = messages.map(m => new Message(m));
    this.participants = participants.map(u => new User(u));
  }

  addMessage(msg) {
    this.messages.push(new Message(msg));
  }

  lastMessage() {
    return this.messages[this.messages.length - 1];
  }
}

