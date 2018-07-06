import React from 'react';
import { Modal, Button } from 'react-bootstrap';

import { formTypes } from './Form';


const FormModal = (props) => {
  return (
    <Modal show={props.show} onHide={props.handleClose}>
      <Modal.Header closeButton>
        <Modal.Title className="text-center modal-header">
          {props.heading}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {props.children}
      </Modal.Body>
      <Modal.Footer>
        {props.formType === formTypes.job &&
         props.isDeletable &&
          <Button
            bsStyle="danger"
            className="pull-left"
            onClick={props.onDeleteJobBtnClick}
          >
            Delete This Job
          </Button>
        }
        {props.formType === formTypes.oneTimeExpense &&
         props.isDeletable &&
          <Button
            bsStyle="danger"
            className="pull-left"
            onClick={props.onDeleteExpenseBtnClick}
          >
            Delete This Expense
          </Button>
        }
        <Button onClick={props.handleClose}>Close</Button>
        <Button
          bsStyle="primary"
          onClick={props.children.props.onFormSubmit}
        >
          Submit
        </Button>
      </Modal.Footer>
    </Modal>
  )
};

export default FormModal;
