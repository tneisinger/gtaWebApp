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
    const [startDate, endDate] = this.getDateRange();
    axios.get(`${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/events`, {
      params: {
        startDate,
        endDate,
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
      className: getClassNamesForEvent(event),
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
        onSelectEvent={this.props.onSelectEvent}
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
    result.push( makeBigCalendarJobEvent(job) );
  });

  // Convert each oneTimeExpense into a React Big Calendar event
  events.expenses.forEach(expense => {
    result.push( makeBigCalendarExpenseEvent(expense) );
  });

  return result;
}

export function makeBigCalendarJobEvent(job) {
  let jobEvent = {
    eventType: 'job',
    id: job.id,
    title: job.client,
    start: datestringToDate(job.startDate),
    end: datestringToDate(job.endDate),
    allDay: true,
  }

  // Add all the attributes from the job to the jobEvent
  for (var attrname in job) { jobEvent[attrname] = job[attrname]; }

  return jobEvent;
}

export function makeBigCalendarExpenseEvent(expense) {
  let expenseEvent = {
    eventType: 'oneTimeExpense',
    id: expense.id,
    title: expense.merchant,
    start: datestringToDate(expense.date),
    end: datestringToDate(expense.date),
    allDay: true,
  }

  // Add all the attributes from the expense to the expenseEvent
  for (var attrname in expense) { expenseEvent[attrname] = expense[attrname]; }

  return expenseEvent;
}

// Given a Big Calendar event, return a string of space separated css class
// names that help in styling the events appropriately.
function getClassNamesForEvent(event) {
  let classNames = [];
  if (event.eventType === 'oneTimeExpense') {
    classNames.push('expense-event');
    classNames.push('expense-' + event.id);
  } else if (event.eventType === 'job') {
    classNames.push('job-event');
    classNames.push('workedby-' + event.workedBy.toLowerCase());
    classNames.push('job-' + event.id);
    if (!event.has_paid && event.end < new Date()) {
      classNames.push('has-not-paid');
    }
  }
  return classNames.join(' ');
}


// Define an exception for when an unkown event type is discovered
export const UnknownEventTypeException = message => {
  this.message = message;
  this.name = 'UnknownEventTypeException';
};


Calendar.propTypes = {
  onSelectEvent: PropTypes.func.isRequired,
  onSelectSlot: PropTypes.func.isRequired,
  events: PropTypes.arrayOf(PropTypes.object).isRequired,
  defaultDate: PropTypes.instanceOf(Date).isRequired,
};

export default Calendar;
