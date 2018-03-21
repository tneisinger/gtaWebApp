import React from 'react';
import { Modal, Button } from 'react-bootstrap';


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
        <Button onClick={props.handleClose}>Close</Button>
        <Button
          bsStyle="primary"
          onClick={props.children.props.onFormSubmit}
        >
          Save
        </Button>
      </Modal.Footer>
    </Modal>
  )
};

export default FormModal;