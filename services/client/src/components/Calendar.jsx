import React from 'react'
import BigCalendar from 'react-big-calendar'
import moment from 'moment'
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css'
import '../css/calendar.css'

// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);

const Calendar = props => (
  <div className='calendar-container'>
    <BigCalendar
      events={[]}
    />
  </div>
);

export default Calendar;
