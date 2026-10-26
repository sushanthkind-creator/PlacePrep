import { useRef } from 'react';
import useTilt from '../utils/useTilt.js';

/** A container that tilts towards the cursor with a soft light, like the section cards. */
export default function TiltPanel({ as: Tag = 'section', className = '', tone, max = 4, children, ...rest }) {
  const ref = useRef(null);
  useTilt(ref, { max });
  return (
    <Tag ref={ref} className={`${className} tilt-card`.trim()} data-tilt data-tone={tone} {...rest}>
      {children}
    </Tag>
  );
}
