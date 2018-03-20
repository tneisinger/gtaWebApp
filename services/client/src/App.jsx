import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';
import dates from 'react-big-calendar/lib/utils/dates';
import moment from 'moment';

import Home from './components/Home';
import Calendar from './components/Calendar';
import Budget from './components/Budget';
import Expenses from './components/Expenses';
import NavBar from './components/NavBar';
import Form from './components/Form';

class App extends Component {

  constructor(props) {
    super(props);
    this.state = {
      currentCalendarDate: new Date(),
      users: [],
      username: '',
      email: '',
      title: 'Gladtime Audio',
      formData: {
        username: '',
        email: '',
        password: ''
      }
    };
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
    this.getEvents = this.getEvents.bind(this);
  };

  componentDidMount() {
    this.getUsers();
  };

  getUsers() {
    axios.get(`${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/users`)
    .then((res) => {
      this.setState({ users: res.data.data.users });
    })
    .catch((err) => { console.log(err); });
  };

  handleUserFormSubmit(event) {
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data = {
      email: this.state.formData.email,
      password: this.state.formData.password,
    };
    if (formType === 'register') {
      data.username = this.state.formData.username;
    }
    const url = `${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/${formType}`
    axios.post(url, data)
    .then((res) => {
      // Clear the form inputs
      this.setState({
        formData: { username: '', email: '', password: '' }
      });

      // save the user's auth token in their browser's local storage
      window.localStorage.setItem('authToken', res.data.auth_token);
    })
    .catch((err) => { console.log(err); });
  };

  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState({ formData: obj });
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
                  <Calendar
                    currentDate={this.state.currentCalendarDate}
                    getEvents={this.getEvents}
                  />}/>
                <Route exact path='/budget' component={Budget}/>
                <Route exact path='/expenses' component={Expenses}/>
                <Route exact path='/register' render={() => (
                  <Form
                    formType={'Register'}
                    formData={this.state.formData}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    handleFormChange={this.handleFormChange}
                  />
                )} />
                <Route exact path='/login' render={() => (
                  <Form
                    formType={'login'}
                    formData={this.state.formData}
                    handleUserFormSubmit={this.handleUserFormSubmit}
                    handleFormChange={this.handleFormChange}
                  />
                )} />
              </Switch>
            </div>
          </div>
        </div>
      </div>
    )
  };

};

export default App;
