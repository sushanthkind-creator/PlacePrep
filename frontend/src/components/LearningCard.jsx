import { useRef } from 'react';
import { Link } from 'react-router-dom';
import { formatPercent } from '../utils/formatting.js';
import { sectionPath } from '../utils/sections.js';
import useTilt from '../utils/useTilt.js';
import StickerFace from './StickerFace.jsx';

export default function LearningCard({ section }) {
  const ref = useRef(null);
  useTilt(ref);
  const path = sectionPath(section.slug);
  return (
    <article ref={ref} className="learning-card tilt-card" data-tone={section.slug} data-tilt>
      <header className="learning-card-head">
        <p className="eyebrow tone-text">{section.short_name}</p>
        <h3>
          <Link to={path}>{section.name}</Link>
        </h3>
      </header>
      <StickerFace tone={section.slug} topics={section.topics} label={`${section.short_name} topics`} />
      <dl className="learning-card-stats">
        <div>
          <dt>Topics done</dt>
          <dd>
            {section.topics_completed}/{section.topics_total}
          </dd>
        </div>
        <div>
          <dt>Practice</dt>
          <dd>
            {section.practice_attempted}/{section.practice_total}
          </dd>
        </div>
        <div>
          <dt>Test accuracy</dt>
          <dd>{section.test_questions ? formatPercent(section.test_percentage) : '—'}</dd>
        </div>
      </dl>
    </article>
  );
}
