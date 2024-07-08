import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";

export const queryVacancy = async ({id}) => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not retrieve vacancy details as the user was not authenticated."
    );
  }

  return await apiCalls.getVacancy({id});
};
