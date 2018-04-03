import React from 'react';
import { mount, shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import { Route, Redirect } from 'react-router-dom';
import { MemoryRouter } from 'react-router';

import PrivateRoute from '../PrivateRoute';
import Calendar from '../Calendar';

jest.mock('../Calendar');
Calendar.mockImplementation(() => 'Calendar');

describe('The PrivateRoute component', () => {
  // Initialize the props that will get passed into Calendar
  let props = {
    userLoggedIn: false,
    componentProps: {
      propOne: 'first',
      propTwo: 'second',
    },
    path: "/somepath",
    component: Calendar,
  };

  let mountedPrivateRoute;

  let treeOfPrivateRoute;

  let routerHistory;

  const mounted = () => {
    if (!mountedPrivateRoute) {
      mountedPrivateRoute = mount(
        <MemoryRouter initialEntries={routerHistory}>
          <PrivateRoute {...props} />
        </MemoryRouter>,
      );
    }
    return mountedPrivateRoute;
  };

  const tree = () => {
    if (treeOfPrivateRoute) {
      treeOfPrivateRoute = renderer.create(
        <MemoryRouter initialEntries={routerHistory}>
          <PrivateRoute {...props} />
        </MemoryRouter>,
      );
    }
    return treeOfPrivateRoute;
  }

  beforeEach(() => {
    routerHistory = undefined;
    mountedPrivateRoute = undefined;
    treeOfPrivateRoute = undefined;
  });

  it('should always render a Route component', () => {
    const wrapper = shallow(<PrivateRoute {...props} />);
    expect(wrapper.find(Route).length).toBeGreaterThan(0);
  });

  describe('when userLoggedIn is false', () => {

    beforeEach(() => {
      routerHistory = ['/somepath'];
    });

    it('should redirect the client', () => {
      expect(mounted().instance().history.location.pathname).toBe("/");
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });
  });


  describe('when userLoggedIn is true', () => {

    beforeEach(() => {
      routerHistory = ['/somepath'];
      props.userLoggedIn = true;
    });

    it('should not redirect the client', () => {
      expect(mounted().instance().history.location.pathname).toBe("/somepath");
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });
  });

});
