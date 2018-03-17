import React from 'react'
import BigCalendar from 'react-big-calendar'
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment'
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css'
import '../css/calendar.css'

// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);

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
    this.getDateRange();
  };


  bindScopes(keys) {
    for (let key of keys) {
      this[key] = this[key].bind(this);
    }
  }

  onNavigate(date, view) {
    console.log('#### onNavigate');
    this.getDateRange(date);
  }

  getDateRange(date = this.state.current_date) {
    let start_date = moment(dates.firstVisibleDay(date)).format('YYYY-MM-DD');
    let end_date = moment(dates.lastVisibleDay(date)).format('YYYY-MM-DD');
    console.log('start_date =', start_date)
    console.log('end_date =', end_date)
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
        />
      </div>
    );
  }

}

export default Calendar;
