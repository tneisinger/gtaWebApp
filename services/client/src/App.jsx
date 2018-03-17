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
    this.loginUser = this.loginUser.bind(this);
    this.registerUser = this.registerUser.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
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

  registerUser(event) {
    event.preventDefault();
    const data = {
      username: this.state.formData.username,
      email: this.state.formData.email,
      password: this.state.formData.password
    };
    axios.post(`${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/register`,
               data
    )
    .then((res) => {
      this.setState({
        formData: { username: '', email: '', password: '' }
      });
    })
    .catch((err) => { console.log(err); });
  }

  loginUser(event) {
    event.preventDefault();
    const data = {
      email: this.state.formData.email,
      password: this.state.formData.password
    };
    axios.post(`${process.env.REACT_APP_FLASK_SERVICE_URL}/admin/login`, data)
    .then((res) => {
      this.setState({
        formData: { username: '', email: '', password: '' }
      });
      console.log('Here is the result:');
      console.log(res);
    })
    .catch((err) => { console.log(err); });
  }

  handleFormChange(event) {
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
                    handleUserFormSubmit={this.registerUser}
                    handleFormChange={this.handleFormChange}
                  />
                )} />
                <Route exact path='/login' render={() => (
                  <Form
                    formType={'login'}
                    formData={this.state.formData}
                    handleUserFormSubmit={this.loginUser}
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
