import apiCalls from "../store-backend/api-calls";

export const mutateCreateTrans = async ({ payload }) => {
  return await apiCalls.postCreateTrans({ payload });
};
