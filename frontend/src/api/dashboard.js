import { request } from './client.js';

export const getDashboard = () => request('/dashboard');
export const getSectionPerformance = () => request('/dashboard/sections');
export const getTopicPerformance = () => request('/dashboard/topics');
