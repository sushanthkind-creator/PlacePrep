import { useEffect, useRef, useState } from 'react';
import { createCubeStage } from './cubeStage.js';

export default function CubeScene({ scramble, getState, reducedMotion }) {
  const mountRef = useRef(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let stage;
    try {
      stage = createCubeStage(mountRef.current, { scramble, getState, reducedMotion });
    } catch {
      setFailed(true);
      return undefined;
    }
    return () => stage.dispose();
  }, [scramble, getState, reducedMotion]);

  if (failed) {
    return (
      <div className="cube-fallback" role="note">
        The 3D cube can&apos;t be shown in this browser (WebGL is unavailable). Everything else works normally.
      </div>
    );
  }

  return <div ref={mountRef} className="cube-mount" />;
}
