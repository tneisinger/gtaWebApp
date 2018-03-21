import React from 'react';
import BigCalendar from 'react-big-calendar';
import moment from 'moment';
import '../../node_modules/react-big-calendar/lib/css/react-big-calendar.css';

import EventFormModal from './EventFormModal';
import EventForm from './EventForm';
import { emptyJobFormData, emptyOneTimeExpenseFormData, formTypes, formData }
from './EventForm';
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

    this.state = {
      events: [],
      showChoiceModal: false,
      showFormModal: false,
      formType: formTypes[0],
      formModalHeading: 'Create a New Job',
      formData: formData,
    }

    this.bindScopes([
      'onNavigate',
      'handleFormSubmit',
      'handleFormChange',
      'showJobFormModal',
      'showOneTimeExpenseFormModal',
      'onSelectDates',
    ]);
  }

  componentDidMount() {
    this.props.getEvents();
  };

  bindScopes(keys) {
    for (let key of keys) {
      this[key] = this[key].bind(this);
    }
  }

  onNavigate(date, view) {
    console.log('#### onNavigate');
  }

  showJobFormModal() {
    // Hide the choice modal and show the job form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formType: formTypes[0],
      formModalHeading: 'Create a new Job',
    });
  }

  showOneTimeExpenseFormModal() {
    // Hide the choice modal and show the one time expense form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formModalHeading: 'Create a new Expense',
      formType: formTypes[1],
    });
  }

  handleFormChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const newFormData = this.state.formData;
    newFormData[this.state.formType][target.name] = value;
    this.setState({ formData: newFormData });
  }

  handleFormSubmit(event) {
    if (event !== undefined) event.preventDefault();

    // Close the form modal
    this.setState({ showFormModal: false });
  }

  onSelectDates(slotInfo) {
    let start_date = moment(slotInfo.start).format('YYYY-MM-DD');
    let end_date = moment(slotInfo.end).format('YYYY-MM-DD');

    // prepare the forms
    const formData = this.state.formData;
    formData.jobForm = emptyJobFormData;
    formData.jobForm.start_date = start_date;
    formData.jobForm.end_date = end_date;
    formData.oneTimeExpenseForm = emptyOneTimeExpenseFormData;
    formData.oneTimeExpenseForm.date = start_date;

    // If the user selects multiple days, just open the job form modal.
    // one time expenses cannot take place over multiple days.
    if (start_date !== end_date) {

      // Open the job form modal.
      this.setState({
        showChoiceModal: false,
        showFormModal: true,
        formType: formTypes[0],
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
            defaultDate={this.props.currentDate}
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
          handleClose={() => this.setState({ showChoiceModal: false })}
          heading='Select Event Type'
          leftButtonText='New Job'
          rightButtonText='New Expense'
          handleLeftButtonClick={this.showJobFormModal}
          handleRightButtonClick={this.showOneTimeExpenseFormModal}
        />

        <EventFormModal
          heading={this.state.formModalHeading}
          show={this.state.showFormModal}
          handleClose={() => this.setState({ showFormModal: false })}
          handleFormSubmit={this.handleFormSubmit}
        >
          <EventForm
            formType={this.state.formType}
            formData={this.state.formData}
            handleFormChange={this.handleFormChange}
          />
        </EventFormModal>

      </div>
    );
  }

}

export default Calendar;
