import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const mutateCreateTechKnowledge = async ({ payload }) => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not create Tech Knowledge as the user was not authenticated."
    );
  }
  return await apiCalls.postCreateTechKnowledge({ payload });
};
