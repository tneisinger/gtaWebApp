import React from 'react';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router';
import { spy } from 'sinon';
import mockAxios from 'jest-mock-axios';

import App from '../../App';
import NavBar from '../NavBar';
import FormModal from '../FormModal';
import { LocalStorageMock } from './testUtils';


global.localStorage = new LocalStorageMock();

test('App renders without crashing', () => {
  const wrapper = shallow(<App />);
  expect(wrapper.find('div').length).toBeGreaterThan(0);
});

describe('The main App component', () => {
  //  instantiate a variable that will hold the mounted App, wrapped in a
  //  MemoryRouter component.  This will get passed to tests to check the
  //  status of the app.
  let memRoutedApp;

  // instantiate a variable that will hold the router history for a given test
  let routerHistory;

  // Return the mounted MemoryRouter that wraps the App component.  If the
  // memRoutedApp has not yet been created for the current test, this function
  // will create it before returning it.
  const wrappedApp = () => {
    if (!memRoutedApp) {
      memRoutedApp = mount(
        <MemoryRouter initialEntries={routerHistory}>
          <App />
        </MemoryRouter>,
      );
    }
    return memRoutedApp;
  };

  // Return a direct reference to the mounted App component.  This is useful
  // when you want check the state of the App component.
  const appInstance = () => wrappedApp().find(App).instance();

  // Before each test, reset the routerHistory and memRoutedApp to undefined
  beforeEach(() => {
    routerHistory = undefined;
    memRoutedApp = undefined;
    global.localStorage = new LocalStorageMock();
  });

  it('always renders a div', () => {
    const divs = wrappedApp().find('div');
    expect(divs.length).toBeGreaterThan(0);
  });

  it('has an outer div that contains everything', () => {
    expect(wrappedApp().children().length).toEqual(1);
  });

  it('always renders a NavBar', () => {
    expect(wrappedApp().find(NavBar).length).toBe(1);
  });

  it('always renders a FormModal', () => {
    expect(wrappedApp().find(FormModal).length).toBe(1);
  });

  it('runs the componentDidMount method', () => {
    const componentDidMountSpy = spy(App.prototype, 'componentDidMount');
    wrappedApp();
    expect(App.prototype.componentDidMount.calledOnce).toEqual(true);
    componentDidMountSpy.restore();
  });


  describe('when a valid authToken is saved in localStorage', () => {
    beforeEach(() => {
      // This is needed for setTimeouts to work in tests
      jest.useFakeTimers();

      global.localStorage = new LocalStorageMock();
      window.localStorage.setItem('authToken', 'valid token wink wink');
    });

    afterEach(() => {
      // This is needed for setTimeouts to work in tests
      jest.runAllTimers();

      mockAxios.reset();
    });

    const goodResponse = {
      status: 200,
      data: {
        user: {
          email: 'fake@fake.com',
          id: 13,
          username: 'Fred',
        },
      },
    };

    it('should set the userLoggedIn state value to true', () => {
      wrappedApp();

      mockAxios.mockResponse(goodResponse);

      setTimeout(() => {
        expect(appInstance().state.userLoggedIn).toBe(true);
      }, 0);
    });

    it('should set the username state value correctly', () => {
      wrappedApp();

      mockAxios.mockResponse(goodResponse);

      setTimeout(() => {
        expect(appInstance().state.username).toBe(
          goodResponse.data.user.username,
        );
      }, 0);

    });
  });


  describe('when no authToken is saved in localStorage', () => {
    it('should set the userLoggedIn state value to false', () => {
      expect(appInstance().state.userLoggedIn).toBe(false);
    });

    it('should have a username state value of the empty string', () => {
      expect(appInstance().state.username).toBe('');
    });
  });


  describe('when on the calendar page', () => {
    beforeEach(() => {
      routerHistory = ['/calendar'];
    });

    // Tests for the calendar page go here
  });
});
