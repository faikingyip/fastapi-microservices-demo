export const isEmail = (text) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(text.toLowerCase());
};

export const isWithinMinLength = (value, minLength) => {
  return value.length >= minLength;
};

export const isWithinMaxLength = (value, maxLength) => {
  return value.length <= maxLength;
};
