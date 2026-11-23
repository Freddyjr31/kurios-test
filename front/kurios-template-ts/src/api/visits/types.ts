export type VisitType = 'En Aula' | 'Encuentro';

export type VisitStatus = 'visible' | 'hide';

export interface VisitBase {
  id: number;
  id_school: number | null;
  id_teacher: number | null;
  date_visit: string | null;
  time_visit: string | null;
  notes: string | null;
  visit_status: VisitStatus | null;
  type_visit: VisitType | null;
  created_at: string;
  updated_at: string | null;
}

export interface Visit extends VisitBase {
  school_name: string | null;
  teacher_name: string | null;
}

export interface VisitsResponse {
  visits: Visit[];
  total: number;
  limit: number;
  offset: number;
}

export interface GetVisitsParams {
  school_id?: number;
  type_visit?: string;
  limit?: number;
  offset?: number;
}

export interface CreateVisitPayload {
  id_school: number;
  id_teacher: number;
  date_visit: string;
  time_visit: string;
  type_visit: VisitType;
  notes?: string | null;
}

export interface UpdateVisitPayload {
  id_school?: number;
  id_teacher?: number;
  date_visit?: string;
  time_visit?: string;
  type_visit?: VisitType;
  notes?: string | null;
}
