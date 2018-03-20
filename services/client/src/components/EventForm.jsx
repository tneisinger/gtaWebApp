import React from 'react';
import PropTypes from 'prop-types';

const EventForm = (props) => {
  if (props.formType === 'jobForm') {
    return (
      <form onSubmit={(event) => props.handleFormSubmit(event)}>

        <div className="form-group">
          <input
            name="client"
            className="form-control input-lg"
            type="text"
            placeholder="Client Name"
            required
            value={props.formData.jobForm.client}
            onChange={props.handleFormChange}
          />
        </div>

        <div className="form-group">
          <input
            name="description"
            className="form-control input-lg"
            type="text"
            placeholder="Description"
            required
            value={props.formData.jobForm.description}
            onChange={props.handleFormChange}
          />
        </div>

        <div className="form-group">
          <input
            name="amount_paid"
            className="form-control input-lg"
            type="number"
            placeholder="Amount Paid"
            required
            value={props.formData.jobForm.amount_paid}
            onChange={props.handleFormChange}
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
            value={props.formData.jobForm.paid_to}
            onChange={props.handleFormChange}
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
            value={props.formData.jobForm.worked_by}
            onChange={props.handleFormChange}
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
            value={props.formData.jobForm.confirmation}
            onChange={props.handleFormChange}
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
            value={props.formData.jobForm.has_paid}
            onChange={props.handleFormChange}
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
            value={props.formData.jobForm.start_date}
            onChange={props.handleFormChange}
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
            value={props.formData.jobForm.end_date}
            onChange={props.handleFormChange}
          />
        </div>

      </form>
    )
  } else if (props.formType === 'oneTimeExpenseForm') {
    return (
      <form onSubmit={(event) => props.handleFormSubmit(event)}>

        <div className="form-group">
          <input
            name="merchant"
            className="form-control input-lg"
            type="text"
            placeholder="Bought From"
            required
            value={props.formData.oneTimeExpenseForm.merchant}
            onChange={props.handleFormChange}
          />
        </div>

        <div className="form-group">
          <input
            name="description"
            className="form-control input-lg"
            type="text"
            placeholder="Description"
            required
            value={props.formData.oneTimeExpenseForm.description}
            onChange={props.handleFormChange}
          />
        </div>

        <div className="form-group">
          <input
            name="amount_spent"
            className="form-control input-lg"
            type="number"
            placeholder="Amount Spent"
            required
            value={props.formData.oneTimeExpenseForm.amount_spent}
            onChange={props.handleFormChange}
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
            value={props.formData.oneTimeExpenseForm.date}
            onChange={props.handleFormChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="paid_by">Paid By</label>
          <select
            id="paid_by"
            name="paid_by"
            className="form-control input-lg"
            required
            value={props.formData.oneTimeExpenseForm.paid_by}
            onChange={props.handleFormChange}
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
            value={props.formData.oneTimeExpenseForm.tax_deductible}
            onChange={props.handleFormChange}
          />
        </div>

        <div className="form-group">
          <label htmlFor="category">Category</label>
          <select
            id="category"
            name="category"
            className="form-control input-lg"
            required
            value={props.formData.oneTimeExpenseForm.category}
            onChange={props.handleFormChange}
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

      </form>
    )
  }
};

EventForm.propTypes = {
  formType: PropTypes.oneOf(['jobForm', 'oneTimeExpenseForm']).isRequired,
  handleFormSubmit: PropTypes.func.isRequired,
  formData: PropTypes.object.isRequired,
  handleFormChange: PropTypes.func.isRequired
};

export default EventForm;
