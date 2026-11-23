const API_BASE_URL = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '');

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

interface ValidationDetail {
  msg?: string;
  loc?: Array<string | number>;
}

function detailToMessage(detail: unknown): string | null {
  if (typeof detail === 'string') return detail;

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item: ValidationDetail) => item?.msg)
      .filter((msg): msg is string => Boolean(msg));

    if (messages.length > 0) return messages.join('. ');
  }

  return null;
}

async function errorMessageFrom(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json();

    if (body && typeof body === 'object' && 'detail' in body) {
      const message = detailToMessage((body as { detail: unknown }).detail);
      if (message) return message;
    }
  } catch {
    // El backend no devolvió JSON; se usa el mensaje por defecto.
  }

  return `Error ${response.status}: ${response.statusText}`;
}

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...init?.headers,
    },
  });

  if (!response.ok) {
    throw new ApiError(await errorMessageFrom(response), response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export function toQueryString(params: Record<string, string | number | undefined>): string {
  const search = new URLSearchParams();

  for (const [key, value] of Object.entries(params)) {
    if (value === undefined || value === '') continue;
    search.set(key, String(value));
  }

  const query = search.toString();
  return query ? `?${query}` : '';
}
