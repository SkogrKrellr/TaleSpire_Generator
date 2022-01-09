
class Quad:
    """
    Class for a Quad.

    Attributes:
        x (float): value for the X component
        y (float): value for the Y component
        z (float): value for the Z component
        w (float): value for the W component
    """

    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        w: float = 0.0
    ):
        """
        The constructor for Quad class.

        Parameters:
            x (float): value for the X component
            y (float): value for the Y component
            z (float): value for the Z component
            w (float): value for the W component
        """

        self.x = x
        self.y = y
        self.z = z
        self.w = w

# Miscellaneous
    def __str__(self):
        """
        Function to convert the object to a string.

        Returns:
            str: object as a string.
        """
        return f"x: {self.x} y: {self.y} z: {self.z} w: {self.w}"

    def __eq__(self, other):
        """
        Function for checking if 2 Quads are equal.

        Parameters:
            other (Quad): Other quad to compare against

        Returns:
            bool: The objects have equal values
        """
        return self.__dict__ == other.__dict__

# SQL operations
    def SqlValues(self):
        """
        Function to convert the object atribute values to a SQL expression.

        Returns:
            str: An  expression for inserting values.
        """

        return f"{self.x}, {self.y}, {self.z}, {self.w}"

    def SqlFieldNames(prefix=""):
        """
        Function to convert the objects atribute labels to a SQL expression by
        adding a prefix to it.

        Parameters:
            prefix (str): Prefix to put before labels

        Returns:
            str: An expression for inserting values.
        """

        return f"{prefix}_x, {prefix}_y, {prefix}_z, {prefix}_w"

    def SqlCreateFields(prefix=""):
        """
        Function to create table columns for Quad with a specific prefix.

        Parameters:
            prefix (str): Prefix to put before column names and types

        Returns:
            str: An expression for creating colums.
        """

        return f"""
        {prefix}_x FLOAT(24),
        {prefix}_y FLOAT(24),
        {prefix}_z FLOAT(24),
        {prefix}_w FLOAT(24)
        """.replace("    ", "").strip()
