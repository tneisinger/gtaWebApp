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

// convert a Date object into a string of the form yyyy-mm-dd
export const dateToDatestring = date => {
  var mm = date.getMonth() + 1; // getMonth() is zero-based
  var dd = date.getDate();

  return [date.getFullYear(),
          (mm>9 ? '' : '0') + mm,
          (dd>9 ? '' : '0') + dd
         ].join('-');
};

// Run the fn function at the given futureDate time.
export const runCallbackAt = (futureTime, callback) => {
  const now = new Date();
  const timeDif = futureTime.getTime() - now.getTime();
  if (now < futureTime) {
    setTimeout(() => { callback(); }, timeDif);
  }
};
