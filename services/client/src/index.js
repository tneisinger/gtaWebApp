import React from 'react';
import ReactDOM from 'react-dom';

const App = () => {
  return (
    <div className="container">
      <div className="row">
        <div className="col-md-4">
          <br/>
          <h1>All Users</h1>
          <hr/><br/>
        </div>
      </div>
    </div>
  )
};

ReactDOM.render(
  <App />,
  document.getElementById('root')
);
