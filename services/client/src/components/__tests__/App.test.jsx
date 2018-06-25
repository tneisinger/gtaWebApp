import React from 'react';
import { shallow, mount } from 'enzyme';
import { MemoryRouter } from 'react-router';
import { withRouter } from 'react-router-dom';
import { spy } from 'sinon';
import mockAxios from 'jest-mock-axios';
import moment from 'moment';

import App from '../../App';
import Calendar from '../Calendar';
import NavBar from '../NavBar';
import PrivateRoute from '../PrivateRoute';
import CheckingUserStatus from '../CheckingUserStatus';
import FormModal from '../FormModal';
import { defaultFormData, formTypes } from '../Form';
import { LocalStorageMock } from '../../testUtils';
import { copy, deepcopy} from '../../utils';


global.localStorage = new LocalStorageMock();

test('App renders without crashing', () => {
  const wrapper = shallow(<App />);
  expect(wrapper.find('div').length).toBeGreaterThan(0);
});

describe('The main App component', () => {
  //  instantiate a variable that will hold the mounted App, wrapped in a
  //  MemoryRouter component.  This will get passed to tests to check the
  //  status of the app.
  let memRoutedApp;

  // instantiate a variable that will hold the router history for a given test
  let routerHistory;

  // Return the mounted MemoryRouter that wraps the App component.  If the
  // memRoutedApp has not yet been created for the current test, this function
  // will create it before returning it.
  const wrappedApp = () => {
    if (!memRoutedApp) {

      // Use withRouter so that url info gets passed into App props.
      // This will allow us to check the current url of the App in our tests.
      const AppWithRouter = withRouter(App);

      memRoutedApp = mount(
        <MemoryRouter initialEntries={routerHistory}>
          <AppWithRouter />
        </MemoryRouter>,
      );
    }
    return memRoutedApp;
  };

  // Return a direct reference to the mounted App component.  This is useful
  // when you want check the state of the App component.
  const appInstance = () => wrappedApp().find(App).instance();

  // Before each test...
  beforeEach(() => {
    // Reset the routerHistory and memRoutedApp to undefined
    routerHistory = undefined;
    memRoutedApp = undefined;
    // Reset the mocked localStorage to empty
    global.localStorage = new LocalStorageMock();

    // This is needed for setTimeouts to work in tests
    jest.useFakeTimers();
  });

  it('always renders a div', () => {
    const divs = wrappedApp().find('div');
    expect(divs.length).toBeGreaterThan(0);
  });

  it('has an outer div that contains everything', () => {
    expect(wrappedApp().children().length).toEqual(1);
  });

  it('always renders a NavBar', () => {
    expect(wrappedApp().find(NavBar).length).toBe(1);
  });

  it('always renders a FormModal', () => {
    expect(wrappedApp().find(FormModal).length).toBe(1);
  });

  it('runs the componentDidMount method', () => {
    const componentDidMountSpy = spy(App.prototype, 'componentDidMount');
    wrappedApp();
    expect(App.prototype.componentDidMount.calledOnce).toEqual(true);
    componentDidMountSpy.restore();
  });

  // Instantiate the goodUserStatusResponse var in a wider scope
  let goodUserStatusResponse;

  describe('when a valid authToken is saved in localStorage', () => {
    beforeEach(() => {
      window.localStorage.setItem('authToken', 'valid token wink wink');

      // Create a date string that is five seconds in the future to mock the
      // authToken expire time that would be returned from the server.
      let t = new Date();
      t.setSeconds(t.getSeconds() + 5);
      let expireTime = t.toString();

      // Create a mock of a good response object from the server
      goodUserStatusResponse = {
        status: 200,
        data: {
          user: {
            email: 'fake@fake.com',
            id: 13,
            username: 'Fred',
          },
          expiration: expireTime,
        },
      };

    });

    afterEach(() => {

      mockAxios.reset();
    });

    it('should set the userLoggedIn state value to true', () => {
      wrappedApp();

      mockAxios.mockResponse(goodUserStatusResponse);

      expect(appInstance().state.userLoggedIn).toBe(true);
    });

    it('should set the username state value correctly', () => {
      wrappedApp();

      mockAxios.mockResponse(goodUserStatusResponse);

      expect(appInstance().state.username).toBe(
        goodUserStatusResponse.data.user.username,
      );
    });

    it('should automatically logout after expiration time has passed', () => {
      // Create a date string that is a few milliseconds in the future.  By the
      // time that we test if the user is still logged in, this time should be
      // in the passed and the user should be automatically logged out.
      let t = new Date();
      t.setMilliseconds(t.getMilliseconds() + 1);
      let expireTime = t.toString();

      goodUserStatusResponse.expiration = expireTime;

      wrappedApp();

      mockAxios.mockResponse(goodUserStatusResponse);

      expect(setTimeout).toHaveBeenCalledTimes(1);
      expect(setTimeout).toHaveBeenLastCalledWith(
        expect.any(Function), expect.any(Number)
      );

      expect(appInstance().state.userLoggedIn).toBe(true);
      expect(appInstance().state.username).toBe(
        goodUserStatusResponse.data.user.username,
      );

      // Run the timers so we can check state after some time has passed
      jest.runAllTimers();

      expect(appInstance().state.userLoggedIn).toBe(false);
      expect(appInstance().state.username).toBe('');
    });

    describe('when on the calendar page', () => {
      beforeEach(() => {
        routerHistory = ['/calendar'];
      });

      it('should not redirect to homepage if user is logged in', () => {
        wrappedApp();

        mockAxios.mockResponse(goodUserStatusResponse);

        expect(appInstance().state.userLoggedIn).toBe(true);
        expect(appInstance().state.username).toBe(
          goodUserStatusResponse.data.user.username,
        );
        expect(appInstance().props.location.pathname).toBe('/calendar')
      });

      it('clicking one day of the calendar should open choiceModal', () => {
        wrappedApp();

        mockAxios.mockResponse(goodUserStatusResponse);

        // Make sure the Calendar gets rendered with update()
        wrappedApp().update();

        // Fake a calendar click by directly running the Calendar's
        // onSelectSlot method.
        let clickedDate = new Date();
        clickedDate.setDate(15);  // The 15th of the current month
        const slotInfo = { start: clickedDate, end: clickedDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slotInfo);
        wrappedApp().update();

        // The choiceModal should now be shown.
        // Click the 'New Job' button
        expect(appInstance().state.showChoiceModal).toBe(true);
      });

      it('Clicking "New Job" in choiceModal shows job formModal', () => {
        wrappedApp();

        mockAxios.mockResponse(goodUserStatusResponse);

        // Make sure the Calendar gets rendered with update()
        wrappedApp().update();

        // Fake a calendar click by directly running the Calendar's
        // onSelectSlot method.
        let clickedDate = new Date();
        clickedDate.setDate(15);  // The 15th of the current month
        const slotInfo = { start: clickedDate, end: clickedDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slotInfo);
        wrappedApp().update();

        // The choiceModal should now be shown.
        // Click the 'New Job' button
        const newJobBtn = wrappedApp()
            .find('.modal-body').find('.btn-primary');
        newJobBtn.simulate('click');
        wrappedApp().update();

        // The formModal should now be shown, showing the job form
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.job);

        // The start and end date inputs should be populated with
        // a date that matches the clickedDate we defined above.
        expect(wrappedApp().find('.input-startDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );
        expect(wrappedApp().find('.input-endDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );
      });

      it('A new job event should be rendered after creating a new job', () => {
        wrappedApp();

        let userStatusRequestInfo = mockAxios.lastReqGet();
        mockAxios.mockResponse(goodUserStatusResponse, userStatusRequestInfo);

        // Make sure the Calendar gets rendered with update()
        wrappedApp().update();

        // Fake a calendar click by directly running the Calendar's
        // onSelectSlot method.
        let clickedDate = new Date();
        clickedDate.setDate(15);  // The 15th of the current month
        const slotInfo = { start: clickedDate, end: clickedDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slotInfo);
        wrappedApp().update();

        // The choiceModal should now be shown.
        // Click the 'New Job' button
        const newJobBtn = wrappedApp()
            .find('.modal-body').find('.btn-primary');
        newJobBtn.simulate('click');
        wrappedApp().update();

        // The formModal should now be shown, showing the job form
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.job);

        // The start and end date inputs should be populated with
        // a date that matches the clickedDate we defined above.
        expect(wrappedApp().find('#startDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );
        expect(wrappedApp().find('#endDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );

        const submitBtn = wrappedApp()
            .find('.modal-footer').find('.btn-primary');
        submitBtn.simulate('click');

        let addJobRequestInfo = mockAxios.lastReqGet();

        mockAxios.mockResponse({
          data: {
            job: {
              client: 'test client value',
              description: 'test description value',
              amountPaid: 300,
              paidTo: 'Gladtime Audio',
              workedBy: 'Tyler',
              confirmation: 'Confirmed',
              hasPaid: false,
              startDate: (new Date()).yyyymmdd('-'),
              endDate: (new Date()).yyyymmdd('-'),
            }
          }
        }, addJobRequestInfo);

        wrappedApp().update();

        const calendarEvents = wrappedApp().find('.rbc-event');
        expect(calendarEvents.length).toBe(1);

        const eventTitle = calendarEvents.find('.rbc-event-content').text();
        expect(eventTitle).toBe('test client value');
      });

      it('Clicking on a BC job event should bring up job form modal', () => {
        wrappedApp();

        let userStatusRequestInfo = mockAxios.lastReqGet();
        mockAxios.mockResponse(goodUserStatusResponse, userStatusRequestInfo);

        // Make sure the Calendar gets rendered with update()
        wrappedApp().update();

        // Fake a calendar click by directly running the Calendar's
        // onSelectSlot method.
        let clickedDate = new Date();
        const currentYear = clickedDate.getFullYear();
        const currentMonth = clickedDate.getMonth();
        // Select the 15th of the current month as the clicked date
        clickedDate = new Date(currentYear, currentMonth, 15);
        const slotInfo = { start: clickedDate, end: clickedDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slotInfo);
        wrappedApp().update();

        // The choiceModal should now be shown.
        // Click the 'New Job' button
        const newJobBtn = wrappedApp()
            .find('.modal-body').find('.btn-primary');
        newJobBtn.simulate('click');
        wrappedApp().update();

        // Submit the job form
        const submitBtn = wrappedApp()
            .find('.modal-footer').find('.btn-primary');
        submitBtn.simulate('click');

        let addJobRequestInfo = mockAxios.lastReqGet();

        const jobData = {
          client: 'test client value',
          description: 'test description value',
          amountPaid: 300,
          paidTo: 'Gladtime Audio',
          workedBy: 'Tyler',
          confirmation: 'Confirmed',
          hasPaid: false,
          startDate: clickedDate.yyyymmdd('-'),
          endDate: clickedDate.yyyymmdd('-'),
        };

        mockAxios.mockResponse({
          data: {
            job: jobData
          }
        }, addJobRequestInfo);

        wrappedApp().update();

        // There should be one job event on the calendar
        const calendarEvents = wrappedApp().find('.rbc-event');
        expect(calendarEvents.length).toBe(1);

        // Click on the one job event
        const jobEvent = calendarEvents.find('.rbc-event-content');
        jobEvent.simulate('click');

        // The formModal should now be shown, showing the job form
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.job);

        // Check that the form is populated with the job data
        expect(wrappedApp().find('.input-client').props().value).toBe(
          jobData.client
        );
        expect(wrappedApp().find('.input-description').props().value).toBe(
          jobData.description
        );
        expect(wrappedApp().find('.input-amountPaid').props().value).toBe(
          jobData.amountPaid
        );
        expect(wrappedApp().find('.input-paidTo').props().value).toBe(
          jobData.paidTo
        );
        expect(wrappedApp().find('.input-workedBy').props().value).toBe(
          jobData.workedBy
        );
        expect(wrappedApp().find('.input-confirmation').props().value).toBe(
          jobData.confirmation
        );
        expect(wrappedApp().find('.input-hasPaid').props().value).toBe(
          jobData.hasPaid
        );
        expect(wrappedApp().find('.input-startDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );
        expect(wrappedApp().find('.input-endDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );
      });

      it('Job form should be reset when new job form opens', () => {
        wrappedApp();

        let userStatusRequestInfo = mockAxios.lastReqGet();
        mockAxios.mockResponse(goodUserStatusResponse, userStatusRequestInfo);

        // Make sure the Calendar gets rendered with update()
        wrappedApp().update();

        // Fake a calendar click by directly running the Calendar's
        // onSelectSlot method.
        let clickedDate = new Date();
        const currentYear = clickedDate.getFullYear();
        const currentMonth = clickedDate.getMonth();
        // Select the 15th of the current month as the clicked date
        clickedDate = new Date(currentYear, currentMonth, 15);
        const slotInfo = { start: clickedDate, end: clickedDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slotInfo);
        wrappedApp().update();

        // The choiceModal should now be shown.
        // Click the 'New Job' button
        const newJobBtn = wrappedApp()
            .find('.modal-body').find('.btn-primary');
        newJobBtn.simulate('click');
        wrappedApp().update();

        // Submit the job form
        const submitBtn = wrappedApp()
            .find('.modal-footer').find('.btn-primary');
        submitBtn.simulate('click');

        let addJobRequestInfo = mockAxios.lastReqGet();

        const jobData = {
          client: 'test client value',
          description: 'test description value',
          amountPaid: 300,
          paidTo: 'Gladtime Audio',
          workedBy: 'Tyler',
          confirmation: 'Confirmed',
          hasPaid: false,
          startDate: clickedDate.yyyymmdd('-'),
          endDate: clickedDate.yyyymmdd('-'),
        };

        mockAxios.mockResponse({
          data: {
            job: jobData
          }
        }, addJobRequestInfo);

        wrappedApp().update();

        // There should be one job event on the calendar
        const calendarEvents = wrappedApp().find('.rbc-event');
        expect(calendarEvents.length).toBe(1);

        // Click on the one job event
        const jobEvent = calendarEvents.find('.rbc-event-content');
        jobEvent.simulate('click');

        // The formModal should now be shown, showing the job form
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.job);

        // Check that the form is populated with the job data
        expect(wrappedApp().find('.input-client').props().value).toBe(
          jobData.client
        );
        expect(wrappedApp().find('.input-description').props().value).toBe(
          jobData.description
        );
        expect(wrappedApp().find('.input-amountPaid').props().value).toBe(
          jobData.amountPaid
        );
        expect(wrappedApp().find('.input-paidTo').props().value).toBe(
          jobData.paidTo
        );
        expect(wrappedApp().find('.input-workedBy').props().value).toBe(
          jobData.workedBy
        );
        expect(wrappedApp().find('.input-confirmation').props().value).toBe(
          jobData.confirmation
        );
        expect(wrappedApp().find('.input-hasPaid').props().value).toBe(
          jobData.hasPaid
        );
        expect(wrappedApp().find('.input-startDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );
        expect(wrappedApp().find('.input-endDate').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );

        // Close the job form
        const closeButton = wrappedApp().find('.close').last();
        closeButton.simulate('click');

        // Make sure that the form modal is closed
        expect(appInstance().state.showFormModal).toBe(false);

        // Fake a calendar click by directly running the Calendar's
        // Select the 20th and 21st of the current month
        const startDate = new Date(currentYear, currentMonth, 20);
        const endDate = new Date(currentYear, currentMonth, 21);
        const slot = { start: startDate, end: endDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slot);
        wrappedApp().update();

        // Make sure that the job form modal is open
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.job);

        // Check that the job form has been reset
        expect(wrappedApp().find('.input-client').props().value).toBe('');
        expect(wrappedApp().find('.input-description').props().value).toBe('');
        expect(wrappedApp().find('.input-amountPaid').props().value).toBe('');
        expect(wrappedApp().find('.input-paidTo').props().value).toBe(
          'Gladtime Audio'
        );
        expect(wrappedApp().find('.input-workedBy').props().value).toBe(
          'Meghan'
        );
        expect(wrappedApp().find('.input-confirmation').props().value).toBe(
          'Confirmed'
        );
        expect(wrappedApp().find('.input-hasPaid').props().value).toBe(false);
        expect(wrappedApp().find('.input-startDate').props().value).toBe(
          startDate.yyyymmdd('-')
        );
        expect(wrappedApp().find('.input-endDate').props().value).toBe(
          endDate.yyyymmdd('-')
        );

      });

      it('Creating a new oneTimeExpense should render of BC event', () => {
        wrappedApp();

        let userStatusRequestInfo = mockAxios.lastReqGet();
        mockAxios.mockResponse(goodUserStatusResponse, userStatusRequestInfo);

        // Make sure the Calendar gets rendered with update()
        wrappedApp().update();

        // Fake a calendar click by directly running the Calendar's
        // onSelectSlot method.
        let clickedDate = new Date();
        clickedDate.setDate(16);  // The 16th of the current month
        const slotInfo = { start: clickedDate, end: clickedDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slotInfo);
        wrappedApp().update();

        // The choiceModal should now be shown.
        // Click the 'New Expense' button
        const newExpenseBtn = wrappedApp()
            .find('.modal-body').find('.btn-danger');
        newExpenseBtn.simulate('click');
        wrappedApp().update();

        // The formModal should now be shown, showing the job form
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.oneTimeExpense);

        // The date input should be populated with a date that matches the
        // clickedDate we defined above.
        expect(wrappedApp().find('#date').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );

        const submitBtn = wrappedApp()
            .find('.modal-footer').find('.btn-primary');
        submitBtn.simulate('click');

        let addExpenseRequestInfo = mockAxios.lastReqGet();

        mockAxios.mockResponse({
          data: {
            expense: {
              merchant: 'Trew Audio',
              description: 'cables',
              amountSpent: 300,
              paidBy: 'Gladtime Audio',
              taxDeductible: true,
              category: 'Business Equipment',
              date: clickedDate.yyyymmdd('-'),
            }
          }
        }, addExpenseRequestInfo);

        wrappedApp().update();

        const calendarEvents = wrappedApp().find('.rbc-event');
        expect(calendarEvents.length).toBe(1);

        const eventTitle = calendarEvents.find('.rbc-event-content').text();
        expect(eventTitle).toBe('Trew Audio');
      });

      it('Clicking on a BC expense event should bring up form modal', () => {
        wrappedApp();

        let userStatusRequestInfo = mockAxios.lastReqGet();
        mockAxios.mockResponse(goodUserStatusResponse, userStatusRequestInfo);

        // Make sure the Calendar gets rendered with update()
        wrappedApp().update();

        // Fake a calendar click by directly running the Calendar's
        // onSelectSlot method.
        let clickedDate = new Date();
        const currentYear = clickedDate.getFullYear();
        const currentMonth = clickedDate.getMonth();
        // Select the 16th of the current month as the clicked date
        clickedDate = new Date(currentYear, currentMonth, 16);
        const slotInfo = { start: clickedDate, end: clickedDate };
        wrappedApp().find(Calendar).prop('onSelectSlot')(slotInfo);
        wrappedApp().update();

        // The choiceModal should now be shown.
        // Click the 'New Expense' button
        const newExpenseBtn = wrappedApp()
            .find('.modal-body').find('.btn-danger');
        newExpenseBtn.simulate('click');
        wrappedApp().update();

        // The formModal should now be shown, showing the job form
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.oneTimeExpense);

        // The date input should be populated with a date that matches the
        // clickedDate we defined above.
        expect(wrappedApp().find('#date').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );

        const submitBtn = wrappedApp()
            .find('.modal-footer').find('.btn-primary');
        submitBtn.simulate('click');

        let addExpenseRequestInfo = mockAxios.lastReqGet();

        const expenseData = {
          merchant: 'Trew Audio',
          description: 'cables',
          amountSpent: 300,
          paidBy: 'Gladtime Audio',
          taxDeductible: true,
          category: 'Business Equipment',
          date: clickedDate.yyyymmdd('-'),
        }

        mockAxios.mockResponse({
          data: {
            expense: expenseData,
          }
        }, addExpenseRequestInfo);

        wrappedApp().update();

        // There should be one expense event on the calendar
        const expenseEvents = wrappedApp().find('.expense-event');
        expect(expenseEvents.length).toBe(1);

        // Click on the one expense event
        const expenseEventContent = expenseEvents.find('.rbc-event-content');
        expenseEventContent.simulate('click');

        // The formModal should now be shown, showing the expense form
        expect(appInstance().state.showFormModal).toBe(true);
        expect(appInstance().state.formType).toBe(formTypes.oneTimeExpense);

        // Check that the form is populated with the expense data
        expect(wrappedApp().find('.input-merchant').props().value).toBe(
          expenseData.merchant
        );
        expect(wrappedApp().find('.input-description').props().value).toBe(
          expenseData.description
        );
        expect(wrappedApp().find('.input-amountSpent').props().value).toBe(
          expenseData.amountSpent
        );
        expect(wrappedApp().find('.input-paidBy').props().value).toBe(
          expenseData.paidBy
        );
        expect(wrappedApp().find('.input-taxDeductible').props().value).toBe(
          expenseData.taxDeductible
        );
        expect(wrappedApp().find('.input-category').props().value).toBe(
          expenseData.category
        );
        expect(wrappedApp().find('.input-date').props().value).toBe(
          moment(clickedDate).format('YYYY-MM-DD')
        );
      });

    });
  });

  describe('when an invalid authToken is saved in localStorage', () => {
    beforeEach(() => {
      global.localStorage = new LocalStorageMock();
      window.localStorage.setItem('authToken', 'invalid token wink wink');

      // Create a date string that is five seconds in the future to mock the
      // authToken expire time that would be returned from the server.
      let t = new Date();
      t.setSeconds(t.getSeconds() + 5);
      let expireTime = t.toString();
    });

    afterEach(() => {
      mockAxios.reset();
    });

    const badUserStatusResponse = {
      status: 401,
      data: {
        status: 'fail',
        message: 'Provide a valid auth token',
      },
    };

    it('should set the userLoggedIn state value to false', () => {
      wrappedApp();

      mockAxios.mockError(badUserStatusResponse);

      expect(appInstance().state.userLoggedIn).toBe(false);
    });

    it('should set the username state value to the empty string', () => {
      wrappedApp();

      mockAxios.mockError(badUserStatusResponse);

      expect(appInstance().state.username).toBe('');
    });

    describe('and starting from the calendar page', () => {

      it('should redirect to homepage because user not signed in', () => {
        wrappedApp();

        mockAxios.mockError(badUserStatusResponse);

        expect(appInstance().props.location.pathname).toBe('/')
      });

    });
  });

  describe('when no authToken is saved in localStorage', () => {
    it('should set the userLoggedIn state value to false', () => {
      expect(appInstance().state.userLoggedIn).toBe(false);
    });

    it('should have a username state value of the empty string', () => {
      expect(appInstance().state.username).toBe('');
    });
  });
});
