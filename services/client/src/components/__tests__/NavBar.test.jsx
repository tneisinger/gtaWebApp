import React from 'react';
import { shallow, mount } from 'enzyme';
import renderer from 'react-test-renderer';
import { MemoryRouter as Router } from 'react-router-dom';

import NavBar from '../NavBar';

describe('The NavBar component', () => {

  let props = {
    onAuthBtnClick: undefined,
    userLoggedIn: undefined,
    username: undefined,
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
      userLoggedIn: undefined,
      username: undefined,
    };

    // throw away the old mountedNavBar
    mountedNavBar = undefined;

    // throw away the old navbarTree
    navbarTree = undefined;
  });

  describe('when the user is logged in', () => {
    beforeEach(() => {
      props.userLoggedIn = true;
      props.username = 'Tyler';
    });

    it('should render the calendar, budget, and expenses links', () => {
      const navLeft = navbar().find('.navbar-left');
      expect(navLeft.length).toBe(1);
      expect(navLeft.find('a').length).toBeGreaterThan(1);
    });

    it('the text of the login/logout button should be "Logout"', () => {
      const authBtn = navbar().find('button.auth-btn');
      expect(authBtn.text()).toBe('Logout');
    });

    it('the user greeting text should be rendered', () => {
      const userGreeting = navbar().find('span.user-greeting');
      expect(userGreeting.text()).toMatch(props.username);
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });

  });

  describe('when the user is not logged in', () => {
    beforeEach(() => {
      props.username = null;
      props.userLoggedIn = false;
    });

    it('should NOT render the calendar, budget, and expenses links', () => {
      const navLeft = navbar().find('.navbar-left');
      expect(navLeft.length).toBe(0);
    });

    it('the text of the login/logout button should be "Login"', () => {
      const authBtn = navbar().find('button.auth-btn');
      expect(authBtn.text()).toMatch('Login');
    });

    it('there should be no user greeting', () => {
        const userGreeting = navbar().find('span.user-greeting');
        expect(userGreeting.length).toBe(0);
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });
  });

  describe('when the userLoggedIn prop is not set', () => {
    beforeEach(() => {
      props.username = null;
      props.userLoggedIn = null;
    });

    it('should NOT render the calendar, budget, and expenses links', () => {
      const navLeft = navbar().find('.navbar-left');
      expect(navLeft.length).toBe(0);
    });

    it('No login/logout button should be rendered', () => {
      const authBtn = navbar().find('button.auth-btn');
      expect(authBtn.length).toBe(0);
    });

    it('there should be no user greeting', () => {
        const userGreeting = navbar().find('span.user-greeting');
        expect(userGreeting.length).toBe(0);
    });

    it('should render properly', () => {
      expect(tree()).toMatchSnapshot();
    });
  });

});
