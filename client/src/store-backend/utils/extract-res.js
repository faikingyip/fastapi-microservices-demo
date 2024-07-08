export const createNormalizedResponseData = (data, status, errors) => {
  return { data, status, errors };
};

export const extractAccessToken = (res) => {
  const token = res.data.access;
  if (!token) {
    throw new Error("Unable to extract the access token from the response.");
  }
  return token;
};

export const extractRefreshToken = (res) => {
  const token = res.data.refresh;
  if (!token) {
    throw new Error("Unable to extract the refresh token from the response.");
  }  
  return token;
};
