import React from 'react';
import PropTypes from 'prop-types';
import { Navbar, Nav, NavItem, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const NavBar = props => (
  <Navbar inverse collapseOnSelect>
    <Navbar.Header>
      <Navbar.Brand>
        <LinkContainer to="/">
          <span>Gladtime Audio</span>
        </LinkContainer>
      </Navbar.Brand>
      <Navbar.Toggle />
    </Navbar.Header>
    <Navbar.Collapse>
      {props.userLoggedIn &&
        <Nav pullLeft>
          <LinkContainer to="/calendar">
            <NavItem eventKey={1}>Calendar</NavItem>
          </LinkContainer>
          <LinkContainer to="/budget">
            <NavItem eventKey={2}>Budget</NavItem>
          </LinkContainer>
          <LinkContainer to="/expenses">
            <NavItem eventKey={3}>Expenses</NavItem>
          </LinkContainer>
        </Nav>
      }
      <Nav pullRight>
        <NavItem eventKey={1}>
          {props.username &&
            <span className="user-greeting">
              Hi, {props.username}
            </span>
          }
        </NavItem>
        <NavItem eventKey={2}>
          {props.userLoggedIn !== null &&
            <Button
              className="auth-btn"
              bsStyle="primary"
              onClick={props.onAuthBtnClick}
            >
              {props.userLoggedIn ? 'Logout' : 'Login'}
            </Button>
          }
        </NavItem>
      </Nav>
    </Navbar.Collapse>
  </Navbar>
);

NavBar.propTypes = {
  onAuthBtnClick: PropTypes.func,
  username: PropTypes.string,
  userLoggedIn: PropTypes.oneOf([null, true, false]),
};

const defaultAuthBtnFn = () => alert('Auth button clicked!');

NavBar.defaultProps = {
  onAuthBtnClick: defaultAuthBtnFn,
  username: '',
  userLoggedIn: null,
};


export default NavBar;
