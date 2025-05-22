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
