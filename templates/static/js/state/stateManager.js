import { createRoom } from "../useCases/createRoom.js";

// Здесь только логика изменения контента на странице
export const state = {
    currentUserToken: null,
    currentUser: null,
    rooms: new Map(),    // key: roomId, value: { name, participants: [], messages: [] }
    roomList: [],        // array of RoomSummary
};

const pages = {
    login_page: document.getElementById('page-login'),
    rooms: document.getElementById('page-rooms'),
    users: document.getElementById('page-users'),
    room: document.getElementById('page-room'),
};

export function showPage(page) {
    Object.values(pages).forEach(p => p.classList.remove('active'));
    pages[page].classList.add('active');
}

export function showLogin() {
    showPage('page-login')
}

export function loadRooms(data) {
    console.log(data)
    const ul = document.getElementById('rooms-list');
    ul.innerHTML = '';
    data.rooms.forEach(room => {
        const li = document.createElement('li');
        li.innerText = room.name;
        li.addEventListener('click', () => selectChat(room.id, room.name));
        ul.appendChild(li);
    });
}

export function loadUsersList(data) {
    console.log(data)
    const ul = document.getElementById('users-list');
    ul.innerHTML = '';
    data.users.forEach(user => {
        const li = document.createElement('li');
        li.innerText = user.username;
        li.addEventListener('click', () => createRoom([user.id]));
        ul.appendChild(li);
    });
}
