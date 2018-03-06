import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Home from '../Home';

test('Home renders properly', () => {
  const wrapper = shallow(<Home/>);
  const element = wrapper.find('p');
  expect(element.length).toBe(1);
  expect(element.text()).toBe('Home goes here.');
});

test('Home renders a snapshot properly', () => {
  const tree = renderer.create(<Home/>).toJSON();
  expect(tree).toMatchSnapshot();
});
