import appLogicAuth from "../app-logic/app-logic-auth";
import apiCalls from "../store-backend/api-calls";
import { backendUrls } from "../store-backend/constants/backend-urls";
import api from "../store-backend/utils/api";

export const mutateDeleteTechKnowledge = async ({ id }) => {
  const isAuth = await appLogicAuth.isAuthenticated();
  if (!isAuth) {
    throw new Error(
      "Could not delete Tech Knowledge as the user was not authenticated."
    );
  }
  return await apiCalls.deleteTechKnowledge({ id });
};
