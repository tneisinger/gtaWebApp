import React from 'react';
import PropTypes from 'prop-types';

import { copy } from '../utils';


// Define the valid values for formType.  Treat this as an enumeration
// of the valid formTypes.
export const formTypes = {
  job: 'jobForm',
  oneTimeExpense: 'oneTimeExpenseForm',
  login: 'loginForm',
};

// Define an exception for when an unknown formType is discovered
export const UnknownFormTypeException = message => {
  this.message = message
  this.name = 'UnknownFormTypeException';
};

// Define the appropriate default values for an empty job form
const emptyJobFormData = {
  client: '',
  description: '',
  amount_paid: '',
  paid_to: 'Gladtime Audio',
  worked_by: 'Meghan',
  confirmation: 'Confirmed',
  has_paid: false,
  start_date: '',
  end_date: '',
};

// Define the appropriate default values for an empty oneTimeExpense form
const emptyOneTimeExpenseFormData = {
  merchant: '',
  description: '',
  amount_spent: '',
  date: '',
  paid_by: 'Gladtime Audio',
  tax_deductible: false,
  category: 'Business Equipment',
};

// Define the appropriate default values for an empty login form
const emptyLoginFormData = {
  username: '',
  password: '',
  private_device: false,
};

// Define a defaultFormData object.  This is used as the default formData
// value if no formData prop is provided when this component is instantiated.
// This can also be imported into another module and used to define the
// initial state of the formData values.  Make copies of the empty data objects
// so that the original objects don't get changed when formData gets modified.
export const defaultFormData = {};
defaultFormData[formTypes.job] = copy(emptyJobFormData);
defaultFormData[formTypes.oneTimeExpense] = copy(emptyOneTimeExpenseFormData);
defaultFormData[formTypes.login] = copy(emptyLoginFormData);


