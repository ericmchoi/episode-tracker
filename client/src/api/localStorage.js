const uuid = require('uuid/v1');

export default {
  getShows() {
    const shows = JSON.parse(window.localStorage.getItem('shows'));

    return shows || [];
  },
  addShow(info) {
    const shows = this.getShows();

    shows.push({ id: uuid(), ...info });
    window.localStorage.setItem('shows', JSON.stringify(shows));
  },
  deleteShow(id) {
    let shows = this.getShows();

    shows = shows.filter(show => show.id !== id);
    window.localStorage.setItem('shows', JSON.stringify(shows));
  },
  editShow(id, info) {
    const shows = this.getShows();

    const idx = shows.findIndex(show => show.id === id);

    shows[idx] = { ...shows[idx], ...info };
    window.localStorage.setItem('shows', JSON.stringify(shows));
  },
};
