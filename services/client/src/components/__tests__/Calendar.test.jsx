import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Calendar from '../Calendar';

test('Calendar renders properly', () => {
  const wrapper = shallow(<Calendar/>);
  const element = wrapper.find('p');
  expect(element.length).toBe(1);
  expect(element.text()).toBe('Calendar goes here.');
});

test('Calendar renders a snapshot properly', () => {
  const tree = renderer.create(<Calendar/>).toJSON();
  expect(tree).toMatchSnapshot();
});
