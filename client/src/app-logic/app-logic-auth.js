import apiCalls from "../store-backend/api-calls";
import { extractAccessToken } from "../store-backend/utils/extract-res";
import authActions from "../store-localstorage/auth-actions";
import configureSharedPromise from "../utils/utils.shared-promise";

const refreshToken = async () => {
  /**
   * Send the existing refresh token to get the refreshed
   * access token.
   *
   * Returns the access token if refreshed, else null.
   */

  const refreshToken = authActions.getRefreshToken();
  if (authActions.isTokenExp(refreshToken)) {
    return null;
  }

  const payload = {
    refresh: refreshToken,
  };

  try {
    const res = await apiCalls.postRefresh({ payload });

    authActions.storeAuthTokens({
      accessToken: extractAccessToken(res),
    });
  } catch (err) {
    throw err;
  }

  return authActions.getAccessToken();
};

async function isAuthenticated() {
  /**
   * Returns true if authenticated, else false.
   *
   * Tries to get the access token and tries to refresh if expired.
   */

  let accessToken = authActions.getAccessToken();
  if (!accessToken) {
    authActions.clearAuthTokens();
    return false;
  }

  if (!authActions.isTokenExp(accessToken)) {
    return true;
  }

  accessToken = await refreshToken();

  if (!accessToken) {
    authActions.clearAuthTokens();
    return false;
  }

  return true;
}

/**
 * isAuthenticated is configured to return the same instance
 * of the promise for all concurrent callers.
 */
const appLogicAuth = {
  isAuthenticated: configureSharedPromise(isAuthenticated),
};

export default appLogicAuth;
