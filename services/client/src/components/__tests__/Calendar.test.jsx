import React from 'react';
import { shallow, mount } from 'enzyme';
import BigCalendar from 'react-big-calendar';

import Calendar from '../Calendar';
import CalendarToolbar from '../CalendarToolbar';


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
};

global.localStorage = new LocalStorageMock;


describe('Calendar', () => {
  let props = {
    events: [],
    setEvents: jest.fn(),
  };
  let mountedCalendar;
  const calendar = () => {
    if (!mountedCalendar) {
      mountedCalendar = mount(
          <Calendar {...props} />
      );
    }
    return mountedCalendar;
  }

  beforeEach(() => {
    props = {
      events: [],
      setEvents: jest.fn(),
    };
    mountedCalendar = undefined;
  });

  it('always renders a div', () => {
    const divs = calendar().find('div');
    expect(divs.length).toBeGreaterThan(0);
  });
});
