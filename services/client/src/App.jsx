import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import moment from 'moment';
import { Button } from 'react-bootstrap';

import PrivateRoute from './components/PrivateRoute';
import Home from './components/Home';
import Calendar from './components/Calendar';
import Form, { formTypes, defaultFormData, UnknownFormTypeException }
  from './components/Form';
import FormModal from './components/FormModal';
import ChoiceModal from './components/ChoiceModal';
import NavBar from './components/NavBar';
import { copy, deepcopy, runCallbackAt } from './utils';


class App extends Component {
  constructor(props) {
    super(props);

    // Shorter constant that contains the root url to the flask api service
    this.FLASK_URL_ROOT = process.env.REACT_APP_FLASK_SERVICE_URL;

    this.state = {
      username: '',
      userLoggedIn: null,
      calendarEvents: [],
      formData: deepcopy(defaultFormData),
      showChoiceModal: false,
      showFormModal: false,
      formType: formTypes.login,
      formModalHeading: '',
    };

    // Bind `this` to all the methods named below.  This must be done because
    // these methods get passed into other components, so in order for the
    // `this` keyword to mean this App component instance, we must bind `this`
    // to the method.
    this.bindScopes([
      'setCalendarEvents',
      'onCalendarDatesSelect',
      'showJobFormModal',
      'showOneTimeExpenseFormModal',
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
    console.log('running logout method');
    window.localStorage.clear();
    this.setState({
      userLoggedIn: false,
      username: null,
    });
  }

  setLogoutTimer(minutes, overwriteOldTimer) {
    let logoutTime = window.localStorage.getItem('logoutTime');
    if (!logoutTime || overwriteOldTimer) {
      logoutTime = moment(new Date()).add(minutes, 'm').toDate();
      window.localStorage.setItem('logoutTime', logoutTime);
    }
    runCallbackAt(logoutTime, this.logout);
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

  onCalendarDatesSelect(slotInfo) {
    const startDate = moment(slotInfo.start).format('YYYY-MM-DD');
    const endDate = moment(slotInfo.end).format('YYYY-MM-DD');

    // prepare the forms
    const { formData } = this.state;
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
        this.requestCreateJob();
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

  requestLogin() {
    // We need to refer to 'this' in an axios request, so get a ref to it
    const self = this;

    // Prepare form data
    const data = this.state.formData[formTypes.login];

    // Make the login request
    axios.post(`${this.FLASK_URL_ROOT}/admin/login`, data)
      .then((response) => {

        // If this is a public device, set a timer to logout after 10 minutes
        if (!data.isPrivateDevice) {
          this.setLogoutTimer(10, true);
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
    // Prepare the form data
    const data = this.state.formData[formTypes.job];

    // Get the current authToken
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
          console.log(response);
        })
        .catch(error => {
          console.log(error);
          console.log(error.response);
        })
      ;
    }
  }

  // requestCreateOneTimeExpense() {
  // }

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
    // Hide the choice modal (if it is shown) and show the job form modal
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

    // If any other form type, just hide the modal
    } else {
      this.setState({ showFormModal: false });
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
          this.setState({
            userLoggedIn: true,
            username: response.data.data.username,
          });
        })
        .catch((err) => {
          console.log(err);
          this.setState({
            userLoggedIn: false,
            username: null,
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
