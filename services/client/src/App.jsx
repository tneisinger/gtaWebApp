import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import moment from 'moment';
import { Button } from 'react-bootstrap';

import PrivateRoute from './components/PrivateRoute';
import Home from './components/Home';
import Calendar, { makeBigCalendarJobEvent, makeBigCalendarExpenseEvent,
  UnknownEventTypeException} from './components/Calendar';
import Form, { formTypes, defaultFormData, UnknownFormTypeException }
  from './components/Form';
import FormModal from './components/FormModal';
import ChoiceModal from './components/ChoiceModal';
import NavBar from './components/NavBar';
import { copy, deepcopy, runCallbackAt, fillObjectWith } from './utils';


class App extends Component {
  constructor(props) {
    super(props);

    // Shorter constant that contains the root url to the flask api service
    this.FLASK_URL_ROOT = process.env.REACT_APP_FLASK_SERVICE_URL;

    this.state = {
      username: '',
      userLoggedIn: null,
      calendarEvents: [],
      selectedEvent: null,
      formData: deepcopy(defaultFormData),
      showChoiceModal: false,
      showFormModal: false,
      formType: formTypes.login,
      formModalHeading: '',
    };

    // Bind `this` to all the methods named below.  This must be done because
    // these methods get passed into other components, so in order for the
    // `this` keyword to mean this App component instance, we must bind `this`
    // to each of these methods.
    this.bindScopes([
      'setCalendarEvents',
      'onCalendarDatesSelect',
      'onCalendarEventSelect',
      'showJobFormModal',
      'showOneTimeExpenseFormModal',
      'onDeleteJobBtnClick',
      'onDeleteExpenseBtnClick',
      'onFormChange',
      'onFormSubmit',
      'onAuthBtnClick',
      'closeFormModal',
      'logout',
    ]);
  }

  componentDidMount() {
    this.checkUserStatus();
  }

  logout() {
    window.localStorage.clear();
    this.setState({
      userLoggedIn: false,
      username: '',
    });
  }

  // Set a timer to automatically logout at the given logoutTime
  setLogoutTimer(logoutTime) {
    const timeFromNow = logoutTime.getTime() - (new Date()).getTime();
    // If the logout time is less than an hour away, set the logout timer
    if (timeFromNow < 3600000) {
      runCallbackAt(logoutTime, this.logout);
    }
  }

  onAuthBtnClick() {
    // If the user is currently logged in...
    if (this.state.userLoggedIn) {
      this.logout();

    // If the user isn't currently logged in
    } else {
      // open the form modal to show the login form
      this.setState({
        showChoiceModal: false,
        showFormModal: true,
        formType: formTypes.login,
        formModalHeading: 'Login',
      });
    }
  }

  onDeleteJobBtnClick() {
    console.log('Clicked "Delete This Job" button');
  }

  onDeleteExpenseBtnClick() {
    console.log('Clicked "Delete This Expense" button');
  }

  onCalendarDatesSelect(slotInfo) {
    const startDate = moment(slotInfo.start).format('YYYY-MM-DD');
    const endDate = moment(slotInfo.end).format('YYYY-MM-DD');

    // Reset the form inputs to their default values
    const formData = deepcopy(defaultFormData);

    // Enter the selected dates into the forms
    formData[formTypes.job].startDate = startDate;
    formData[formTypes.job].endDate = endDate;
    formData[formTypes.oneTimeExpense].date = startDate;

    // If the user selects multiple days, just open the job form modal.
    // one time expenses cannot take place over multiple days.
    if (startDate !== endDate) {
      // Open the job form modal.
      this.setState({
        showChoiceModal: false,
        showFormModal: true,
        formType: formTypes.job,
        formModalHeading: 'Create a new Job',
        selectedEvent: null,
        formData,
      });
    } else {
      // Put the dates in the forms and show the choice modal
      this.setState({
        formData,
        showChoiceModal: true,
      });
    }
  }

  onCalendarEventSelect(event) {
    let formType;
    let formModalHeading;
    switch (event.eventType) {
      case 'job':
        formType = formTypes.job;
        formModalHeading = 'Edit Job';
        break;
      case 'oneTimeExpense':
        formType = formTypes.oneTimeExpense;
        formModalHeading = 'Edit Expense';
        break;
      default:
        throw new UnknownEventTypeException('Unknown calendar event type');
    }

    // Update the form data before showing the form modal
    const newFormData = this.state.formData;
    newFormData[formType] = fillObjectWith(newFormData[formType], event);

    // Set the new form data and show the job form
    this.setState({
      formData: newFormData,
      showFormModal: true,
      formType: formType,
      formModalHeading: formModalHeading,
      selectedEvent: event,
    });
  }

