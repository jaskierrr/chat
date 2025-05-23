export class User {
  constructor({ id, username}) {
    this.id = id;
    this.username = username;
  }

  displayName() {
    return this.username || 'Аноним';
  }

  isValid() {
    return typeof this.id === 'string' && this.username.length > 0;
  }
}

