import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import BigCalendar from 'react-big-calendar';
import '../node_modules/react-big-calendar/lib/css/react-big-calendar.css';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';
import { Button } from 'react-bootstrap';

import Home from './components/Home';
import CalendarToolbar from './components/CalendarToolbar.jsx';
import './css/calendar.css';
import Form from './components/Form';
import { emptyJobFormData, emptyOneTimeExpenseFormData, emptyLoginFormData,
         formTypes, formData }
from './components/Form';
import FormModal from './components/FormModal';
import ChoiceModal from './components/ChoiceModal.jsx';
import NavBar from './components/NavBar';
import { copy } from './utils';


// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      currentCalendarDate: new Date(),
      calendarEvents: [],
      formData: formData,
      showChoiceModal: false,
      showFormModal: false,
      formType: formTypes[0],
      formModalHeading: '',
    };

    // Bind `this` to all the methods named below.  This must be done because
    // these methods get passed into other components, so in order for the
    // `this` keyword to mean this App component instance, we must bind `this`
    // to the method.
    this.bindScopes([
      'getEvents',
      'onNavigate',
      'onCalendarDatesSelect',
      'showJobFormModal',
      'showOneTimeExpenseFormModal',
      'onFormChange',
      'onFormSubmit',
      'onAuthBtnClick',
      'closeFormModal',
    ]);
  };

  bindScopes(keys) {
    for (let key of keys) {
      this[key] = this[key].bind(this);
    }
  }

  componentDidMount() {
  };

  onAuthBtnClick() {
    // open the form modal to show the login form
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formType: formTypes[2],
      formModalHeading: 'Login',
      formData: formData,
    });
  }

  onNavigate(date, view) {
    console.log('#### onNavigate');
  }

  closeFormModal() {
    // If the current formType is the login form...
    if (this.state.formType === formTypes[2]) {

      // reset the login form to protect the user's info
      const updatedFormData = this.state.formData;
      updatedFormData[formTypes[2]] = copy(emptyLoginFormData);

      // reset the login form and hide the form modal
      this.setState({
        showFormModal: false,
        formData: updatedFormData,
      });

    // If any other form type, just hide the modal
    } else {
      this.setState({ showFormModal: false });
    }
  }

  onCalendarDatesSelect(slotInfo) {
    let start_date = moment(slotInfo.start).format('YYYY-MM-DD');
    let end_date = moment(slotInfo.end).format('YYYY-MM-DD');

    // prepare the forms
    const formData = this.state.formData;
    formData[formTypes[0]].start_date = start_date;
    formData[formTypes[0]].end_date = end_date;
    formData[formTypes[1]].date = start_date;

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

  showJobFormModal() {
    // Hide the choice modal (if it is shown) and show the job form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formType: formTypes[0],
      formModalHeading: 'Create a new Job',
    });
  }

  showOneTimeExpenseFormModal() {
    // Hide the choice modal (if shown) and show the oneTimeExpense form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formModalHeading: 'Create a new Expense',
      formType: formTypes[1],
    });
  }

  onFormChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const newFormData = this.state.formData;
    newFormData[this.state.formType][target.name] = value;
    this.setState({ formData: newFormData });
  }

  onFormSubmit(event) {
    // If event passed in, prevent default form behavior
    if (event !== undefined) event.preventDefault();

    // Close the form modal
    this.closeFormModal();
  }

  getDateRange(date) {
    date = date || this.state.currentCalendarDate;
    let date_range;
    if (this.props.location.pathname === '/calendar') {
      date_range = this.getCalendarDateRange(date);
    }
    return date_range;
  }

  getCalendarDateRange(date) {
    date = date || this.state.currentCalendarDate;
    const date_range = {
      start_date: moment(dates.firstVisibleDay(date)).format('YYYY-MM-DD'),
      end_date: moment(dates.lastVisibleDay(date)).format('YYYY-MM-DD')
    }
    return date_range;
  }

  getEvents() {
    console.log('###### ran foreign getEvents');
    let date_range = this.getDateRange();
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
      <div>
        <NavBar
          onAuthBtnClick={this.onAuthBtnClick}
        />
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <br/>
              <Switch>
                <Route exact path='/' component={Home}/>
                <Route exact path='/calendar' render={()=>
                    <BigCalendar
                      defaultDate={this.state.currentCalendarDate}
                      onNavigate={this.onNavigate}
                      events={this.state.calendarEvents}
                      startAccessor={'start'}
                      endAccessor={'end'}
                      components={{ toolbar: CalendarToolbar }}
                      selectable={true}
                      onSelectSlot={this.onCalendarDatesSelect}
                    />
                  }
                />
                <Route exact path='/budget' render={() =>
                  <p>This is the budget page</p>
                }/>
                <Route exact path='/expenses' render={() =>
                  <p>This is the expenses page</p>
                }/>
              </Switch>

              <ChoiceModal
                show={this.state.showChoiceModal}
                onHide={() => this.setState({ showChoiceModal: false })}
                title='Select Event Type'
              >
                <Button bsStyle="primary" onClick={this.showJobFormModal}>
                  New Job
                </Button>
                <Button
                  bsStyle="danger"
                  onClick={this.showOneTimeExpenseFormModal}
                >
                  New Expense
                </Button>
              </ChoiceModal>

              <FormModal
                heading={this.state.formModalHeading}
                show={this.state.showFormModal}
                handleClose={this.closeFormModal}
              >
                <Form
                  formType={this.state.formType}
                  formData={this.state.formData}
                  onFormChange={this.onFormChange}
                  onFormSubmit={this.onFormSubmit}
                />
              </FormModal>

            </div>
          </div>
        </div>
      </div>
    )
  };

};

export default App;
