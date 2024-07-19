import { backendUrls } from "./constants/backend-urls";

import api from "./utils/api";

const getTechs = async () => {
  return await api.get(backendUrls.TECHS);
};

const getTechKnowledge = async () => {
  return await api.get(backendUrls.TECH_KNOWLEDGE);
};

const getEmployerRep = async () => {
  return await api.get(backendUrls.EMPLOYER_REP);
};

const getEmployerVacancies = async () => {
  return await api.get(backendUrls.EMPLOYER_VACANCIES);
};

const getVacancy = async ({ id }) => {
  return await api.get(`${backendUrls.VACANCY}${id}/`);
};

const getTransaction = async ({ id }) => {
  return await api.get(`${backendUrls.TRANSACTION}${id}/`);
};
const postCreateUserMe = async ({ payload }) => {
  return await api.post(backendUrls.REGISTER, payload);
};

const postCreateTechKnowledge = async ({ payload }) => {
  return await api.post(backendUrls.CREATE_TECH_KNOWLEDGE, payload);
};

const postCreateTrans = async ({ payload }) => {
  return await api.post(backendUrls.CREATE_TRANS, payload);
};

const postCreateVacancy = async ({ payload }) => {
  return await api.post(backendUrls.CREATE_VACANCY, payload);
};

const patchEmployerRep = async ({ payload }) => {
  return await api.patch(backendUrls.PATCH_EMPLOYER_REP, payload);
};

const patchVacancy = async ({ id, payload }) => {
  return await api.patch(`${backendUrls.PATCH_VACANCY}${id}/`, payload);
};

const deleteTechKnowledge = async ({ id }) => {
  return await api.delete(`${backendUrls.DELETE_TECH_KNOWLEDGE}${id}/`);
};

const getAccount = async () => {
  return await api.get(backendUrls.ACCOUNT);
};


const postLogin = async ({ payload }) => {
  const params = new URLSearchParams();
  params.append("username", payload.email);
  params.append("password", payload.password);
  return await api.post(backendUrls.LOGIN, params, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  //   const response = await axios.post('/token', params, {
  //     headers: {
  //         'Content-Type': 'application/x-www-form-urlencoded'
  //     }
  // });
};

const postRefresh = async ({ payload }) => {
  return await api.post(backendUrls.REFRESH, payload);
};

const apiCalls = {
  getTechs,
  getTechKnowledge,
  getEmployerVacancies,
  getVacancy,
  getTransaction,
  getEmployerRep,
  postCreateUserMe,
  postCreateTechKnowledge,
  postCreateVacancy,
  patchEmployerRep,
  patchVacancy,
  deleteTechKnowledge,
  postLogin,
  postRefresh,
  getAccount,
  postCreateTrans,
};

export default apiCalls;
