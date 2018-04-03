// Convenient utility functions

// Make and return a shallow copy of the input object
export const copy = object => Object.assign({}, object);

// Make and return a deep copy of the input object
export const deepcopy = object => JSON.parse(JSON.stringify(object));
