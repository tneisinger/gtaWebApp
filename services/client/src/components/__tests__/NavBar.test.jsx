import React from 'react';
import { shallow, mount } from 'enzyme';
import renderer from 'react-test-renderer';
import { MemoryRouter as Router } from 'react-router-dom';

import NavBar from '../NavBar';

describe('The NavBar component', () => {

  let props = {
    onAuthBtnClick: undefined,
    userIsAdmin: undefined,
  };

  // Initialize a variable that will hold the mounted NavBar component
  let mountedNavBar;

  // Initialize a variable that will hold the navbar tree for snapshots
  let navbarTree;

  // Define a function that will always return the mounted NavBar component.
  // If the mountedNavBar hasn't been created yet for the current test,
  // create it and then return it.
  const navbar = () => {
    if (!mountedNavBar) {
      mountedNavBar = mount(
        <Router location='/'><NavBar {...props} /></Router>
      );
    }
    return mountedNavBar;
  }

  const tree = () => {
    if (!navbarTree) {
      navbarTree = renderer.create(
        <Router location='/'><NavBar {...props} /></Router>
      ).toJSON()
    }
    return navbarTree;
  }

  beforeEach(() => {
    // Reset the prop values for each test
    props = {
      onAuthBtnClick: undefined,
      userIsAdmin: undefined,
    };

    // throw away the old mountedNavBar
    mountedNavBar = undefined;

    // throw away the old navbarTree
    navbarTree = undefined;
  });

  describe('when userIsAdmin is set to true', () => {
    beforeEach(() => {
      props.userIsAdmin = true;
    });

    it('should render the calendar, budget, and expenses links', () => {
      const navbarNavs = navbar().find('.navbar-nav');
      expect(navbarNavs.length).toBeGreaterThan(1);
      expect(navbarNavs.first().find('li').length).toBeGreaterThan(1);
    });

    it('the text of the login/logout button should be "Logout"', () => {
      const authBtn = navbar().find('button.auth-btn');
      expect(authBtn.text()).toBe('Logout');
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });

  });

  describe('when userIsAdmin is set to false', () => {
    beforeEach(() => {
      props.userIsAdmin = false;
    });

    it('should NOT render the calendar, budget, and expenses links', () => {
      const navbarNavs = navbar().find('.navbar-nav');
      expect(navbarNavs.length).toBe(1);
      expect(navbarNavs.find('button').length).toBe(1);
    });

    it('the text of the login/logout button should be "Login"', () => {
      const authBtn = navbar().find('button.auth-btn');
      expect(authBtn.text()).toBe('Login');
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });
  });

  describe('when userIsAdmin is set to null', () => {
    beforeEach(() => {
      props.userIsAdmin = null;
    });

    it('should NOT render the admin links or the auth button', () => {
      const navbarNavs = navbar().find('.navbar-nav');
      expect(navbarNavs.length).toBe(0);
      expect(navbarNavs.find('button').length).toBe(0);
    });

    it('the login/logout button should not be rendered', () => {
      const authBtn = navbar().find('button.auth-btn');
      expect(authBtn.length).toBe(0);
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });
  });

});
