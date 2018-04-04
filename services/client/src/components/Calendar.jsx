import React, { Component } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import BigCalendar from 'react-big-calendar';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css';

import CalendarToolbar from './CalendarToolbar';
import '../css/calendar.css';


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
      // TODO:
    }).catch((err) => {
      // TODO: [err.response.data, err.response.status];
    });
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
        defaultDate={this.props.defaultDate}
        onNavigate={this.onNavigate}
        events={this.props.events}
        components={{ toolbar: CalendarToolbar }}
        selectable={true} // eslint-disable-line react/jsx-boolean-value
        views={['month']}
        onSelectSlot={this.props.onSelectSlot}
      />
    );
  }
}

Calendar.propTypes = {
  onSelectSlot: PropTypes.func.isRequired,
  events: PropTypes.arrayOf(PropTypes.object).isRequired,
  defaultDate: PropTypes.instanceOf(Date).isRequired,
};

export default Calendar;
