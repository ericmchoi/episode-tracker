/**
 * Object that acts as an API shim for the remote storage of show data.
 */

export default (url, key) => {
  const headers = {
    Authorization: `Bearer ${key}`,
    'Content-Type': 'application/json',
  };

  // TODO: Research/follow best practices for FetchAPI error handling
  const responseHandler = (response) => {
    if (!response.ok) throw new Error(response.status);

    return response;
  };

  const getShows = () => fetch(url, {
    method: 'GET',
    headers,
  })
    .then(responseHandler)
    .then(response => response.json());

  const addShow = info => fetch(url, {
    method: 'POST',
    headers,
    body: JSON.stringify(info),
  }).then(responseHandler);

  const deleteShow = id => fetch(`${url}/${id}`, {
    method: 'DELETE',
    headers,
  }).then(responseHandler);

  const editShow = (id, info) => fetch(`${url}/${id}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(info),
  }).then(responseHandler);

  return {
    getShows,
    addShow,
    deleteShow,
    editShow,
  };
};
