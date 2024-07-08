import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const queryTechKnowledge = async () => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not retrieve list of Tech Knowledge as the user was not authenticated."
    );
  }
  return await apiCalls.getTechKnowledge();
};
