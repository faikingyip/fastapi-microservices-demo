import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const mutatePatchEmployerRep = async ({ payload }) => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not patch employer rep as the user was not authenticated."
    );
  }
  return await apiCalls.patchEmployerRep({ payload });
};
