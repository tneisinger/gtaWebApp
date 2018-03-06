import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Expenses from '../Expenses';

test('Expenses renders properly', () => {
  const wrapper = shallow(<Expenses/>);
  const element = wrapper.find('p');
  expect(element.length).toBe(1);
  expect(element.text()).toBe('Expenses goes here.');
});

test('Expenses renders a snapshot properly', () => {
  const tree = renderer.create(<Expenses/>).toJSON();
  expect(tree).toMatchSnapshot();
});
