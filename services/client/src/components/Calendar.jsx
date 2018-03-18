import React from 'react';
import BigCalendar from 'react-big-calendar';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';
import axios from 'axios';
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css';
import '../css/calendar.css';

// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);

const CustomToolbar = (toolbar) => {
  const goToBack = () => {
    toolbar.date.setMonth(toolbar.date.getMonth() - 1);
    toolbar.onNavigate('prev');
  };

  const goToNext = () => {
    toolbar.date.setMonth(toolbar.date.getMonth() + 1);
    toolbar.onNavigate('next');
  };

  const goToCurrent = () => {
    const now = new Date();
    toolbar.date.setMonth(now.getMonth());
    toolbar.date.setYear(now.getFullYear());
    toolbar.onNavigate('current');
  };

  const label = () => {
    const date = moment(toolbar.date);
    return (
      <span>
        <b>{date.format('MMMM')}</b>
        <span> {date.format('YYYY')}</span>
      </span>
    );
  };

  return (
    <div className='rbc-toolbar'>
      <span className='rbc-btn-group'>
        <button type='button' onClick={goToBack}>prev</button>
        <button type='button' onClick={goToNext}>next</button>
      </span>
      <span className='rbc-toolbar-label'>{label()}</span>
      <span className='rbc-btn-group'>
        <button type='button' onClick={goToCurrent}>today</button>
      </span>
    </div >
  );
}

class Calendar extends React.Component {

  constructor() {
    super();
    this.state = {
      current_date: new Date(),
      events: []
    }

    this.bindScopes([
      'onNavigate'
    ]);
  }

  componentDidMount() {
    this.getEvents();
  };

  bindScopes(keys) {
    for (let key of keys) {
      this[key] = this[key].bind(this);
    }
  }

  onNavigate(date, view) {
    console.log('#### onNavigate');
    this.getVisibleDateRange(date);
  }

  getVisibleDateRange(date = this.state.current_date) {
    let result = {
      start_date: moment(dates.firstVisibleDay(date)).format('YYYY-MM-DD'),
      end_date: moment(dates.lastVisibleDay(date)).format('YYYY-MM-DD')
    }
    return result;
  }

  getEvents() {
    let date_range = this.getVisibleDateRange();
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
      alert('You are not authorized!');
      console.log(err.response.data);
      console.log(err.response.status);
    });
  }

  render() {
    return (
      <div className='calendar-container'>
        <BigCalendar
          defaultDate={this.state.current_date}
          onNavigate={this.onNavigate}
          events={this.state.events}
          startAccessor={'start'}
          endAccessor={'end'}
          components={{
            toolbar: CustomToolbar
          }}
        />
      </div>
    );
  }

}

export default Calendar;
