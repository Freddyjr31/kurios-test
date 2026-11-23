import { useCallback, useEffect, useState } from 'react';
import { getSchools } from '../../api/schools/schoolService';
import type { School } from '../../api/schools/types';

interface SchoolsState {
  key: string;
  schools: School[];
  error: string | null;
}

export function useSchools(limit = 100) {
  const [state, setState] = useState<SchoolsState | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
  const key = `${limit}:${reloadKey}`;

  useEffect(() => {
    let isMounted = true;

    getSchools({ limit })
      .then((result) => {
        if (isMounted) {
          setState({ key, schools: result.schools, error: null });
        }
      })
      .catch((err: unknown) => {
        if (isMounted) {
          setState({
            key,
            schools: [],
            error: err instanceof Error ? err.message : 'Error al cargar los colegios',
          });
        }
      });

    return () => {
      isMounted = false;
    };
  }, [key, limit]);

  const isCurrent = state?.key === key;
  const schools = isCurrent ? state.schools : [];
  const loading = !isCurrent;
  const error = isCurrent ? state.error : null;

  const reload = useCallback(() => setReloadKey((current) => current + 1), []);

  return { schools, loading, error, reload };
}
