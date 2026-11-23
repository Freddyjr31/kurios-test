import { ChevronLeft, ChevronRight, Loader2, Pencil, RefreshCw, Trash2 } from 'lucide-react';
import { useState } from 'react';
import { ApiError } from '../../api/http';
import type { Visit } from '../../api/visits/types';
import { deleteVisit } from '../../api/visits/visitsService';
import { useVisits } from '../../hooks/visits/useVisits';
import { ConfirmDialog } from '../ui/confirmDialog';
import type { SelectOption } from '../ui/searchableSelect';
import { EditVisitDialog } from './editVisitDialog';

const PAGE_SIZE = 10;

interface VisitsTableProps {
  colegios: SelectOption[];
  tiposVisita: SelectOption[];
}

function formatDate(value: string | null): string {
  if (!value) return '—';

  const [year, month, day] = value.split('-');
  if (!year || !month || !day) return value;

  return `${day}/${month}/${year}`;
}

function formatTime(value: string | null): string {
  if (!value) return '—';
  return value.slice(0, 5);
}

function schoolLabel(visit: Visit): string {
  if (visit.school_name) return visit.school_name;
  return visit.id_school ? `Colegio #${visit.id_school}` : '—';
}

function teacherLabel(visit: Visit): string {
  if (visit.teacher_name) return visit.teacher_name;
  return visit.id_teacher ? `Profesor #${visit.id_teacher}` : '—';
}

function typeBadgeClass(type: string | null): string {
  if (type === 'En Aula') return 'bg-indigo-50 text-indigo-700 border-indigo-200';
  if (type === 'Encuentro') return 'bg-emerald-50 text-emerald-700 border-emerald-200';
  return 'bg-slate-50 text-slate-600 border-slate-200';
}

