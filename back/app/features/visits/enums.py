from enum import StrEnum


class VisitStatusEnum(StrEnum):
    """
    Estado lógico de una visita (columna `visit_status`).

    Una visita nunca se elimina físicamente: pasa de `visible` a `hide`.
    """

    VISIBLE = "visible"
    HIDE = "hide"


class TypeVisitEnum(StrEnum):
    """
    Tipos de visita disponibles (enum `type_visits_enum`).

    El front obtiene los valores vigentes desde `GET /visits/types`; este enum
    documenta los que la aplicación conoce hoy.
    """

    EN_AULA = "En Aula"
    ENCUENTRO = "Encuentro"
