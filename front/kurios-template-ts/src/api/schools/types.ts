export interface School {
  id: number;
  name: string;
  address: string;
}

export interface SchoolsResponse {
  schools: School[];
  total: number;
  limit: number;
  offset: number;
}

export interface GetSchoolsParams {
  name?: string;
  limit?: number;
  offset?: number;
}
