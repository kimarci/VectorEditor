class ToolManager:
    """
    Управляет инструментами

    :cvar TOOLS: список кортежей
    :ivar current_tool: текущий выбранный инструмент
    """

    TOOLS = [
        ("select", "Выбрать"),
        ("brush", "Кисть"),
        ("rectangle", "Прямоугольник"),
        ("ellipse", "Овал"),
        ("parallelogram", "Параллелограмм"),
        ("triangle", "Треугольник"),
        ("rhombus", "Ромб"),
        ("fill", "Заливка"),
    ]

    def __init__(self):
        """
        Создаёт менеджер инструментов

        По умолчанию выбирается инструмент "select".
        """
        self.current_tool = "select"

    def get_readable_name(self, internal_name):
        """
        Поиск читаемого названия по внутреннему имени

        :param internal_name: внутреннее имя инструмента
        :return: читаемое название
        """
        for internal, readable in self.TOOLS:
            if internal == internal_name:
                return readable
        return internal_name

    def set_tool(self, tool):
        """
        Устанавливает текущий инструмент

        :param tool: внутреннее имя инструмента
        """
        self.current_tool = tool