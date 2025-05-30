import { loadRooms, showPage } from "../state/stateManager.js";

export function handleGetRoomsList(payload) {
    // Предполагаем, что payload соответствует GetRoomsListResponse
    console.log('Список комнат:', payload);
    showPage('rooms')
    loadRooms(payload)
    // Здесь update UI или state
}