  onFormChange(event) {
    const { target } = event;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const newFormData = this.state.formData;
    newFormData[this.state.formType][target.name] = value;
    this.setState({ formData: newFormData });
  }

  onFormSubmit(event) {
    // If event passed in, prevent default form behavior
    if (event !== undefined) event.preventDefault();

    // Based on the current formType, perform a request
    switch (this.state.formType) {
      case formTypes.login:
        this.requestLogin();
        break;
      case formTypes.job:
        if (this.state.selectedEvent) {
          this.requestUpdateJob();
        } else {
          this.requestCreateJob();
        }
        break;
      case formTypes.oneTimeExpense:
        this.requestCreateOneTimeExpense();
        break;
      default:
        throw new UnknownFormTypeException('Unknown form type in App state');
    }

    // Close the form modal and reset the current form to its default
    this.setState({
      showFormModal: false,
      formData: this.getResetFormData(),
    });
  }

  getResetFormData(inputFormType) {
    const formType = inputFormType || this.state.formType;

    if (formType === 'all') {
      return deepcopy(defaultFormData);
    }

    const updatedFormData = this.state.formData;
    updatedFormData[formType] = copy(defaultFormData[formType]);
    return updatedFormData;
  }

  setCalendarEvents(events) {
    this.setState({ calendarEvents: events });
  }

  addCalendarJobEvent(job) {
    const jobEvent = makeBigCalendarJobEvent(job);
    this.setState({
      calendarEvents: this.state.calendarEvents.concat([jobEvent]),
    });
  }

  updateCalendarJobEvent(job) {
    const newJobEvent = makeBigCalendarJobEvent(job);
    const oldCalendarEvents = this.state.calendarEvents;
    const newCalendarEvents = [];

    oldCalendarEvents.forEach(event => {
      if (event.eventType === 'job' && event.id === newJobEvent.id) {
        newCalendarEvents.push(newJobEvent)
      } else {
        newCalendarEvents.push(event)
      }
    });

    this.setState({
      calendarEvents: newCalendarEvents,
    });
  }

  addCalendarExpenseEvent(expense) {
    const expenseEvent = makeBigCalendarExpenseEvent(expense);
    this.setState({
      calendarEvents: this.state.calendarEvents.concat([expenseEvent]),
    });
  }

  requestLogin() {
    // We need to refer to 'this' (the current App component instance) in an
    // axios callback below. Because the 'this' variable in the axios callbacks
    // will refer to something else, we need to store a reference to the
    // current 'this' in a variable.
    const self = this;

    // Get the form data from the login form
    const data = this.state.formData[formTypes.login];

    // Make the login request
    axios.post(`${this.FLASK_URL_ROOT}/admin/login`, data)
      .then((response) => {

        // If client is not using a private device, set a timer to
        // automatically logout the user when the authToken expires.
        if (!data.isPrivateDevice) {
          const authExpireTime = new Date(response.data.expiration);
          console.log(response);
          this.setLogoutTimer(authExpireTime);
        }

        // Save the authToken and declare the user logged in
        window.localStorage.setItem('authToken', response.data.auth_token);
        self.setState({
          userLoggedIn: true,
          username: response.data.user.username,
        });
      })
      .catch((error) => {
        console.log('There was an error when you tried to log in');
        console.log(error);
      });
  }

