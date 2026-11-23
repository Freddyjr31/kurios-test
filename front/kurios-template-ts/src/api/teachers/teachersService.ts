import { apiRequest, toQueryString } from '../http';
import type { GetTeachersParams, TeachersResponse } from './types';

export async function getTeachers({
  school_id,
  name,
  limit = 100,
  offset = 0,
}: GetTeachersParams): Promise<TeachersResponse> {
  const search = name?.trim() ?? '';

  return apiRequest<TeachersResponse>(
    `/teachers${toQueryString({
      school_id,
      // El backend exige un mínimo de 2 caracteres para buscar por nombre.
      name: search.length >= 2 ? search : undefined,
      limit,
      offset,
    })}`,
  );
}
