export const getEnteredValues = (eventOrFormData) => {
  /**
   * Retrieves all the entered values from the formData.
   * If the passed in object is an event, then first
   * retrieve the formData from the event.
   */

  let formData = eventOrFormData;
  if (!(eventOrFormData instanceof FormData)) {
    formData = new FormData(eventOrFormData.target);
  }

  // Retrieve all form values
  const enteredValues = {};
  for (var pair of formData.entries()) {
    if (!enteredValues[pair[0]]) {
      enteredValues[pair[0]] = [];
    }
    enteredValues[pair[0]].push(pair[1]);
  }

  return enteredValues;
};
