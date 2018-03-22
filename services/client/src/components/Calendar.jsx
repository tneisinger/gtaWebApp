import React, { Component } from 'react';
import axios from 'axios';
import BigCalendar from 'react-big-calendar';
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';
import { Button } from 'react-bootstrap';

import CalendarToolbar from './CalendarToolbar.jsx';
import '../css/calendar.css';
import { formTypes, defaultFormData } from './Form';
import ChoiceModal from './ChoiceModal.jsx';
import NavBar from './NavBar';


// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);


class Calendar extends Component {

  constructor(props) {
    super(props);

    this.bindScopes([
      'onNavigate',
    ]);
  }

  bindScopes(keys) {
    for (let key of keys) {
      this[key] = this[key].bind(this);
    }
  }

  componentDidMount() {
    const [start_date, end_date] = this.getDateRange();
    this.getEvents(start_date, end_date);
  }

  getEvents(start_date, end_date) {
    let date_range = {
      start_date: start_date,
      end_date: end_date
    };
    axios.get(`${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/events`, {
      params: date_range,
      headers: {
        'Authorization': `Bearer ${window.localStorage.getItem('authToken')}`
      }
    })
    .then((res) => {
      console.log(res);
    })
    .catch((err) => {
      console.log(err);
      //alert('You are not authorized!');
      //console.log(err.response.data);
      //console.log(err.response.status);
    });
  }

  getDateRange(date) {
    date = date || this.props.currentDate;
    const start_date = moment(dates.firstVisibleDay(date))
                         .format('YYYY-MM-DD');
    const end_date = moment(dates.lastVisibleDay(date)).format('YYYY-MM-DD');
    return [start_date, end_date];
  }

  onNavigate(date, view) {
    const [start_date, end_date] = this.getDateRange(date);
    console.log('start_date:', start_date);
    console.log('end_date:', end_date);
  }

  render() {
    return (
      <BigCalendar
        date={this.props.currentDate}
        onNavigate={this.onNavigate}
        events={this.props.events}
        components={{ toolbar: CalendarToolbar }}
        selectable={true}
        views={['month']}
        onSelectSlot={this.props.onSelectSlot}
      />
    );
  }
}

export default Calendar;
