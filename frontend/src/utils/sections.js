// Frontend routes for the three learning sections. Names and colours come from the API.
export const SECTION_PATHS = {
  logical: '/learn/logical',
  quant: '/learn/quant',
  verbal: '/learn/english',
};

export const SECTION_ORDER = ['logical', 'quant', 'verbal'];

export function sectionPath(slug) {
  return SECTION_PATHS[slug] || '/dashboard';
}

export function topicStatus(topic) {
  if (topic.completed) return { label: 'Completed', tone: 'done' };
  if (topic.practice?.attempted || topic.tests?.total) return { label: 'In progress', tone: 'progress' };
  return { label: 'Not started', tone: 'idle' };
}
