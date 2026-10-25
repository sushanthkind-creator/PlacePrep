import { Link } from 'react-router-dom';

/**
 * A section drawn as a cube face: one sticker per topic, filled in the section colour once completed.
 */
export default function StickerFace({ tone, topics, size = 'md', label }) {
  const done = topics.filter((t) => t.completed).length;
  return (
    <ul
      className={`sticker-face sticker-face--${size}`}
      data-tone={tone}
      aria-label={label || `${done} of ${topics.length} topics completed`}
    >
      {topics.map((topic) => (
        <li key={topic.slug}>
          <Link
            to={`/topics/${topic.slug}`}
            className={`sticker${topic.completed ? ' is-done' : ''}`}
            title={`${topic.name}${topic.completed ? ' (completed)' : ''}`}
            aria-label={`${topic.name}, ${topic.completed ? 'completed' : 'not completed yet'}`}
          />
        </li>
      ))}
    </ul>
  );
}
