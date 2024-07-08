import authActions from "../store-localstorage/auth-actions";

/**
 * This provider provides the functionality to retrieve the
 * access token, hiding the details of the module that
 * does the heavy lifting.
 */
export const getAccessTokenFn = authActions.getAccessToken