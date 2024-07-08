import apiCalls from "../store-backend/api-calls";

export const mutateLogin = async ({ payload }) => {
  return await apiCalls.postLogin({ payload });
};
