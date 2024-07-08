/**
 * Evaluates all the provide a list of validation 
 * functions that returns and error message when
 * there are errors and returns false (invalid)
 * if any of the functions return in an error
 * message, or true if all returned an empty string.
 */
export const validateSet = (validationList) => {


  const validationErrorMessages = validationList.map((validation) =>
    validation.validationErrorMessageFn()
  );

  // We want no messages to be valid.
  if (validationErrorMessages.some((str) => str)) {
    return false;
  }

  // Valid
  return true;
};

/**
 * Determines if the specified multi checkbox field of the entered values provided
 * has at least one value supplied. Returns true if one or more values supplied,
 * else false.
 */
export const hasAtLeastOneSelection = (enteredValues, fieldName) => {
  if (enteredValues[fieldName] === undefined) {
    return false;
  }

  if (!enteredValues[fieldName]) {
    return false;
  }

  const selectedValues = enteredValues[fieldName];
  if (selectedValues.length < 1) {
    return false;
  }

  if (selectedValues.some((val) => val)) {
    return true;
  }

  return false;
};
