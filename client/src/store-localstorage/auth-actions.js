import { jwtDecode } from "jwt-decode";

const ACCESS_TOKEN = "access";
const REFRESH_TOKEN = "refresh";

const storeAuthTokens = ({ accessToken, refreshToken }) => {
  localStorage.setItem(ACCESS_TOKEN, accessToken);
  if (refreshToken) {
    localStorage.setItem(REFRESH_TOKEN, refreshToken);
  }
};

const clearAuthTokens = () => {
  localStorage.removeItem(ACCESS_TOKEN);
  localStorage.removeItem(REFRESH_TOKEN);
};

const getAccessToken = () => {
  return localStorage.getItem(ACCESS_TOKEN);
};

const getRefreshToken = () => {
  return localStorage.getItem(REFRESH_TOKEN);
};

const getDecodedAccessToken = () => {
  const accessToken = localStorage.getItem(ACCESS_TOKEN);
  if (!accessToken) {
    return null;
  }
  return jwtDecode(accessToken);
};

const isTokenExp = (token) => {
  return jwtDecode(token).exp < Date.now() / 1000; // get date in secs and not ms.
};

const getAuthDetails = () => {
  const decoded = getDecodedAccessToken();
  if (!decoded) {
    return null;
  }
  return {
    firstName: decoded.first_name,
    lastName: decoded.last_name,
    exp: decoded.exp,
  };
};

const authActions = {
  storeAuthTokens,
  clearAuthTokens,
  getAccessToken,
  getRefreshToken,
  getAuthDetails,
  isTokenExp,
};

export default authActions