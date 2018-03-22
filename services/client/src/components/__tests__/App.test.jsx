import React from 'react';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router';
import BigCalendar from 'react-big-calendar';

import App from '../../App';
import NavBar from '../NavBar';
import Calendar from '../Calendar';
import FormModal from '../FormModal';


test('App renders without crashing', () => {
  const wrapper = shallow(<App/>);
});

describe('App', () => {
  let routerHistory;
  let mountedApp;
  const app = () => {
    if (!mountedApp) {
      mountedApp = mount(
        <MemoryRouter initialEntries={routerHistory}>
          <App/>
        </MemoryRouter>
      );
    }
    return mountedApp;
  }

  beforeEach(() => {
    routerHistory = undefined;
    mountedApp = undefined;
  });

  it('always renders a div', () => {
    const divs = app().find('div');
    expect(divs.length).toBeGreaterThan(0);
  });

  it('always renders a NavBar', () => {
    expect(app().find(NavBar).length).toBe(1);
  });

  it('always renders a FormModal', () => {
    expect(app().find(FormModal).length).toBe(1);
  });

  describe('the outer div', () => {
    it('contains everything else that gets rendered', () => {
      expect(app().children().length).toEqual(1);
    });
  });

  describe('when on the calendar page', () => {
    beforeEach(() => {
      routerHistory = ['/calendar']
    });

    // Tests for the calendar page go here
  });
});
