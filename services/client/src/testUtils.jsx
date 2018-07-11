// Utilities for test files

// A class for mocking localStorage
export class LocalStorageMock {
  constructor() {
    this.store = {};
  }

  clear() {
    this.store = {};
  }

  getItem(key) {
    return this.store[key] || null;
  }

  setItem(key, value) {
    this.store[key] = value.toString();
  }

  removeItem(key) {
    delete this.store[key];
  }
}

// A function that simulates a click on a day-range of the React Big Calendar
// dayStart and dayEnd are integers that represent the day of the month.
// dayStart should always be <= dayEnd.  This function will not check
// that condition.
export function clickCalendarDays(app, calendar, dayStart, dayEnd) {
  // create the startDate date object
  let today = new Date();
  const thisYear = today.getFullYear();
  const thisMonth = today.getMonth();
  const startDate = new Date(thisYear, thisMonth, dayStart);

  // if dayEnd was provided, use it to create the endDate date object.
  // Otherwise, just use the startDate as the endDate
  const endDate = dayEnd ? new Date(thisYear, thisMonth, dayEnd) : startDate;

  const clickedDates = {
    start: startDate,
    end: endDate,
  };

  // Fake a calendar click by directly running Calendar's onSelectSlot method.
  app.find(calendar).prop('onSelectSlot')(clickedDates);

  app.update();

  return clickedDates;
}
