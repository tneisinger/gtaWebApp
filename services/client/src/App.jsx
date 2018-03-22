import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import moment from 'moment';
import { Button } from 'react-bootstrap';

import Home from './components/Home';
import Calendar from './components/Calendar';
import Form from './components/Form';
import { formTypes, defaultFormData } from './components/Form';
import FormModal from './components/FormModal';
import ChoiceModal from './components/ChoiceModal.jsx';
import NavBar from './components/NavBar';
import { copy, deepcopy } from './utils';


class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      currentCalendarDate: new Date(),
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
    ]);
  };

  bindScopes(keys) {
    for (let key of keys) {
      this[key] = this[key].bind(this);
    }
  }

  onAuthBtnClick() {
    // open the form modal to show the login form
    this.setState({
      showChoiceModal: false,
      showFormModal: true,
      formType: formTypes.login,
      formModalHeading: 'Login',
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

  onCalendarDatesSelect(slotInfo) {
    let start_date = moment(slotInfo.start).format('YYYY-MM-DD');
    let end_date = moment(slotInfo.end).format('YYYY-MM-DD');

    // prepare the forms
    const formData = this.state.formData;
    formData[formTypes.job].start_date = start_date;
    formData[formTypes.job].end_date = end_date;
    formData[formTypes.oneTimeExpense].date = start_date;

    // If the user selects multiple days, just open the job form modal.
    // one time expenses cannot take place over multiple days.
    if (start_date !== end_date) {

      // Open the job form modal.
      this.setState({
        showChoiceModal: false,
        showFormModal: true,
        formType: formTypes.job,
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
      formType: formTypes.job,
      formModalHeading: 'Create a new Job',
    });
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

    // Close the form modal and reset the current form to its default
    this.setState({
      showFormModal: false,
      formData: this.getResetFormData(),
    });
  }

  getResetFormData(formType) {
    formType = formType || this.state.formType;

    if (formType === 'all') {
      return copy(defaultFormData);
    }

    const updatedFormData = this.state.formData;
    updatedFormData[formType] = copy(defaultFormData[formType]);
    return updatedFormData;
  }

  setCalendarEvents(events) {
    this.setState({ calendarEvents: events });
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
                    <Calendar
                      currentDate={this.state.currentCalendarDate}
                      events={this.state.calendarEvents}
                      setEvents={this.setCalendarEvents}
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
