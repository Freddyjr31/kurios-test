import { useEffect, useState } from 'react';
import { getTeachers } from '../../api/teachers/teachersService';
import type { Teacher } from '../../api/teachers/types';

interface TeachersState {
  key: string;
  teachers: Teacher[];
  error: string | null;
}

export function useTeachers(schoolId: number | null, limit = 100) {
  const [state, setState] = useState<TeachersState | null>(null);
  const key = schoolId === null ? null : `${schoolId}:${limit}`;

  useEffect(() => {
    if (schoolId === null) return;

    let isMounted = true;

    getTeachers({ school_id: schoolId, limit })
      .then((result) => {
        if (isMounted) {
          setState({ key: `${schoolId}:${limit}`, teachers: result.teachers, error: null });
        }
      })
      .catch((err: unknown) => {
        if (isMounted) {
          setState({
            key: `${schoolId}:${limit}`,
            teachers: [],
            error: err instanceof Error ? err.message : 'Error al cargar los profesores',
          });
        }
      });

    return () => {
      isMounted = false;
    };
  }, [schoolId, limit]);

  const isCurrent = key !== null && state?.key === key;
  const teachers = isCurrent ? state.teachers : [];
  const loading = key !== null && !isCurrent;
  const error = isCurrent ? state.error : null;

  return { teachers, loading, error };
}
