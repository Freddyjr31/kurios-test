import { useCallback, useEffect, useState } from 'react';
import { getVisits } from '../../api/visits/visitsService';
import type { Visit } from '../../api/visits/types';

interface UseVisitsOptions {
  schoolId?: number | null;
  typeVisit?: string;
  limit?: number;
  offset?: number;
}

interface VisitsState {
  key: string;
  visits: Visit[];
  total: number;
  error: string | null;
}

export function useVisits({
  schoolId = null,
  typeVisit,
  limit = 10,
  offset = 0,
}: UseVisitsOptions = {}) {
  const [state, setState] = useState<VisitsState | null>(null);
  const [reloadKey, setReloadKey] = useState(0);
  const key = `${schoolId}:${typeVisit ?? ''}:${limit}:${offset}:${reloadKey}`;

  useEffect(() => {
    let isMounted = true;

    getVisits({
      school_id: schoolId ?? undefined,
      type_visit: typeVisit,
      limit,
      offset,
    })
      .then((result) => {
        if (isMounted) {
          setState({ key, visits: result.visits, total: result.total, error: null });
        }
      })
      .catch((err: unknown) => {
        if (isMounted) {
          setState({
            key,
            visits: [],
            total: 0,
            error: err instanceof Error ? err.message : 'Error al cargar las visitas',
          });
        }
      });

    return () => {
      isMounted = false;
    };
  }, [key, schoolId, typeVisit, limit, offset]);

  const isCurrent = state?.key === key;
  const visits = isCurrent ? state.visits : [];
  const total = isCurrent ? state.total : 0;
  const loading = !isCurrent;
  const error = isCurrent ? state.error : null;

  const reload = useCallback(() => setReloadKey((current) => current + 1), []);

  return { visits, total, loading, error, reload };
}
