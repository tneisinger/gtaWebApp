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

// Assume that the dataObject has all the keys that the modelObject has, but
// the dataObject also has other key-value pairs.  This function will create a
// new object that has only the keys of the modelObject, and fill those keys
// with the corresponding data from the dataObject.
//
// Example:
//
//   modelObject = {
//     first: '',
//     second: '',
//     third: ''
//   }
//
//   dataObject = {
//     zeroth: 'zero!!!',
//     first: 'first!!!',
//     second: 'second!!!',
//     third: 'third!!!',
//     fourth: 'fourth!!!'
//   }
//
//   fillObjectWith(modelObject, dataObject)
//
//   RESULT:
//   >>>    {
//   >>>      first: 'first!!!',
//   >>>      second: 'second!!!',
//   >>>      third: 'third!!!',
//   >>>    }
//
// This function does not check that all the keys in modelObject are also in
// dataObject.  This function will blow up if that is not the case.
export const fillObjectWith = (modelObject, dataObject) => {
  let result = {};
  Object.keys(modelObject).forEach(key => {
    result[key] = dataObject[key];
  })
  return result;
}
