import React from 'react';
import { Modal, Button } from 'react-bootstrap';

import EventForm from './EventForm';


const EventFormModal = (props) => {

  return (
    <Modal show={props.show} onHide={props.handleClose}>
      <Modal.Header closeButton>
        <Modal.Title className="text-center modal-header">
          {props.heading}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <EventForm
          formType={props.formType}
          handleFormSubmit={props.handleFormSubmit}
          formData={props.formData}
          handleFormChange={props.handleFormChange}
        />
      </Modal.Body>
      <Modal.Footer>
        <Button onClick={props.handleClose}>Close</Button>
        <Button bsStyle="primary" onClick={props.handleFormSubmit}>
          Save
        </Button>
      </Modal.Footer>
    </Modal>
  )
};

export default EventFormModal;
