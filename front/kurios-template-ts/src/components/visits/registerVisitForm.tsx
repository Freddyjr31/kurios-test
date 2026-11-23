import { zodResolver } from '@hookform/resolvers/zod';
import { Loader2, Save, Send } from 'lucide-react';
import React from 'react';
import { Controller, useForm } from 'react-hook-form';
import type { VisitFormValues } from '../../schemas/visit.schema';
import { visitSchema } from '../../schemas/visit.schema';
import type { SelectOption } from '../ui/searchableSelect';
import { SearchableSelect } from '../ui/searchableSelect';

type VisitFormMode = 'create' | 'edit';

interface VisitFormProps {
  colegios: SelectOption[];
  profesores: SelectOption[];
  tiposVisita: SelectOption[];
  onSubmitVisit: (data: VisitFormValues) => Promise<boolean> | boolean;
  onColegioChange?: (colegioId: string) => void;
  onFormChange?: () => void;
  onCancel?: () => void;
  mode?: VisitFormMode;
  initialValues?: VisitFormValues;
  idPrefix?: string;
  loadingColegios?: boolean;
  loadingProfesores?: boolean;
  loadingTipos?: boolean;
  serverError?: string | null;
}

export const VisitForm: React.FC<VisitFormProps> = ({
  colegios,
  profesores,
  tiposVisita,
  onSubmitVisit,
  onColegioChange,
  onFormChange,
  onCancel,
  mode = 'create',
  initialValues,
  idPrefix = '',
  loadingColegios = false,
  loadingProfesores = false,
  loadingTipos = false,
  serverError,
}) => {
  const isEdit = mode === 'edit';
  const {
    register,
    handleSubmit,
    control,
    watch,
    setValue,
    clearErrors,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<VisitFormValues>({
    resolver: zodResolver(visitSchema),
    defaultValues: initialValues ?? {
      colegioId: '',
      profesorId: '',
      fecha: '',
      hora: '',
      tipoVisita: '',
      observaciones: '',
    },
  });

  const observacionesValue = watch('observaciones') || '';
  const colegioId = watch('colegioId');

  const onSubmit = async (data: VisitFormValues) => {
    const saved = await onSubmitVisit(data);

    if (saved && !isEdit) {
      reset();
      onColegioChange?.('');
    }
  };

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      className="w-full rounded-xl p-5 space-y-4"
    >
      <div className="border-b border-slate-100 pb-3">
        <h2 className="text-base font-semibold text-slate-900">
          {isEdit ? 'Editar visita' : 'Registrar Visita'}
        </h2>
        <p className="text-xs text-slate-500 mt-0.5">
          {isEdit
            ? 'Modifica los datos de la visita y guarda los cambios.'
            : 'Completa los datos para agendar o reportar la actividad.'}
        </p>
      </div>

      {serverError && (
        <div
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-xs text-red-700"
        >
          {serverError}
        </div>
      )}

      {/* 1. Select con Search: Colegio */}
      <Controller
        name="colegioId"
        control={control}
        render={({ field }) => (
          <SearchableSelect
            label="Colegio"
            options={colegios}
            value={field.value}
            onChange={(value) => {
              field.onChange(value);
              setValue('profesorId', '', { shouldValidate: false });
              clearErrors('profesorId');
              onColegioChange?.(value);
              onFormChange?.();
            }}
            placeholder={loadingColegios ? 'Cargando colegios...' : 'Selecciona un colegio'}
            searchPlaceholder="Buscar institución..."
            error={errors.colegioId?.message}
            disabled={loadingColegios}
          />
        )}
      />

      {/* 2. Select con Search: Profesor (depende del colegio) */}
      <Controller
        name="profesorId"
        control={control}
        render={({ field }) => (
          <SearchableSelect
            label="Profesor"
            options={profesores}
            value={field.value}
            onChange={(value) => {
              field.onChange(value);
              onFormChange?.();
            }}
            placeholder={
              !colegioId
                ? 'Selecciona primero un colegio'
                : loadingProfesores
                  ? 'Cargando profesores...'
                  : 'Selecciona un profesor'
            }
            searchPlaceholder="Buscar docente..."
            error={errors.profesorId?.message}
            disabled={!colegioId || loadingProfesores}
          />
        )}
      />

      {/* 3. Fecha y Hora uno al lado del otro */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        <div>
          <label
            htmlFor={`${idPrefix}fecha`}
            className="block text-xs font-medium text-slate-700 mb-1.5"
          >
            Fecha
          </label>
          <input
            id={`${idPrefix}fecha`}
            type="date"
            {...register('fecha', { onChange: onFormChange })}
            className={`w-full px-3 py-2 text-sm rounded-lg border bg-white text-slate-900 focus:outline-none focus:ring-2 transition-colors ${
              errors.fecha
                ? 'border-red-500 focus:ring-red-500/20'
                : 'border-slate-300 hover:border-slate-400 focus:border-indigo-600 focus:ring-indigo-600/20'
            }`}
          />
          {errors.fecha && <p className="mt-1 text-xs text-red-600">{errors.fecha.message}</p>}
        </div>

        <div>
          <label
            htmlFor={`${idPrefix}hora`}
            className="block text-xs font-medium text-slate-700 mb-1.5"
          >
            Hora
          </label>
          <input
            id={`${idPrefix}hora`}
            type="time"
            {...register('hora', { onChange: onFormChange })}
            className={`w-full px-3 py-2 text-sm rounded-lg border bg-white text-slate-900 focus:outline-none focus:ring-2 transition-colors ${
              errors.hora
                ? 'border-red-500 focus:ring-red-500/20'
                : 'border-slate-300 hover:border-slate-400 focus:border-indigo-600 focus:ring-indigo-600/20'
            }`}
          />
          {errors.hora && <p className="mt-1 text-xs text-red-600">{errors.hora.message}</p>}
        </div>
      </div>

      {/* 4. Select sin Search: Tipo de visita (dinámico desde la API) */}
      <div>
        <label
          htmlFor={`${idPrefix}tipoVisita`}
          className="block text-xs font-medium text-slate-700 mb-1.5"
        >
          Tipo de visita
        </label>
        <select
          id={`${idPrefix}tipoVisita`}
          {...register('tipoVisita', { onChange: onFormChange })}
          disabled={loadingTipos}
          className={`w-full px-3 py-2 text-sm rounded-lg border bg-white text-slate-900 focus:outline-none focus:ring-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed ${
            errors.tipoVisita
              ? 'border-red-500 focus:ring-red-500/20'
              : 'border-slate-300 hover:border-slate-400 focus:border-indigo-600 focus:ring-indigo-600/20'
          }`}
        >
          <option value="" disabled className="text-slate-400">
            {loadingTipos ? 'Cargando tipos...' : 'Selecciona el tipo...'}
          </option>
          {tiposVisita.map((type) => (
            <option key={type.value} value={type.value} className="bg-white text-slate-900">
              {type.label}
            </option>
          ))}
        </select>
        {errors.tipoVisita && (
          <p className="mt-1 text-xs text-red-600">{errors.tipoVisita.message}</p>
        )}
      </div>

      {/* 5. Input / Textarea para comentarios y observaciones */}
      <div>
        <div className="flex items-center justify-between mb-1.5">
          <label
            htmlFor={`${idPrefix}observaciones`}
            className="text-xs font-medium text-slate-700"
          >
            Comentarios y observaciones
          </label>
          <span className="text-[11px] text-slate-400">
            {observacionesValue.length}/500
          </span>
        </div>
        <textarea
          id={`${idPrefix}observaciones`}
          rows={3}
          placeholder="Escribe los detalles relevantes de la visita..."
          {...register('observaciones', { onChange: onFormChange })}
          className={`w-full px-3 py-2 text-sm rounded-lg border bg-white text-slate-900 placeholder-slate-400 resize-none focus:outline-none focus:ring-2 transition-colors ${
            errors.observaciones
              ? 'border-red-500 focus:ring-red-500/20'
              : 'border-slate-300 hover:border-slate-400 focus:border-indigo-600 focus:ring-indigo-600/20'
          }`}
        />
        {errors.observaciones && (
          <p className="mt-1 text-xs text-red-600">{errors.observaciones.message}</p>
        )}
      </div>

      {/* 6. Botones de acción */}
      <div className="flex items-center gap-2">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="flex-1 px-4 py-2.5 text-sm font-medium text-slate-700 border border-slate-300 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors cursor-pointer"
          >
            Cancelar
          </button>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed rounded-lg transition-colors cursor-pointer"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>{isEdit ? 'Guardando...' : 'Subiendo...'}</span>
            </>
          ) : (
            <>
              {isEdit ? <Save className="w-4 h-4" /> : <Send className="w-4 h-4" />}
              <span>{isEdit ? 'Guardar cambios' : 'Subir registro'}</span>
            </>
          )}
        </button>
      </div>
    </form>
  );
};
