import { request } from './client.js';

export const getSections = () => request('/sections');
export const getSection = (slug) => request(`/sections/${encodeURIComponent(slug)}`);
export const getTopic = (slug) => request(`/topics/${encodeURIComponent(slug)}`);
export const getExamples = (slug) => request(`/topics/${encodeURIComponent(slug)}/examples`);
export const setTopicCompleted = (slug, completed) =>
  request(`/topics/${encodeURIComponent(slug)}/progress`, { method: 'POST', body: { completed } });
export const getTopicProgress = () => request('/progress/topics');

export const getPractice = (slug) => request(`/topics/${encodeURIComponent(slug)}/practice`);
export const checkPracticeAnswer = (questionId, optionId) =>
  request('/practice/answers', { method: 'POST', body: { question_id: questionId, option_id: optionId } });
