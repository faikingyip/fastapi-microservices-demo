import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const queryTransaction = async ({id}) => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not retrieve transaction as the user was not authenticated."
    );
  }

  return await apiCalls.getTransaction({id});
};