  requestCreateJob() {
    // Get the form data from the job form
    const data = this.state.formData[formTypes.job];

    // Try to get the current authToken
    const authToken = window.localStorage.getItem('authToken');

    // If no authToken, redirect to the homepage and, if necessary, change
    // state to reflect that the user is not logged in.
    if (!authToken) {
      this.props.history.push('/');
      if (this.state.username || this.state.userLoggedIn) {
        this.setState({ username: '', userLoggedIn: false });
      }
    } else {
      // Attempt to add the job to the db
      axios.post(`${this.FLASK_URL_ROOT}/admin/jobs`, data, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        }
      })
        .then(response => {
          const newJob = response.data.job;
          this.addCalendarJobEvent(newJob)
        })
        .catch(error => {
          console.log(error);
          if (error.response) {
            console.log(error.response);
          }
        })
      ;
    }
  }

  requestUpdateJob() {
    // Get the form data from the job form
    const data = this.state.formData[formTypes.job];

    // Try to get the current authToken
    const authToken = window.localStorage.getItem('authToken');

    // If no authToken, redirect to the homepage and, if necessary, change
    // state to reflect that the user is not logged in.
    if (!authToken) {
      this.props.history.push('/');
      if (this.state.username || this.state.userLoggedIn) {
        this.setState({ username: '', userLoggedIn: false });
      }
    } else {
      // Get the id of the selected job
      const jobId = this.state.selectedEvent.id
      // Attempt to update the job's database entry
      axios.post(`${this.FLASK_URL_ROOT}/admin/jobs/${jobId}`, data, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        }
      })
        .then(response => {
          const newJob = response.data.job;
          this.updateCalendarJobEvent(newJob)
        })
        .catch(error => {
          console.log(error);
          if (error.response) {
            console.log(error.response);
          }
        })
      ;
    }
  }

  requestCreateOneTimeExpense() {
    // Get the form data from the oneTimeExpense form
    const data = this.state.formData[formTypes.oneTimeExpense];

    // Try to get the current authToken
    const authToken = window.localStorage.getItem('authToken');

    // If no authToken, redirect to the homepage and, if necessary, change
    // state to reflect that the user is not logged in.
    if (!authToken) {
      this.props.history.push('/');
      if (this.state.username || this.state.userLoggedIn) {
        this.setState({ username: '', userLoggedIn: false });
      }
    } else {
      // Attempt to add the expense to the db
      axios.post(`${this.FLASK_URL_ROOT}/admin/one-time-expenses`, data, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        }
      })
        .then(response => {
          const newExpense = response.data.expense;
          this.addCalendarExpenseEvent(newExpense)
        })
        .catch(error => {
          console.log(error);
          if (error.response) {
            console.log(error.response);
          }
        })
      ;
    }
  }

  showOneTimeExpenseFormModal() {
    // Hide the choice modal (if shown) and show the oneTimeExpense form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formModalHeading: 'Create a new Expense',
      formType: formTypes.oneTimeExpense,
    });
  }

  showJobFormModal() {
    // Hide the choice modal (if shown) and show the job form modal
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formType: formTypes.job,
      formModalHeading: 'Create a new Job',
    });
  }

  closeFormModal() {
    // If the current formType is the login form...
    if (this.state.formType === formTypes.login) {
      // reset the login form and hide the form modal
      this.setState({
        showFormModal: false,
        formData: this.getResetFormData(),
      });

    // If any other form type, hide the modal and set
    // this.state.selectedEvent to null
    } else {
      this.setState({
        showFormModal: false,
        selectedEvent: null,
      });
    }
  }

  checkUserStatus() {
    const authToken = window.localStorage.getItem('authToken');
    if (!authToken) {
      // If there is no auth token, declare that the user is not logged in
      this.setState({ username: '', userLoggedIn: false });
    } else {
      axios.get(`${this.FLASK_URL_ROOT}/admin/status`, {
        headers: {
          Authorization: `Bearer ${authToken}`,
        },
      })
        .then((response) => {
          // Set a timer to automatically log out when the authToken expires
          const authExpireTime = new Date(response.data.expiration);
          this.setLogoutTimer(authExpireTime);

          // Declare in app state that the user is logged in
          this.setState({
            userLoggedIn: true,
            username: response.data.user.username,
          });
        })
        .catch((err) => {
          this.setState({
            userLoggedIn: false,
            username: '',
          });
        });
    }
  }

  bindScopes(keys) {
    keys.forEach((key) => {
      this[key] = this[key].bind(this);
    });
  }

  render() {
    return (
      <div>
        <NavBar
          onAuthBtnClick={this.onAuthBtnClick}
          username={this.state.username}
          userLoggedIn={this.state.userLoggedIn}
        />
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <br />
              <Switch>
                <Route exact path="/" component={Home} />
                <PrivateRoute
                  userLoggedIn={this.state.userLoggedIn}
                  path="/calendar"
                  exact
                  component={Calendar}
                  componentProps={{
                    defaultDate: new Date(),
                    events: this.state.calendarEvents,
                    setCalendarEvents: this.setCalendarEvents,
                    onSelectSlot: this.onCalendarDatesSelect,
                    onSelectEvent: this.onCalendarEventSelect,
                  }}
                />
                <Route
                  exact
                  path="/budget"
                  render={() =>
                    <p>This is the budget page</p>
                }
                />
                <Route
                  exact
                  path="/expenses"
                  render={() =>
                    <p>This is the expenses page</p>
                }
                />
              </Switch>

              <ChoiceModal
                show={this.state.showChoiceModal}
                onHide={() => this.setState({ showChoiceModal: false })}
                title="Select Event Type"
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
                formType={this.state.formType}
                onDeleteExpenseBtnClick={this.onDeleteExpenseBtnClick}
                onDeleteJobBtnClick={this.onDeleteJobBtnClick}
                isDeletable={Boolean(this.state.selectedEvent)}
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
    );
  }
}

export default App;
