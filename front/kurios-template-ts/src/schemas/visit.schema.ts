import { z } from 'zod';

export const visitSchema = z
  .object({
    colegioId: z.string().min(1, 'Por favor, seleccionar un colegio'),
    profesorId: z.string().min(1, 'Por favor, seleccionar un profesor'),
    fecha: z
      .string()
      .min(1, 'La fecha es obligatoria')
      .refine((val) => !Number.isNaN(Date.parse(val)), 'Fecha inválida'),
    hora: z
      .string()
      .min(1, 'La hora es obligatoria')
      .regex(/^([01]\d|2[0-3]):([0-5]\d)$/, 'Formato de hora inválido (HH:MM)'),
    tipoVisita: z.string().min(1, 'Selecciona un tipo de visita válido'),
    observaciones: z
      .string()
      .trim()
      .min(10, 'Mínimo 10 caracteres para detallar la observación')
      .max(500, 'Máximo 500 caracteres permitidos'),
  })
  .refine(
    (data) => {
      if (!data.fecha || !data.hora) return true;

      const visitDate = new Date(`${data.fecha}T${data.hora}`);
      if (Number.isNaN(visitDate.getTime())) return true;

      return visitDate.getTime() <= Date.now();
    },
    {
      message: 'La fecha y hora no pueden ser futuras',
      path: ['fecha'],
    },
  );

export type VisitFormValues = z.infer<typeof visitSchema>;
