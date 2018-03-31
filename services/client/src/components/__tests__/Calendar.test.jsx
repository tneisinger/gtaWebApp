import React from 'react';
import moxios from 'moxios';
import { mount } from 'enzyme';

import Calendar from '../Calendar';


// create a class to mock localStorage
class LocalStorageMock {
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

global.localStorage = new LocalStorageMock();


describe('The Calendar component', () => {
  // Define a date to use for the tests
  const idesOfMarch = new Date(2018, 2, 15);

  // Initialize the props that will get passed into Calendar
  let props = {
    defaultDate: idesOfMarch,
    events: [],
    setEvents: jest.fn(),
    onSelectSlot: jest.fn(),
  };

  // Initialize a variable that will hold the mounted Calendar component
  let mountedCalendar;

  // Define a function for mocking an empty response to an /admin/events
  // get request
  const mockEmptyGetEventsResponse = () => {
    const request = moxios.requests.mostRecent();
    request.respondWith({
      status: 200,
    });
  };

  // Define a function that will always return the mounted calendar component.
  // If the mountedCalendar hasn't been created yet for the current test,
  // create it and then return it.
  const calendar = () => {
    if (!mountedCalendar) {
      mountedCalendar = mount(<Calendar {...props} />);
    }
    return mountedCalendar;
  };

  beforeEach(() => {
    // Reset the prop values for each test
    props = {
      defaultDate: idesOfMarch,
      events: [],
      setEvents: jest.fn(),
      onSelectSlot: jest.fn(),
    };

    // throw away the old mountedCalendar
    mountedCalendar = undefined;

    // prepare to mock axios requests
    moxios.install();
  });

  afterEach(() => {
    // Tear down axios mocking
    moxios.uninstall();
  });

  it('should render without error', () => {
    const divs = calendar().find('div');

    // Mock a response to the getEvents axios request
    moxios.wait(mockEmptyGetEventsResponse);

    expect(divs.length).toBeGreaterThan(0);
  });
});
