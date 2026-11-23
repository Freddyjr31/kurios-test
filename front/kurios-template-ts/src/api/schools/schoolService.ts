import { apiRequest, toQueryString } from '../http';
import type { GetSchoolsParams, SchoolsResponse } from './types';

export async function getSchools({
  name,
  limit = 100,
  offset = 0,
}: GetSchoolsParams = {}): Promise<SchoolsResponse> {
  const search = name?.trim() ?? '';

  return apiRequest<SchoolsResponse>(
    `/schools${toQueryString({
      // El backend exige un mínimo de 2 caracteres para buscar por nombre.
      name: search.length >= 2 ? search : undefined,
      limit,
      offset,
    })}`,
  );
}
