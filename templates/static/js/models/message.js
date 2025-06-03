import { state } from "../state/stateManager.js";

export class Message {
  constructor(text) {
    this.user_id = state.currentUser.id; 
    this.room_id = state.currentRoom.id; 
    this.text = text;
  }

  isEmpty() {
    return this.text.trim().length === 0;
  }
}

