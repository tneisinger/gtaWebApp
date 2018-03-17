import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';

import Home from './components/Home';
import Calendar from './components/Calendar';
import Budget from './components/Budget';
import Expenses from './components/Expenses';
import NavBar from './components/NavBar';
import Form from './components/Form';

class App extends Component {

  constructor() {
    super();
    this.state = {
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
    this.addUser = this.addUser.bind(this);
    this.handleChange = this.handleChange.bind(this);
  };

  componentDidMount() {
    this.getUsers();
  };

  getUsers() {
    axios.get(`${process.env.REACT_APP_USERS_SERVICE_URL}/admin/users`)
    .then((res) => {
      this.setState({ users: res.data.data.users });
    })
    .catch((err) => { console.log(err); });
  };

  addUser(event) {
    event.preventDefault();
    const data = {
      username: this.state.username,
      email: this.state.email
    };
    axios.post(`${process.env.REACT_APP_USERS_SERVICE_URL}admin/users`, data)
    .then((res) => {
      this.getUsers();
      this.setState({ username: '', email: '' });
    })
    .catch((err) => { console.log(err); });
  }

  handleChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState({
      formData: obj
    });
  };

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
                <Route exact path='/calendar' component={Calendar}/>
                <Route exact path='/budget' component={Budget}/>
                <Route exact path='/expenses' component={Expenses}/>
                <Route exact path='/register' render={() => (
                  <Form
                    formType={'Register'}
                    formData={this.state.formData}
                    handleUserFormSubmit={this.addUser}
                    handleFormChange={this.handleChange}
                  />
                )} />
                <Route exact path='/login' render={() => (
                  <Form
                    formType={'login'}
                    formData={this.state.formData}
                    handleFormChange={this.handleChange}
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
