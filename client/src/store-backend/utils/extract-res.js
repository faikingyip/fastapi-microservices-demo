export const createNormalizedResponseData = (data, status, errors) => {
  return { data, status, errors };
};

export const extractAccessToken = (res) => {
  const token = res.data.access_token;
  if (!token) {
    throw new Error("Unable to extract the access token from the response.");
  }
  return token;
};

export const extractRefreshToken = (res) => {
  const token = res.data.refresh_token;
  if (!token) {
    throw new Error("Unable to extract the refresh token from the response.");
  }  
  return token;
};
