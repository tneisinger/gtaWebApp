import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';

import Form, { emptyJobFormData, emptyOneTimeExpenseFormData,
         formTypes, formData } from '../Form';


const dummyFunction = () => { console.log('dummy function ran') };

formTypes.forEach((formType) => {
  test(`${formType} form renders properly`, () => {
    const component = <Form
                        formType={formType}
                        formData={formData}
                        onFormChange={dummyFunction}
                        onFormSubmit={dummyFunction}
                      />;
    const wrapper = shallow(component);
    const form = wrapper.find('form');
    expect(form.length).toBe(1);
    const formGroup = wrapper.find('.form-group');
    expect(formGroup.length).toBe(Object.keys(formData[formType]).length);
    expect(formGroup.get(0).props.children.props.name)
      .toBe(Object.keys(formData[formType])[0]);
    expect(formGroup.get(0).props.children.props.value).toBe('');
  });
  test(`${formType} form renders a snapshot properly`, () => {
    const component = <Form
                        formType={formType}
                        formData={formData}
                        onFormChange={dummyFunction}
                        onFormSubmit={dummyFunction}
                      />;
    const tree = renderer.create(component).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
