import { loadRoom, showPage } from "../state/stateManager.js";

export function handleGetRoom(payload) {
  console.log('Данные комнаты:', payload);
    showPage('room')
    loadRoom(payload)
}

