import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const mutateCreateVacancy = async ({ payload }) => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not create vacancy as the user was not authenticated."
    );
  }
  return await apiCalls.postCreateVacancy({ payload });
};
