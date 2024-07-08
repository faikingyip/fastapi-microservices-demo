import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const queryEmployerRep = async () => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not retrieve employer rep details as the user was not authenticated."
    );
  }

  return await apiCalls.getEmployerRep();
};
