import { request } from './client.js';

export function listTests(filters = {}) {
  const params = new URLSearchParams(Object.entries(filters).filter(([, v]) => v));
  const query = params.toString();
  return request(`/tests${query ? `?${query}` : ''}`);
}

export const getTest = (testId) => request(`/tests/${testId}`);
export const startAttempt = (testId, settings) => request(`/tests/${testId}/attempts`, { method: 'POST', body: settings });

export const getAttempt = (attemptId) => request(`/attempts/${attemptId}`);
export const saveAnswer = (attemptId, questionId, optionId) =>
  request(`/attempts/${attemptId}/answers`, { method: 'PUT', body: { question_id: questionId, option_id: optionId } });
export const submitAttempt = (attemptId, answers) =>
  request(`/attempts/${attemptId}/submit`, { method: 'POST', body: { answers } });
export const getResult = (attemptId) => request(`/attempts/${attemptId}/result`);
export const getHistory = (page = 1, perPage = 20) => request(`/attempts?page=${page}&per_page=${perPage}`);
