class AboutInfo:
    def __init__(self):
        self.course: str = "Data Structure - 301305"
        self.student: str = "Johan Aldana"
        self.group: str = "Group 301305-41"
        self.career: str = "UNAD | System Engineering | ECBTI"
        self.date: str = "September 24, 2026"

    def get_info(self) -> str:
        return (
            f"Course: {self.course}\n"
            f"Student: {self.student}\n"
            f"Group: {self.group}\n"
            f"Career: {self.career}\n"
            f"Date: {self.date}"
        )