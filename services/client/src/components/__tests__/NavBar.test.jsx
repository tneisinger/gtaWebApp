import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
import { MemoryRouter as Router } from 'react-router-dom';

import NavBar from '../NavBar';

test('NavBar renders properly', () => {
  const wrapper = shallow(<NavBar/>);
  const element = wrapper.find('span');
  expect(element.length).toBe(1);
});

test('NavBar renders a snapshot properly', () => {
  const tree = renderer.create(
    <Router location="/"><NavBar/></Router>
  ).toJSON();
  expect(tree).toMatchSnapshot();
});
