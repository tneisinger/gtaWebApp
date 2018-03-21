import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import BigCalendar from 'react-big-calendar';
import '../node_modules/react-big-calendar/lib/css/react-big-calendar.css';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';

import Home from './components/Home';
import CalendarToolbar from './components/CalendarToolbar.jsx';
import './css/calendar.css';
import EventForm from './components/EventForm';
import { emptyJobFormData, emptyOneTimeExpenseFormData, formTypes, formData }
from './components/EventForm';
import FormModal from './components/FormModal';
import ChoiceModal from './components/ChoiceModal.jsx';
import NavBar from './components/NavBar';
import Form from './components/Form';


// select moment as the localizer for BigCalendar
BigCalendar.momentLocalizer(moment);

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      currentCalendarDate: new Date(),
      calendarEvents: [],
      username: '',
      email: '',
      title: 'Gladtime Audio',
      authFormData: {
        username: '',
        email: '',
        password: ''
      },
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
      'handleUserFormSubmit',
      'handleAuthFormChange',
      'getEvents',
      'onNavigate',
      'onCalendarDatesSelect',
      'showJobFormModal',
      'showOneTimeExpenseFormModal',
      'handleFormChange',
      'handleFormSubmit',
    ]);
  };

  bindScopes(keys) {
    for (let key of keys) {
      this[key] = this[key].bind(this);
    }
  }

  componentDidMount() {
  };

  onNavigate(date, view) {
    console.log('#### onNavigate');
  }

  onCalendarDatesSelect(slotInfo) {
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

  handleFormChange(event) {
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const newFormData = this.state.formData;
    newFormData[this.state.formType][target.name] = value;
    this.setState({ formData: newFormData });
  }

  handleFormSubmit(event) {
    // If event passed in, prevent default form behavior
    if (event !== undefined) event.preventDefault();

    // Close the form modal
    this.setState({ showFormModal: false });
  }

  handleUserFormSubmit(event) {
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data = {
      email: this.state.authFormData.email,
      password: this.state.authFormData.password,
    };
    if (formType === 'register') {
      data.username = this.state.authFormData.username;
    }
    const url = `${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/${formType}`
    axios.post(url, data)
    .then((res) => {
      // Clear the form inputs
      this.setState({
        authFormData: { username: '', email: '', password: '' }
      });

      // save the user's auth token in their browser's local storage
      window.localStorage.setItem('authToken', res.data.auth_token);
    })
    .catch((err) => { console.log(err); });
  };

  handleAuthFormChange(event) {
    const obj = this.state.authFormData;
    obj[event.target.name] = event.target.value;
    this.setState({ authFormData: obj });
  };


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
          title={this.state.title}
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
                <Route exact path='/register' render={() => (
                  <Form
                    formType={'Register'}
                    formData={this.state.authFormData}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    handleFormChange={this.handleAuthFormChange}
                  />
                )} />
                <Route exact path='/login' render={() => (
                  <Form
                    formType={'login'}
                    formData={this.state.authFormData}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    handleFormChange={this.handleAuthFormChange}
                  />
                )} />
              </Switch>

              <ChoiceModal
                show={this.state.showChoiceModal}
                handleClose={() => this.setState({ showChoiceModal: false })}
                heading='Select Event Type'
                leftButtonText='New Job'
                rightButtonText='New Expense'
                handleLeftButtonClick={this.showJobFormModal}
                handleRightButtonClick={this.showOneTimeExpenseFormModal}
              />

              <FormModal
                heading={this.state.formModalHeading}
                show={this.state.showFormModal}
                handleClose={() => this.setState({ showFormModal: false })}
              >
                <EventForm
                  formType={this.state.formType}
                  formData={this.state.formData}
                  onFormChange={this.handleFormChange}
                  onFormSubmit={this.handleFormSubmit}
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
