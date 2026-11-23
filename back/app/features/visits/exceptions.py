class VisitsError(Exception):
    """
    Error de negocio del feature `visits`.

    Cada subclase define el código HTTP con el que la API debe responder.
    El caso de uso lanza estas excepciones y `main.py` las traduce a JSON,
    así la capa de negocio no conoce FastAPI.
    """

    status_code: int = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class VisitNotFoundError(VisitsError):
    status_code = 404


class SchoolNotFoundError(VisitsError):
    status_code = 404


class TeacherNotFoundError(VisitsError):
    status_code = 404


class VisitConflictError(VisitsError):
    status_code = 409


class VisitValidationError(VisitsError):
    status_code = 422
