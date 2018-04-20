import React from 'react';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router';
import { withRouter } from 'react-router-dom';
import { spy } from 'sinon';
import mockAxios from 'jest-mock-axios';

import App from '../../App';
import Calendar from '../Calendar';
import NavBar from '../NavBar';
import FormModal from '../FormModal';
import { LocalStorageMock } from '../../testUtils';


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

      // Use withRouter so that url info gets passed into App props.
      // This will allow us to check the current url of the App in our tests.
      const AppWithRouter = withRouter(App);

      memRoutedApp = mount(
        <MemoryRouter initialEntries={routerHistory}>
          <AppWithRouter />
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

  // Instantiate the goodUserStatusResponse var in a wider scope
  let goodUserStatusResponse;

  describe('when a valid authToken is saved in localStorage', () => {
    beforeEach(() => {
      // This is needed for setTimeouts to work in tests
      jest.useFakeTimers();

      global.localStorage = new LocalStorageMock();
      window.localStorage.setItem('authToken', 'valid token wink wink');

      // Create a date string that is five seconds in the future to mock the
      // authToken expire time that would be returned from the server.
      let t = new Date();
      t.setSeconds(t.getSeconds() + 5);
      let expireTime = t.toString();

      // Create a mock of a good response object from the server
      goodUserStatusResponse = {
        status: 200,
        data: {
          user: {
            email: 'fake@fake.com',
            id: 13,
            username: 'Fred',
          },
          expiration: expireTime,
        },
      };

    });

    afterEach(() => {
      // This is needed for setTimeouts to work in tests
      jest.runAllTimers();

      mockAxios.reset();
    });

    it('should set the userLoggedIn state value to true', () => {
      wrappedApp();

      mockAxios.mockResponse(goodUserStatusResponse);

      setTimeout(() => {
        expect(appInstance().state.userLoggedIn).toBe(true);
      }, 0);
    });

    it('should set the username state value correctly', () => {
      wrappedApp();

      mockAxios.mockResponse(goodUserStatusResponse);

      setTimeout(() => {
        expect(appInstance().state.username).toBe(
          goodUserStatusResponse.data.user.username,
        );
      }, 0);

    });

    it('should automatically logout after expiration time has passed', () => {
      // Create a date string that is a few milliseconds in the future.  By the
      // time that we test if the user is still logged in, this time should be
      // in the passed and the user should be automatically logged out.
      let t = new Date();
      t.setMilliseconds(t.getMilliseconds() + 1);
      let expireTime = t.toString();

      goodUserStatusResponse.expiration = expireTime;

      wrappedApp();

      mockAxios.mockResponse(goodUserStatusResponse);

      expect(setTimeout).toHaveBeenCalledTimes(1);
      expect(setTimeout).toHaveBeenLastCalledWith(
        expect.any(Function), expect.any(Number)
      );

      setTimeout(() => {
        expect(appInstance().state.userLoggedIn).toBe(true);
        expect(appInstance().state.username).toBe(
          goodUserStatusResponse.data.user.username,
        );
      }, 0);

      jest.runAllTimers();

      expect(appInstance().state.userLoggedIn).toBe(false);
      expect(appInstance().state.username).toBe('');
    });

    describe('when starting from the calendar page', () => {
      beforeEach(() => {
        routerHistory = ['/calendar'];
      });

      it('should not redirect to homepage if user is logged in', () => {
        wrappedApp();

        mockAxios.mockResponse(goodUserStatusResponse);

        setTimeout(() => {
          expect(appInstance().state.username).toBe(
            goodUserStatusResponse.data.user.username,
          );
          expect(appInstance().props.location.pathname).toBe('/calendar')
        }, 0);
      });


    });
  });

  describe('when an invalid authToken is saved in localStorage', () => {
    beforeEach(() => {
      // This is needed for setTimeouts to work in tests
      jest.useFakeTimers();

      global.localStorage = new LocalStorageMock();
      window.localStorage.setItem('authToken', 'invalid token wink wink');

      // Create a date string that is five seconds in the future to mock the
      // authToken expire time that would be returned from the server.
      let t = new Date();
      t.setSeconds(t.getSeconds() + 5);
      let expireTime = t.toString();

    });

    afterEach(() => {
      // This is needed for setTimeouts to work in tests
      jest.runAllTimers();

      mockAxios.reset();
    });

    const badUserStatusResponse = {
      status: 401,
      data: {
        status: 'fail',
        message: 'Provide a valid auth token',
      },
    };

    it('should set the userLoggedIn state value to false', () => {
      wrappedApp();

      mockAxios.mockError(badUserStatusResponse);

      setTimeout(() => {
        expect(appInstance().state.userLoggedIn).toBe(false);
      }, 0);
    });

    it('should set the username state value to null', () => {
      wrappedApp();

      mockAxios.mockError(badUserStatusResponse);

      setTimeout(() => {
        expect(appInstance().state.username).toBe(null);
      }, 0);

    });

    describe('and starting from the calendar page', () => {

      it('should redirect to homepage because user not signed in', () => {
        wrappedApp();

        mockAxios.mockError(badUserStatusResponse);

        setTimeout(() => {
          expect(appInstance().props.location.pathname).toBe('/')
        }, 0);
      });

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
});
