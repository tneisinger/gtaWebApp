import React from 'react';
import { Modal, Button } from 'react-bootstrap';


const ChoiceModal = (props) => {
  return (
    <Modal
      className="choice-modal"
      show={props.show}
      onHide={props.handleClose}
    >
      <Modal.Header closeButton>
        <Modal.Title className="text-center modal-header">
          {props.heading}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <Button bsStyle="primary" onClick={props.handleLeftButtonClick}>
          {props.leftButtonText}
        </Button>
        <Button bsStyle="danger" onClick={props.handleRightButtonClick}>
          {props.rightButtonText}
        </Button>
      </Modal.Body>
    </Modal>
  )
};

export default ChoiceModal;
