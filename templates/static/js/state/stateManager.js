// Здесь только логика изменения контента на странице
export const state = {
    currentUserToken: null,
    currentUser: null,
    rooms: new Map(),    // key: roomId, value: { name, participants: [], messages: [] }
    roomList: [],        // array of RoomSummary
};

const pages = {
    login_page: document.getElementById('page-login'),
    chats: document.getElementById('page-chats'),
    chat: document.getElementById('page-chat'),
};

export function showPage(page) {
    Object.values(pages).forEach(p => p.classList.remove('active'));
    pages[page].classList.add('active');
}

export function loadRooms(data) {
    console.log(data)
    const ul = document.getElementById('chats-list');
    ul.innerHTML = '';
    data.rooms.forEach(chat => {
        const li = document.createElement('li');
        li.innerText = chat.name;
        li.addEventListener('click', () => selectChat(chat.id, chat.name));
        ul.appendChild(li);
    });
}
