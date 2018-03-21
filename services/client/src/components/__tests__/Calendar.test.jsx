import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Calendar from '../Calendar';

const idesOfMarch = new Date(2018, 2, 15);
const getEvents = () => { console.log('get events') }

test('Calendar renders properly', () => {
  const wrapper = shallow(
                    <Calendar
                      currentDate={idesOfMarch}
                      getEvents={getEvents}
                    />
                  );
  const calendarElement = wrapper.find('.calendar-container');
  expect(calendarElement.length).toBe(1);
});
//test('Calendar renders a snapshot properly', () => {
  //const tree = renderer.create(<Calendar/>).toJSON();
  //expect(tree).toMatchSnapshot();
//});
