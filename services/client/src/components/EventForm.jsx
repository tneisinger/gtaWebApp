import React from 'react';
import PropTypes from 'prop-types';


// Define the valid values for formType
export const formTypes = ['Job', 'OneTimeExpense'];

// Define the appropriate default values for an empty job form
export const emptyJobFormData = {
  client: '',
  description: '',
  amount_paid: '',
  paid_to: 'Gladtime Audio',
  worked_by: 'Meghan',
  confirmation: 'Confirmed',
  has_paid: false,
  start_date: '',
  end_date: '',
}

// Define the appropriate default values for an empty oneTimeExpense form
export const emptyOneTimeExpenseFormData = {
  merchant: '',
  description: '',
  amount_spent: '',
  date: '',
  paid_by: 'Gladtime Audio',
  tax_deductible: false,
  category: 'Business Equipment',
}

// Define a default formData object.  This is used as the default formData
// value if no formData prop is provided when this component is instantiated.
// This can also be imported into another module and used to define the
// initial state of the formData values.
export const formData = {};
formData[formTypes[0]] = emptyJobFormData;
formData[formTypes[1]] = emptyOneTimeExpenseFormData;


const EventForm = (props) => {
  const data = props.formData[props.formType];
  return (
    <form onSubmit={(event) => props.onFormSubmit(event)}>

      {props.formType === formTypes[0] &&
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
            <label htmlFor="paid_to">Paid To</label>
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
          </div>

          <div className="form-group">
            <label htmlFor="worked_by">Worked By</label>
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
          </div>

          <div className="form-group">
            <label htmlFor="confirmation">Confirmation</label>
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
          </div>

          <div className="form-group">
            <label htmlFor="has_paid">Has Paid</label>
            <input
              id="has_paid"
              name="has_paid"
              className="form-check-input checkbox-lg"
              type="checkbox"
              value={data.has_paid}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="start_date">Start Date</label>
            <input
              id="start_date"
              name="start_date"
              className="form-control input-lg"
              type="date"
              required
              value={data.start_date}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="end_date">End Date</label>
            <input
              id="end_date"
              name="end_date"
              className="form-control input-lg"
              type="date"
              required
              value={data.end_date}
              onChange={props.onFormChange}
            />
          </div>
        </div>
      }

      {props.formType === formTypes[1] &&
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
            <label htmlFor="date">Date</label>
            <input
              id="date"
              name="date"
              className="form-control input-lg"
              type="date"
              required
              value={data.date}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="paid_by">Paid By</label>
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
          </div>

          <div className="form-group">
            <label htmlFor="tax_deductible">Tax Deductible</label>
            <input
              id="tax_deductible"
              name="tax_deductible"
              className="form-check-input checkbox-lg"
              type="checkbox"
              value={data.tax_deductible}
              onChange={props.onFormChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="category">Category</label>
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
          </div>
        </div>
      }

    </form>
  )
};

EventForm.propTypes = {
  formType: PropTypes.oneOf(formTypes).isRequired,
  formData: PropTypes.object,
  onFormChange: PropTypes.func.isRequired,
  onFormSubmit: PropTypes.func.isRequired
};

EventForm.defaultProps = {
  formData: formData
}

export default EventForm;
