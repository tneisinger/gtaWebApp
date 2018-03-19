import React from 'react';
import BigCalendar from 'react-big-calendar';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';
import axios from 'axios';
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css';

import EventFormModal from './EventFormModal';
import ChoiceModal from './ChoiceModal.jsx';
import '../css/calendar.css';

// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);

// Create a custom toolbar for the calendar
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

  constructor(props) {
    super(props);

    this.emptyJobForm = {
      client: '',
      description: '',
      amount_paid: '',
      paid_to: 'Gladtime Audio',
      worked_by: 'Meghan',
      confirmation: 'Confirmed',
      has_paid: false,
      start_date: '',
      end_date: '',
    }

    this.emptyOneTimeExpenseForm = {
      merchant: '',
      description: '',
      amount_spent: '',
      date: '',
      paid_by: 'Gladtime Audio',
      tax_deductible: false,
      category: 'Business Equipment',
    }

    this.state = {
      current_date: new Date(),
      events: [],
      showChoiceModal: false,
      showFormModal: false,
      formType: 'jobForm',
      formModalHeading: 'Create a New Job',
      formData: {
        jobForm: this.emptyJobForm,
        oneTimeExpenseForm: this.emptyOneTimeExpenseForm,
      },
    }

    this.bindScopes([
      'onNavigate',
      'showFormModal',
      'closeFormModal',
      'showChoiceModal',
      'closeChoiceModal',
      'handleFormSubmit',
      'handleFormChange',
      'showJobFormModal',
      'showOneTimeExpenseFormModal',
      'onSelectDates',
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

  showChoiceModal() {
    this.setState({ showChoiceModal: true });
  }

  closeChoiceModal() {
    this.setState({ showChoiceModal: false });
  }

  showFormModal() {
    this.setState({ showFormModal: true });
  }

  closeFormModal() {
    this.setState({ showFormModal: false });
  }

  showJobFormModal() {

    // Hide the choice modal and show the job form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formType: 'jobForm',
      formModalHeading: 'Create a new Job',
    });
  }

  showOneTimeExpenseFormModal() {
    // Hide the choice modal and show the one time expense form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formModalHeading: 'Create a new Expense',
      formType: 'oneTimeExpenseForm',
    });
  }

  handleFormChange(event, formType) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const obj = this.state.formData;
    obj[this.state.formType][target.name] = value;
    this.setState({ formData: obj });
  }

  handleFormSubmit(event) {
    if (event !== undefined) event.preventDefault();
    this.closeFormModal();
  }

  onSelectDates(slotInfo) {
    let start_date = moment(slotInfo.start).format('YYYY-MM-DD');
    let end_date = moment(slotInfo.end).format('YYYY-MM-DD');

    // prepare the forms
    const formData = this.state.formData;
    formData.jobForm = this.emptyJobForm;
    formData.jobForm.start_date = start_date;
    formData.jobForm.end_date = end_date;
    formData.oneTimeExpenseForm = this.emptyOneTimeExpenseForm;
    formData.oneTimeExpenseForm.date = start_date;

    // If the user selects multiple days, just open the job form modal.
    // one time expenses cannot take place over multiple days.
    if (start_date !== end_date) {

      // Open the job form modal.
      this.setState({
        showChoiceModal: false,
        showFormModal: true,
        formType: 'jobForm',
        formModalHeading: 'Create a new Job',
        formData: formData,
      });

    } else {

      // Put the dates in the forms and show the choice modal
      this.setState({
        formData: formData,
        showChoiceModal: true,
      });

    }
  }

  render() {
    return (
      <div>
        <div className='calendar-container'>
          <BigCalendar
            defaultDate={this.state.current_date}
            onNavigate={this.onNavigate}
            events={this.state.events}
            startAccessor={'start'}
            endAccessor={'end'}
            components={{ toolbar: CustomToolbar }}
            selectable={true}
            onSelectSlot={this.onSelectDates}
          />
        </div>

        <ChoiceModal
          show={this.state.showChoiceModal}
          handleClose={this.closeChoiceModal}
          heading='Select Event Type'
          leftButtonText='New Job'
          rightButtonText='New Expense'
          handleLeftButtonClick={this.showJobFormModal}
          handleRightButtonClick={this.showOneTimeExpenseFormModal}
        />

        <EventFormModal
          show={this.state.showFormModal}
          handleClose={this.closeFormModal}
          heading={this.state.formModalHeading}
          formType={this.state.formType}
          formData={this.state.formData}
          handleFormChange={this.handleFormChange}
          handleFormSubmit={this.handleFormSubmit}
        />

      </div>
    );
  }

}

export default Calendar;
