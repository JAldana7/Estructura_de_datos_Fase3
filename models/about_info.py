# clase para la información del estudiante
class AboutInfo:
    # Constructor de la clase AboutInfo
    def __init__(self):
        self._course: str = "Data Structure - 301305"
        self._student: str = "Johan Aldana"
        self._group: str = "Group 301305-41"
        self._career: str = "UNAD | System Engineering | ECBTI"
        self._date: str = "September 24, 2026"

    # función para obtener la información del estudiante
    def get_info(self) -> str:
        return (
            f"Course: {self._course}\n"
            f"Student: {self._student}\n"
            f"Group: {self._group}\n"
            f"Career: {self._career}\n"
            f"Date: {self._date}"
        )