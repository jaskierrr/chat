import { state } from "../state/stateManager.js";

export class Message {
  constructor(text) {
    this.user = state.currentUser; 
    this.room = state.currentRoom; 
    this.text = text;
  }

  isEmpty() {
    return this.text.trim().length === 0;
  }
}

