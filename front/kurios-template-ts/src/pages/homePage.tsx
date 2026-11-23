import { BookOpen } from 'lucide-react';
import { useMemo, useState } from 'react';
import type { VisitType } from '../api/visits/types';
import { createVisit } from '../api/visits/visitsService';
import type { SelectOption } from '../components/ui/searchableSelect';
import { VisitForm } from '../components/visits/registerVisitForm';
import VisitsTable from '../components/visits/visitsTable';
import { useSchools } from '../hooks/schools/useSchools';
import { useTeachers } from '../hooks/teachers/useTeachers';
import { useVisitTypes } from '../hooks/visits/useVisitTypes';
import type { VisitFormValues } from '../schemas/visit.schema';

export default function HomePage() {
    
  const { schools, loading: loadingSchools, error: schoolsError } = useSchools();
  const [colegioId, setColegioId] = useState('');
  const schoolId = colegioId ? Number(colegioId) : null;
  const { teachers, loading: loadingTeachers, error: teachersError } = useTeachers(schoolId);
  const { types, loading: loadingTypes } = useVisitTypes();

  const [serverError, setServerError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);

  const colegios = useMemo<SelectOption[]>(
    () => schools.map((school) => ({ value: String(school.id), label: school.name })),
    [schools],
  );

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

  const tiposVisita = useMemo<SelectOption[]>(
    () => types.map((type) => ({ value: type, label: type })),
    [types],
  );

  const handleVisitSubmit = async (data: VisitFormValues): Promise<boolean> => {

    setServerError(null);

    try {

      await createVisit({
        id_school: Number(data.colegioId),
        id_teacher: Number(data.profesorId),
        date_visit: data.fecha,
        time_visit: data.hora,
        type_visit: data.tipoVisita as VisitType,
        notes: data.observaciones.trim() || null,
      });

      setRefreshKey((key) => key + 1);
      return true;
    } catch (err) {
      setServerError(
        err instanceof Error ? err.message : 'No se pudo registrar la visita',
      );
      return false;
    }
  };

  const dataError = schoolsError ?? teachersError;

  return (
    <div>

        
    {/* Contenedor principal del encabezado */}
    <div className="w-full px-3 sm:px-4 py-4">
        <div className="flex items-center justify-start gap-3">
            {/* Icono en recuadro redondeado */}
            <div className="w-11 h-11 rounded-xl bg-[#5b4ce8] flex items-center justify-center shrink-0 text-white">
                <BookOpen className="w-5 h-5 stroke-[1.8]" />
            </div>

            {/* Título y subtítulo */}
            <div className="min-w-0">
                <p className="text-4xl font-normal text-indigo-900 leading-tight truncate">
                    Kurios visits portal
                </p>
                <p className="text-xs text-slate-500 mt-0.5 truncate">
                    Portal de Gestión de Visitas de Kurios. Aquí puedes registrar y consultar visitas a colegios.
                </p>
            </div>
        </div>
    </div>
        
     
      <div className="flex flex-col md:flex-row gap-6">

        <main className="w-full md:w-1/3 bg-white p-6 rounded-lg shadow">
          {dataError && (
            <div
              role="alert"
              className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700"
            >
              {dataError}
            </div>
          )}

          <VisitForm
            colegios={colegios}
            profesores={profesores}
            tiposVisita={tiposVisita}
            onSubmitVisit={handleVisitSubmit}
            onColegioChange={(value) => {
              setColegioId(value);
              setServerError(null);
            }}
            onFormChange={() => setServerError(null)}
            loadingColegios={loadingSchools}
            loadingProfesores={loadingTeachers}
            loadingTipos={loadingTypes}
            serverError={serverError}
          />
        </main>

        <aside className="w-full md:w-2/3 bg-white p-6 rounded-lg shadow">
          {/* La key remonta la tabla al crear una visita: vuelve a la página 1 y recarga. */}
          <VisitsTable
            key={refreshKey}
            colegios={colegios}
            tiposVisita={tiposVisita}
          />
        </aside>

      </div>
    </div>
  );
}
