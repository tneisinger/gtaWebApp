import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Calendar from '../Calendar';

test('Calendar renders properly', () => {
  const wrapper = shallow(<Calendar/>);
  const calendarElement = wrapper.find('.calendar-container');
  expect(calendarElement.length).toBe(1);
});
//test('Calendar renders a snapshot properly', () => {
  //const tree = renderer.create(<Calendar/>).toJSON();
  //expect(tree).toMatchSnapshot();
//});
