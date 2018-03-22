import React from 'react';
import { Modal } from 'react-bootstrap';


const ChoiceModal = (props) => {
  return (
    <Modal
      className="choice-modal"
      show={props.show}
      onHide={props.onHide}
    >
      <Modal.Header closeButton>
        <Modal.Title className="text-center modal-header">
          {props.title}
        </Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {props.children}
      </Modal.Body>
    </Modal>
  )
};

export default ChoiceModal;
