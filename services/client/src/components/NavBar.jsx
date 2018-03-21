import React from 'react';
import { Navbar, Nav, NavItem, Button } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

const NavBar = (props) => (
  <Navbar inverse collapseOnSelect>
    <Navbar.Header>
      <Navbar.Brand>
        <LinkContainer to="/">
          <span>{props.title}</span>
        </LinkContainer>
      </Navbar.Brand>
      <Navbar.Toggle />
    </Navbar.Header>
    <Navbar.Collapse>
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
      <Nav pullRight>
        <NavItem eventKey={1}>
          <Button bsStyle="primary" onClick={props.onAuthBtnClick}>
            Login
          </Button>
        </NavItem>
      </Nav>
    </Navbar.Collapse>
  </Navbar>
)

export default NavBar;
