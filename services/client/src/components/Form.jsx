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
  this.message = message;
  this.name = 'UnknownFormTypeException';
};

// Define the appropriate default values for an empty job form
const emptyJobFormData = {
  client: '',
  description: '',
  amountPaid: '',
  paidTo: 'Gladtime Audio',
  workedBy: 'Meghan',
  confirmation: 'Confirmed',
  hasPaid: false,
  startDate: '',
  endDate: '',
};

// Define the appropriate default values for an empty oneTimeExpense form
const emptyOneTimeExpenseFormData = {
  merchant: '',
  description: '',
  amountSpent: '',
  date: '',
  paidBy: 'Gladtime Audio',
  taxDeductible: false,
  category: 'Business Equipment',
};

// Define the appropriate default values for an empty login form
const emptyLoginFormData = {
  username: '',
  password: '',
  isPrivateDevice: false,
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
              autoFocus
              name="client"
              className="form-control input-lg input-client"
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
              className="form-control input-lg input-description"
              type="text"
              placeholder="Description"
              required
              value={data.description}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <input
              name="amountPaid"
              className="form-control input-lg input-amountPaid"
              type="number"
              placeholder="Amount Paid"
              required
              value={data.amountPaid}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="paidTo">
              Paid To
              <select
                id="paidTo"
                name="paidTo"
                className="form-control input-lg input-paidTo"
                placeholder="Paid To"
                required
                value={data.paidTo}
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
            <label htmlFor="workedBy">
              Worked By
              <select
                id="workedBy"
                name="workedBy"
                className="form-control input-lg input-workedBy"
                required
                value={data.workedBy}
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
                className="form-control input-lg input-confirmation"
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
            <label htmlFor="hasPaid">
              Has Paid
              <input
                id="hasPaid"
                name="hasPaid"
                className="form-check-input checkbox-lg input-hasPaid"
                type="checkbox"
                value={data.hasPaid}
                onChange={props.onFormChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="startDate">
              Start Date
              <input
                id="startDate"
                name="startDate"
                className="form-control input-lg input-startDate"
                type="date"
                required
                value={data.startDate}
                onChange={props.onFormChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="endDate">
              End Date
              <input
                id="endDate"
                name="endDate"
                className="form-control input-lg input-endDate"
                type="date"
                required
                value={data.endDate}
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
              autoFocus
              name="merchant"
              className="form-control input-lg input-merchant"
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
              className="form-control input-lg input-description"
              type="text"
              placeholder="Description"
              required
              value={data.description}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <input
              name="amountSpent"
              className="form-control input-lg input-amountSpent"
              type="number"
              placeholder="Amount Spent"
              required
              value={data.amountSpent}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="date">
              Date
              <input
                id="date"
                name="date"
                className="form-control input-lg input-date"
                type="date"
                required
                value={data.date}
                onChange={props.onFormChange}
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="paidBy">
              Paid By
              <select
                id="paidBy"
                name="paidBy"
                className="form-control input-lg input-paidBy"
                required
                value={data.paidBy}
                onChange={props.onFormChange}
              >
                <option value="Gladtime Audio">Gladtime Audio</option>
                <option value="Meghan">Meghan</option>
                <option value="Tyler">Tyler</option>
                <option value="Tyler and Meghan">
                  Tyler and Meghan
                </option>
              </select>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="taxDeductible">
              Tax Deductible
              <input
                id="taxDeductible"
                name="taxDeductible"
                className="form-check-input checkbox-lg input-taxDeductible"
                type="checkbox"
                value={data.taxDeductible}
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
                className="form-control input-lg input-category"
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
              autoFocus
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
            <label htmlFor="isPrivateDevice">
              <input
                id="isPrivateDevice"
                name="isPrivateDevice"
                className="form-check-input checkbox-lg"
                type="checkbox"
                value={data.isPrivateDevice}
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
  jobForm: PropTypes.shape({
    client: PropTypes.string,
    description: PropTypes.string,
    amountPaid: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    paidTo: PropTypes.string,
    workedBy: PropTypes.string,
    confirmation: PropTypes.string,
    hasPaid: PropTypes.bool,
    startDate: PropTypes.string,
    endDate: PropTypes.string,
  }),
  oneTimeExpenseForm: PropTypes.shape({
    merchant: PropTypes.string,
    description: PropTypes.string,
    amountSpent: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    date: PropTypes.string,
    paidBy: PropTypes.string,
    taxDeductible: PropTypes.bool,
    category: PropTypes.string,
  }),
  loginForm: PropTypes.shape({
    username: PropTypes.string,
    password: PropTypes.string,
    isPrivateDevice: PropTypes.bool,
  }),
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
