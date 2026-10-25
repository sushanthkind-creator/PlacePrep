import { useCallback, useEffect, useState } from 'react';

/** Runs an async loader when `deps` change and tracks loading / error / data. */
export default function useAsync(loader, deps) {
  const [state, setState] = useState({ status: 'loading', data: null, error: null });
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let active = true;
    setState((s) => ({ ...s, status: 'loading', error: null }));
    loader()
      .then((data) => active && setState({ status: 'success', data, error: null }))
      .catch((error) => active && setState({ status: 'error', data: null, error }));
    return () => {
      active = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, attempt]);

  const reload = useCallback(() => setAttempt((n) => n + 1), []);
  const setData = useCallback(
    (updater) => setState((s) => ({ ...s, data: typeof updater === 'function' ? updater(s.data) : updater })),
    [],
  );

  return { ...state, reload, setData };
}
