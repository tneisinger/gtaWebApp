import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Budget from '../Budget';

test('Budget renders properly', () => {
  const wrapper = shallow(<Budget/>);
  const element = wrapper.find('p');
  expect(element.length).toBe(1);
  expect(element.text()).toBe('Budget goes here.');
});

test('Budget renders a snapshot properly', () => {
  const tree = renderer.create(<Budget/>).toJSON();
  expect(tree).toMatchSnapshot();
});
