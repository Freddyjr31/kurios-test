import { useEffect, useState } from 'react';
import { getVisitTypes } from '../../api/visits/visitsService';
import type { VisitType } from '../../api/visits/types';

interface VisitTypesState {
  types: VisitType[];
  error: string | null;
}

export function useVisitTypes() {
  const [state, setState] = useState<VisitTypesState | null>(null);

  useEffect(() => {
    let isMounted = true;

    getVisitTypes()
      .then((result) => {
        if (isMounted) {
          setState({ types: result, error: null });
        }
      })
      .catch((err: unknown) => {
        if (isMounted) {
          setState({
            types: [],
            error: err instanceof Error ? err.message : 'Error al cargar los tipos de visita',
          });
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return {
    types: state?.types ?? [],
    loading: state === null,
    error: state?.error ?? null,
  };
}
