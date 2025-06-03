import { loadUsersList, showPage } from "../state/stateManager.js";

export function handleGetUsersList(payload) {
    console.log('Список пользователей:', payload);
    showPage('users')
    loadUsersList(payload)
}

