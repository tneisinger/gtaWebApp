import React from 'react';
import { Navbar, Nav, NavItem, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const NavBar = (props) => (
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
      {props.userIsAdmin &&
        <Nav>
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
          <Button
            className="auth-btn"
            bsStyle="primary"
            onClick={props.onAuthBtnClick}
          >
            {props.userIsAdmin ? 'Logout' : 'Login'}
          </Button>
        </NavItem>
      </Nav>
    </Navbar.Collapse>
  </Navbar>
)

export default NavBar;
