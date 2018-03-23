import React from 'react';
import { Route } from 'react-router-dom';

const PrivateRoute = ({ component: Component, ...rest }) => {
  <Route {...rest} render={(props) => (
    props.userLoggedIn
    ? <Component {...props} />
    : { () => props.handleDenyPrivateRouteAccess(props.location) }
  )}
};

export default PrivateRoute;
