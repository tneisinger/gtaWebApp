import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import BigCalendar from 'react-big-calendar';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css';

import CalendarToolbar from './CalendarToolbar';
import '../css/calendar.css';
import { datestringToDate } from '../utils';


// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);


class Calendar extends Component {
  constructor(props) {
    super(props);

    this.bindScopes([
      'onNavigate',
    ]);
  }

  componentDidMount() {
    this.getEvents();
  }

  onNavigate(date) {
    const [startDate, endDate] = this.getDateRange(date);
    return [startDate, endDate];
  }

  getEvents() {
    const [start_date, end_date] = this.getDateRange();
    axios.get(`${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/events`, {
      params: {
        start_date,
        end_date,
      },
      headers: {
        Authorization: `Bearer ${window.localStorage.getItem('authToken')}`,
      },
    }).then((res) => {
      const bcEvents = createBigCalendarEvents(res.data.data);
      this.props.setCalendarEvents(bcEvents);
    }).catch((err) => {
      // TODO: [err.response.data, err.response.status];
    });
  }

  setEventProps(event, start, end, isSelected) {
    return {
      className: 'custom-class-name other-class-name',
    }
  }

  getDateRange(inputDate) {
    const date = inputDate || this.props.defaultDate;
    const startDate = moment(dates.firstVisibleDay(date)).format('YYYY-MM-DD');
    const endDate = moment(dates.lastVisibleDay(date)).format('YYYY-MM-DD');
    return [startDate, endDate];
  }

  bindScopes(keys) {
    keys.forEach((key) => {
      this[key] = this[key].bind(this);
    });
  }

  render() {
    return (
      <BigCalendar
        selectable
        onSelectEvent={event => console.log(event)}
        defaultDate={this.props.defaultDate}
        onNavigate={this.onNavigate}
        events={this.props.events}
        components={{ toolbar: CalendarToolbar }}
        views={['month']}
        onSelectSlot={this.props.onSelectSlot}
        eventPropGetter={this.setEventProps}
      />
    );
  }
}


// Convert an object of jobs and oneTimeExpenses (as they are received from the
// '/admin/events' api route) into a list of React Big Calendar events.
function createBigCalendarEvents(events) {
  let result = [];

  // Convert each job into a React Big Calendar event
  events.jobs.forEach(job => {
    let bcEvent = {
      eventType: 'job',
      id: job.id,
      title: job.client,
      start: datestringToDate(job.start_date),
      end: datestringToDate(job.end_date),
      allDay: true,
    }

    // Add all the attributes from the job to the bcEvent
    for (var attrname in job) { bcEvent[attrname] = job[attrname]; }
    result.push(bcEvent);
  });

  // Convert each oneTimeExpense into a React Big Calendar event
  events.expenses.forEach(expense => {
    let bcEvent = {
      eventType: 'oneTimeExpense',
      id: expense.id,
      title: expense.merchant,
      start: datestringToDate(expense.date),
      end: datestringToDate(expense.date),
      allDay: true,
    }
    // Add all the attributes from the job to the bcEvent
    for (var attrname in expense) { bcEvent[attrname] = expense[attrname]; }
    result.push(bcEvent);
  });

  return result;
}


Calendar.propTypes = {
  onSelectSlot: PropTypes.func.isRequired,
  events: PropTypes.arrayOf(PropTypes.object).isRequired,
  defaultDate: PropTypes.instanceOf(Date).isRequired,
};

export default Calendar;
