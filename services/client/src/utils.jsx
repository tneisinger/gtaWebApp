// Convenient utility functions

// Make and return a shallow copy of the input object
export const copy = object => Object.assign({}, object);

// Make and return a deep copy of the input object
export const deepcopy = object => JSON.parse(JSON.stringify(object));

// convert a datestring of the form yyyy-mm-dd to a js Date
export const datestringToDate = datestring => {
  const year = parseInt(datestring.slice(0,4), 10);
  const month = parseInt(datestring.slice(5,7), 10) - 1;
  const day = parseInt(datestring.slice(8,10), 10);
  return new Date(year, month, day);
};
