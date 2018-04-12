import React from 'react';
import axios from 'axios';
import mockAxios from 'jest-mock-axios';
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

global.localStorage.setItem('authToken', 'fakeAuthToken')

describe('The Calendar component', () => {
  // Define a date to use for the tests
  const idesOfMarch = new Date(2018, 2, 15);

  // Initialize the props variable that will get passed into Calendar
  let props;

  // mock the onSelectSlot function
  const mockOnSelectSlot = jest.fn();

  // mock the setCalendarEvents function
  const mockSetCalendarEvents = jest.fn(events => {
    calendar().setProps({ events: events });
  });

  // Initialize a variable that will hold the mounted Calendar component
  let mountedCalendar;

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
    // This is needed for setTimeouts to work in tests
    jest.useFakeTimers();

    mockSetCalendarEvents.mockClear();
    mockOnSelectSlot.mockClear();
    // Reset the prop values for each test
    props = {
      defaultDate: idesOfMarch,
      events: [],
      setCalendarEvents: mockSetCalendarEvents,
      onSelectSlot: mockOnSelectSlot,
    };

    // throw away the old mountedCalendar
    mountedCalendar = undefined;
  });

  afterEach(() => {
    // This is needed for setTimeouts to work in tests
    jest.runAllTimers();

    mockAxios.reset();
  });

  it('should render without error', () => {
    const divs = calendar().find('div');

    expect(divs.length).toBeGreaterThan(0);
  });

  it('should render job calendar events', () => {
    // Instantiate the calendar app for this test.
    calendar();

    // Mock a server response
    mockAxios.mockResponse({
        status: 200,
        data: {
          data: {
            expenses: [],
            jobs: [{
              amount_paid: 350,
              client: "test client",
              confirmation: "Confirmed",
              description: "some description",
              end_date: "2018-03-06",
              start_date: "2018-03-08",
              has_paid: false,
              id: 1,
              paid_to: "Gladtime Audio",
              worked_by: "Meghan",
            }],
            user: {
              email: 'fake@email.com',
              id: 1,
              username: 'Fred',
            }
          }
        }
      });

    let url = `${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/events`;
    let requestData = {
      "headers": { "Authorization": "Bearer fakeAuthToken"},
      "params": {"end_date": "2018-03-31", "start_date": "2018-02-25"}
    };
    expect(mockAxios.get).toHaveBeenCalledWith(url, requestData);

    // Put expects in a setTimeout so that they run after everything has
    // rendered
    setTimeout(() => {
      expect(mockSetCalendarEvents.mock.calls.length).toBe(1);
      const eventElems = calendar().find('.rbc-event');
      expect(eventElems.length).toBe(1);
      const eventText = eventElems.find('.rbc-event-content').text();
      expect(eventText).toMatch('test client');
    }, 0);
  });
});
