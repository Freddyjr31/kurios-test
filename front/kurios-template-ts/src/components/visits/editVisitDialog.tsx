import { useMemo, useState } from 'react';
import { updateVisit } from '../../api/visits/visitsService';
import type { Visit, VisitType } from '../../api/visits/types';
import { useTeachers } from '../../hooks/teachers/useTeachers';
import type { VisitFormValues } from '../../schemas/visit.schema';
import type { SelectOption } from '../ui/searchableSelect';
import { VisitForm } from './registerVisitForm';

interface EditVisitDialogProps {
  visit: Visit;
  colegios: SelectOption[];
  tiposVisita: SelectOption[];
  onClose: () => void;
  onSaved: () => void;
}

export function EditVisitDialog({
  visit,
  colegios,
  tiposVisita,
  onClose,
  onSaved,
}: EditVisitDialogProps) {
  const [colegioId, setColegioId] = useState(
    visit.id_school ? String(visit.id_school) : '',
  );
  const schoolId = colegioId ? Number(colegioId) : null;
  const { teachers, loading: loadingProfesores } = useTeachers(schoolId);
  const [serverError, setServerError] = useState<string | null>(null);

  const profesores = useMemo<SelectOption[]>(
    () =>
      teachers.map((teacher) => ({
        value: String(teacher.id),
        label:
          [teacher.name, teacher.last_name].filter(Boolean).join(' ') ||
          `Profesor #${teacher.id}`,
      })),
    [teachers],
  );

  // Si el tipo actual ya no está en el catálogo, lo mostramos igualmente.
  const tipos = useMemo<SelectOption[]>(() => {
    const currentType = visit.type_visit;

    if (!currentType || tiposVisita.some((option) => option.value === currentType)) {
      return tiposVisita;
    }

    return [{ value: currentType, label: currentType }, ...tiposVisita];
  }, [tiposVisita, visit.type_visit]);

  const initialValues: VisitFormValues = {
    colegioId: visit.id_school ? String(visit.id_school) : '',
    profesorId: visit.id_teacher ? String(visit.id_teacher) : '',
    fecha: visit.date_visit ?? '',
    hora: visit.time_visit ? visit.time_visit.slice(0, 5) : '',
    tipoVisita: visit.type_visit ?? '',
    observaciones: visit.notes ?? '',
  };

  const handleSubmit = async (data: VisitFormValues): Promise<boolean> => {
    setServerError(null);

    try {
      await updateVisit(visit.id, {
        id_school: Number(data.colegioId),
        id_teacher: Number(data.profesorId),
        date_visit: data.fecha,
        time_visit: data.hora,
        type_visit: data.tipoVisita as VisitType,
        notes: data.observaciones.trim(),
      });

      onSaved();
      return true;
    } catch (err) {
      setServerError(
        err instanceof Error ? err.message : 'No se pudo actualizar la visita',
      );
      return false;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-slate-900/40 p-4 sm:items-center">
      <div
        role="dialog"
        aria-modal="true"
        aria-label="Editar visita"
        className="w-full max-w-lg rounded-xl bg-white shadow-xl"
      >
        <VisitForm
          key={visit.id}
          mode="edit"
          initialValues={initialValues}
          idPrefix="edit-visit-"
          colegios={colegios}
          profesores={profesores}
          tiposVisita={tipos}
          onSubmitVisit={handleSubmit}
          onColegioChange={setColegioId}
          onFormChange={() => setServerError(null)}
          onCancel={onClose}
          loadingProfesores={loadingProfesores}
          serverError={serverError}
        />
      </div>
    </div>
  );
}
