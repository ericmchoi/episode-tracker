export default (url, key) => {
  const headers = {
    Authorization: `Bearer ${key}`,
    'Content-Type': 'application/json',
  };

  const getShows = () => fetch(url, {
    method: 'GET',
    headers,
  })
    .then(response => response.json());

  const addShow = info => fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(info),
  });

  const deleteShow = id => fetch(`${url}/${id}`, {
    method: 'DELETE',
    headers,
  });

  const editShow = (id, info) => fetch(`${url}/${id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(info),
  });

  return {
    getShows,
    addShow,
    deleteShow,
    editShow,
  };
};
