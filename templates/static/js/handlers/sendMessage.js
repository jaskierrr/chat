import { loadRoom, showPage, state } from "../state/stateManager.js";

export function handleSendMessage(payload) {
  console.log('Новое сообщение:', payload);
    showPage('room')
    state.currentRoom = payload.room
    console.log('State:', state)
    loadRoom(payload)
}

