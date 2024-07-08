import apiCalls from "../store-backend/api-calls";

export const mutateCreateMe = async ({ payload }) => {
  return await apiCalls.postCreateUserMe({ payload });
};