const Form = (props) => {
  const data = props.formData[props.formType];
  return (
    <form onSubmit={event => props.onFormSubmit(event)}>

      {props.formType === formTypes.job &&
        /* render the job form inputs */
        <div>
          <div className="form-group">
            <input
              name="client"
              className="form-control input-lg"
              type="text"
              placeholder="Client Name"
              required
              value={data.client}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <input
              name="description"
              className="form-control input-lg"
              type="text"
              placeholder="Description"
              required
              value={data.description}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <input
              name="amount_paid"
              className="form-control input-lg"
              type="number"
              placeholder="Amount Paid"
              required
              value={data.amount_paid}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="paid_to">
              Paid To
              <select
                id="paid_to"
                name="paid_to"
                className="form-control input-lg"
                placeholder="Paid To"
                required
                value={data.paid_to}
                onChange={props.onFormChange}
              >
                <option value="Gladtime Audio">Gladtime Audio</option>
                <option value="Meghan">Meghan</option>
                <option value="Tyler">Tyler</option>
                <option value="Tyler/Meghan Separately">
                  Tyler/Meghan Separately
                </option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="worked_by">
              Worked By
              <select
                id="worked_by"
                name="worked_by"
                className="form-control input-lg"
                required
                value={data.worked_by}
                onChange={props.onFormChange}
              >
                <option value="Meghan">Meghan</option>
                <option value="Tyler">Tyler</option>
                <option value="Tyler and Meghan">Tyler and Meghan</option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="confirmation">
              Confirmation
              <select
                id="confirmation"
                name="confirmation"
                className="form-control input-lg"
                required
                value={data.confirmation}
                onChange={props.onFormChange}
              >
                <option value="Confirmed">Confirmed</option>
                <option value="Pencilled In">Pencilled In</option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="has_paid">
              Has Paid
              <input
                id="has_paid"
                name="has_paid"
                className="form-check-input checkbox-lg"
                type="checkbox"
                value={data.has_paid}
                onChange={props.onFormChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="start_date">
              Start Date
              <input
                id="start_date"
                name="start_date"
                className="form-control input-lg"
                type="date"
                required
                value={data.start_date}
                onChange={props.onFormChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="end_date">
              End Date
              <input
                id="end_date"
                name="end_date"
                className="form-control input-lg"
                type="date"
                required
                value={data.end_date}
                onChange={props.onFormChange}
              />
            </label>
          </div>
        </div>
      }

      {props.formType === formTypes.oneTimeExpense &&
        /* Render the oneTimeExpense form inputs */
        <div>
          <div className="form-group">
            <input
              name="merchant"
              className="form-control input-lg"
              type="text"
              placeholder="Bought From"
              required
              value={data.merchant}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <input
              name="description"
              className="form-control input-lg"
              type="text"
              placeholder="Description"
              required
              value={data.description}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <input
              name="amount_spent"
              className="form-control input-lg"
              type="number"
              placeholder="Amount Spent"
              required
              value={data.amount_spent}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="date">
              Date
              <input
                id="date"
                name="date"
                className="form-control input-lg"
                type="date"
                required
                value={data.date}
                onChange={props.onFormChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="paid_by">
              Paid By
              <select
                id="paid_by"
                name="paid_by"
                className="form-control input-lg"
                required
                value={data.paid_by}
                onChange={props.onFormChange}
              >
                <option value="Gladtime Audio">Gladtime Audio</option>
                <option value="Meghan">Meghan</option>
                <option value="Tyler">Tyler</option>
                <option value="Tyler/Meghan Separately">
                  Tyler/Meghan Separately
                </option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="tax_deductible">
              Tax Deductible
              <input
                id="tax_deductible"
                name="tax_deductible"
                className="form-check-input checkbox-lg"
                type="checkbox"
                value={data.tax_deductible}
                onChange={props.onFormChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="category">
              Category
              <select
                id="category"
                name="category"
                className="form-control input-lg"
                required
                value={data.category}
                onChange={props.onFormChange}
              >
                <option value="Business Equipment">Business Equipment</option>
                <option value="Business Supplies">Business Supplies</option>
                <option value="Gasoline">Gasoline</option>
                <option value="Vehicle Maintenance">Vehicle Maintenance</option>
                <option value="Travel Expense">Travel Expense</option>
                <option value="Entertainment">Entertainment</option>
                <option value="Food">Food</option>
              </select>
            </label>
          </div>
        </div>
      }

      {props.formType === formTypes.login &&
        /* Render the login form inputs */
        <div>
          <div className="form-group">
            <input
              name="username"
              className="form-control input-lg"
              type="text"
              placeholder="Enter username"
              required
              value={data.username}
              onChange={props.onFormChange}
            />
          </div>
          <div className="form-group">
            <input
              name="password"
              className="form-control input-lg"
              type="password"
              placeholder="Enter password"
              required
              value={data.password}
              onChange={props.onFormChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="private_device">
              <input
                id="private_device"
                name="private_device"
                className="form-check-input checkbox-lg"
                type="checkbox"
                value={data.private_device}
                onChange={props.onFormChange}
              />
              Keep me logged in. This is a private device.
            </label>
          </div>
        </div>
      }

    </form>
  );
};

// Define the shape of the formData prop for use in the propType defs
const formDataShape = {
  jobForm: {
    client: PropTypes.string,
    description: PropTypes.string,
    amount_paid: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    paid_to: PropTypes.string,
    worked_by: PropTypes.string,
    confirmation: PropTypes.string,
    has_paid: PropTypes.bool,
    start_date: PropTypes.string,
    end_date: PropTypes.string,
  },
  oneTimeExpenseForm: {
    merchant: PropTypes.string,
    description: PropTypes.string,
    amount_spent: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    date: PropTypes.string,
    paid_by: PropTypes.string,
    tax_deductible: PropTypes.bool,
    category: PropTypes.string,
  },
  loginForm: {
    username: PropTypes.string,
    password: PropTypes.string,
    private_device: PropTypes.bool,
  },
};

Form.propTypes = {
  formType: PropTypes.oneOf(Object.values(formTypes)).isRequired,
  formData: PropTypes.shape(formDataShape),
  onFormChange: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired,
};

Form.defaultProps = {
  formData: defaultFormData,
};

export default Form;
