import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const mutatePatchVacancy = async ({id, payload }) => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not patch vacancy as the user was not authenticated."
    );
  }
  return await apiCalls.patchVacancy({id, payload });
};