export default function VisitsTable({ colegios, tiposVisita }: VisitsTableProps) {
  const [page, setPage] = useState(0);
  const offset = page * PAGE_SIZE;

  const { visits, total, loading, error, reload } = useVisits({
    limit: PAGE_SIZE,
    offset,
  });

  const [editingVisit, setEditingVisit] = useState<Visit | null>(null);
  const [visitToDelete, setVisitToDelete] = useState<Visit | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const firstItem = total === 0 ? 0 : offset + 1;
  const lastItem = Math.min(offset + PAGE_SIZE, total);
  const hasPrevious = page > 0;
  const hasNext = offset + PAGE_SIZE < total;

  const finishDelete = () => {
    const wasLastOnPage = visits.length === 1 && page > 0;

    setVisitToDelete(null);

    if (wasLastOnPage) {
      setPage((current) => Math.max(0, current - 1));
    } else {
      reload();
    }
  };

  const openDelete = (visit: Visit) => {
    setDeleteError(null);
    setVisitToDelete(visit);
  };

  const closeDelete = () => {
    if (deleting) return;
    setVisitToDelete(null);
    setDeleteError(null);
  };

  const confirmDelete = async () => {
    if (!visitToDelete) return;

    setDeleting(true);
    setDeleteError(null);

    try {
      await deleteVisit(visitToDelete.id);
      finishDelete();
    } catch (err) {
      if (err instanceof ApiError && err.status === 404) {
        // La visita ya no existe o estaba oculta: el resultado deseado ya se cumplió.
        finishDelete();
      } else {
        setDeleteError(
          err instanceof Error ? err.message : 'No se pudo eliminar la visita',
        );
      }
    } finally {
      setDeleting(false);
    }
  };

  return (
    <div className="w-full">
      <div className="flex items-center justify-between gap-3 border-b border-slate-100 pb-3">
        <div>
          <h2 className="text-base font-semibold text-slate-900">Visitas registradas</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            {total === 0 ? 'Sin registros' : `${total} visita${total === 1 ? '' : 's'} en total`}
          </p>
        </div>

        <button
          type="button"
          onClick={reload}
          disabled={loading}
          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 text-xs font-medium text-slate-600 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors cursor-pointer"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          Refrescar
        </button>
      </div>

      {error && (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700"
        >
          {error}
        </div>
      )}

      <div className="mt-3 overflow-x-auto">
        <table className="w-full min-w-[720px] border-collapse text-sm">
          <thead>
            <tr className="text-left text-[11px] uppercase tracking-wide text-slate-500 border-b border-slate-200">
              <th className="py-2 pr-3 font-semibold">Fecha</th>
              <th className="py-2 pr-3 font-semibold">Hora</th>
              <th className="py-2 pr-3 font-semibold">Colegio</th>
              <th className="py-2 pr-3 font-semibold">Profesor</th>
              <th className="py-2 pr-3 font-semibold">Tipo</th>
              <th className="py-2 font-semibold">Observaciones</th>
              <th className="py-2 pl-3 font-semibold text-right">Acciones</th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100">
            {loading && visits.length === 0 && (
              <tr>
                <td colSpan={7} className="py-10 text-center text-slate-500">
                  <span className="inline-flex items-center gap-2 text-xs">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Cargando visitas...
                  </span>
                </td>
              </tr>
            )}

            {!loading && visits.length === 0 && !error && (
              <tr>
                <td colSpan={7} className="py-10 text-center text-xs text-slate-500">
                  No hay visitas registradas todavía.
                </td>
              </tr>
            )}

            {visits.map((visit) => (
              <tr key={visit.id} className="align-top hover:bg-slate-50 transition-colors">
                <td className="py-2.5 pr-3 whitespace-nowrap text-slate-700">
                  {formatDate(visit.date_visit)}
                </td>
                <td className="py-2.5 pr-3 whitespace-nowrap text-slate-700">
                  {formatTime(visit.time_visit)}
                </td>
                <td className="py-2.5 pr-3 text-slate-700">{schoolLabel(visit)}</td>
                <td className="py-2.5 pr-3 text-slate-700">{teacherLabel(visit)}</td>
                <td className="py-2.5 pr-3 whitespace-nowrap">
                  <span
                    className={`inline-flex items-center rounded-full border px-2 py-0.5 text-[11px] font-medium ${typeBadgeClass(
                      visit.type_visit,
                    )}`}
                  >
                    {visit.type_visit ?? '—'}
                  </span>
                </td>
                <td className="py-2.5 text-slate-600 max-w-[220px]">
                  {visit.notes ? (
                    <span className="line-clamp-2" title={visit.notes}>
                      {visit.notes}
                    </span>
                  ) : (
                    <span className="text-slate-400">—</span>
                  )}
                </td>
                <td className="py-2.5 pl-3 text-right whitespace-nowrap">
                  <div className="flex items-center justify-end gap-1">
                    <button
                      type="button"
                      onClick={() => setEditingVisit(visit)}
                      aria-label={`Editar visita del ${formatDate(visit.date_visit)}`}
                      title="Editar"
                      className="p-1.5 rounded-md text-slate-500 hover:bg-indigo-50 hover:text-indigo-700 transition-colors cursor-pointer"
                    >
                      <Pencil className="w-3.5 h-3.5" />
                    </button>
                    <button
                      type="button"
                      onClick={() => openDelete(visit)}
                      aria-label={`Eliminar visita del ${formatDate(visit.date_visit)}`}
                      title="Eliminar"
                      className="p-1.5 rounded-md text-slate-500 hover:bg-red-50 hover:text-red-600 transition-colors cursor-pointer"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-center justify-between gap-3 border-t border-slate-100 pt-3">
        <p className="text-xs text-slate-500">
          {total === 0 ? 'Mostrando 0 de 0' : `Mostrando ${firstItem}–${lastItem} de ${total}`}
        </p>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={() => setPage((current) => Math.max(0, current - 1))}
            disabled={!hasPrevious || loading}
            className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-slate-600 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            Anterior
          </button>

          <span className="text-xs text-slate-500">
            Página {page + 1}
          </span>

          <button
            type="button"
            onClick={() => setPage((current) => current + 1)}
            disabled={!hasNext || loading}
            className="inline-flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-slate-600 border border-slate-300 rounded-lg hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors cursor-pointer"
          >
            Siguiente
            <ChevronRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {editingVisit && (
        <EditVisitDialog
          key={editingVisit.id}
          visit={editingVisit}
          colegios={colegios}
          tiposVisita={tiposVisita}
          onClose={() => setEditingVisit(null)}
          onSaved={() => {
            setEditingVisit(null);
            reload();
          }}
        />
      )}

      {visitToDelete && (
        <ConfirmDialog
          title="Eliminar visita"
          confirmLabel="Eliminar"
          loading={deleting}
          error={deleteError}
          onConfirm={confirmDelete}
          onCancel={closeDelete}
          description={
            <>
              Se ocultará la visita del{' '}
              <span className="font-medium text-slate-800">
                {formatDate(visitToDelete.date_visit)}
              </span>{' '}
              a las{' '}
              <span className="font-medium text-slate-800">
                {formatTime(visitToDelete.time_visit)}
              </span>{' '}
              de{' '}
              <span className="font-medium text-slate-800">
                {schoolLabel(visitToDelete)}
              </span>
              . Dejará de aparecer en el listado, pero el registro histórico se conserva.
            </>
          }
        />
      )}
    </div>
  );
}
