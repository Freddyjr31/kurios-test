export interface Teacher {
  id: number;
  name: string | null;
  last_name: string | null;
  id_school: number;
}

export interface TeachersResponse {
  teachers: Teacher[];
  total: number;
  limit: number;
  offset: number;
}

export interface GetTeachersParams {
  school_id: number;
  name?: string;
  limit?: number;
  offset?: number;
}
