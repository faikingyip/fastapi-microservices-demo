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

const getVacancy = async ({id}) => {
  return await api.get(`${backendUrls.VACANCY}${id}/`);
};
const postCreateUserMe = async ({ payload }) => {
  return await api.post(backendUrls.REGISTER, payload);
};

const postCreateTechKnowledge = async ({ payload }) => {
  return await api.post(backendUrls.CREATE_TECH_KNOWLEDGE, payload);
};

const postCreateVacancy = async ({ payload }) => {
  return await api.post(backendUrls.CREATE_VACANCY, payload);
};

const patchEmployerRep = async ({ payload }) => {
  return await api.patch(backendUrls.PATCH_EMPLOYER_REP, payload);
};

const patchVacancy = async ({id, payload }) => {
  return await api.patch(`${backendUrls.PATCH_VACANCY}${id}/`, payload);
};

const deleteTechKnowledge = async ({ id }) => {
  return await api.delete(`${backendUrls.DELETE_TECH_KNOWLEDGE}${id}/`);
};

const postLogin = async ({ payload }) => {
  return await api.post(backendUrls.LOGIN, payload);
};

const postRefresh = async ({ payload }) => {
  return await api.post(backendUrls.REFRESH, payload);
};

const apiCalls = {
  getTechs,
  getTechKnowledge,
  getEmployerVacancies,
  getVacancy,
  getEmployerRep,
  postCreateUserMe,
  postCreateTechKnowledge,
  postCreateVacancy,
  patchEmployerRep,
  patchVacancy,
  deleteTechKnowledge,
  postLogin,
  postRefresh,
};

export default apiCalls;
