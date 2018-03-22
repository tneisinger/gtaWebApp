import React, { Component } from 'react';
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
  }

  getDateRange(date) {
    date = date || this.props.currentDate;
    const date_range = {
      start_date: moment(dates.firstVisibleDay(date)).format('YYYY-MM-DD'),
      end_date: moment(dates.lastVisibleDay(date)).format('YYYY-MM-DD')
    }
    return date_range;
  }

  render() {
    return (
      <BigCalendar
        date={this.props.currentDate}
        onNavigate={this.props.onNavigate}
        events={this.props.events}
        components={{ toolbar: CalendarToolbar }}
        selectable={true}
        onSelectSlot={this.props.onSelectSlot}
      />
    );
  }
}

export default Calendar;
