const uuid = require('uuid/v1');

export default () => {
  let shows = [];

  try {
    shows = JSON.parse(window.localStorage.getItem('shows')) || [];
  } catch {
    shows = [];
  }

  const saveShows = () => window.localStorage.setItem('shows', JSON.stringify(shows));

  const getShows = () => new Promise((resolve) => { resolve([...shows]); });

  const addShow = (info) => new Promise((resolve) => {
    shows.push({ id: uuid(), ...info });
    saveShows();
    resolve();
  });

  const deleteShow = (id) => new Promise((resolve) => {
    shows = shows.filter((show) => show.id !== id);
    saveShows();
    resolve();
  });

  const editShow = (id, info) => new Promise((resolve) => {
    const idx = shows.findIndex((show) => show.id === id);
    shows[idx] = { ...shows[idx], ...info };
    saveShows();
    resolve();
  });

  return {
    getShows,
    addShow,
    deleteShow,
    editShow,
  };
};
