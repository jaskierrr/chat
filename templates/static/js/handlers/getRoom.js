import { loadRoom, showPage, state } from "../state/stateManager.js";

export function handleGetRoom(payload) {
    console.log('Данные комнаты:', payload);
    showPage('room')
    state.currentRoom = payload.room
    console.log('State:', state)
    loadRoom(payload)
}

