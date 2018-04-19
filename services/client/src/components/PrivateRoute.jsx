import React from 'react';
import { Route, Redirect } from 'react-router-dom';

import CheckingUserStatus from './CheckingUserStatus';

const PrivateRoute = ({ component: Component, ...rest }) => {

  // If userLoggedIn === null, that means that we don't yet know if the user
  // is logged in or not.  We are probably waiting for the server to respond to
  // a user status request.
  if (rest.userLoggedIn === null) {
    return (
      <Route {...rest} render={(props) => (
        <CheckingUserStatus />
      )} />
    );
  }

  return (
    <Route {...rest} render={(props) => (
      rest.userLoggedIn
      ? <Component {...rest.componentProps} />
      : <Redirect to={{
          pathname: "/",
          state: { from: props.location } }} />
    )} />
  );
};

export default PrivateRoute;
