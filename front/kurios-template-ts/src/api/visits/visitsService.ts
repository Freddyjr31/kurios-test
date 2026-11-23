import { apiRequest, toQueryString } from '../http';
import type {
  CreateVisitPayload,
  GetVisitsParams,
  UpdateVisitPayload,
  VisitBase,
  VisitsResponse,
  VisitType,
} from './types';

export async function getVisits({
  school_id,
  type_visit,
  limit = 10,
  offset = 0,
}: GetVisitsParams = {}): Promise<VisitsResponse> {
  return apiRequest<VisitsResponse>(
    `/visits${toQueryString({
      school_id,
      type_visit,
      limit,
      offset,
    })}`,
  );
}

export async function getVisitTypes(): Promise<VisitType[]> {
  return apiRequest<VisitType[]>('/visits/types');
}

export async function createVisit(payload: CreateVisitPayload): Promise<VisitBase> {
  return apiRequest<VisitBase>('/visits', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function updateVisit(
  visitId: number,
  payload: UpdateVisitPayload,
): Promise<VisitBase> {
  return apiRequest<VisitBase>(`/visits/${visitId}`, {
    method: 'PATCH',
    body: JSON.stringify(payload),
  });
}

export async function deleteVisit(visitId: number): Promise<void> {
  return apiRequest<void>(`/visits/${visitId}`, {
    method: 'DELETE',
  });
}
