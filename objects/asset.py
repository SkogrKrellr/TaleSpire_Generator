import uuid as UUID
from objects.quad import Quad
from objects.config import config as Config
from converter.conversionManager import ConversionManager

TABLE_NAME = DATABASE_NAME = Config.get('tableName', 'assets')


class Asset:
    """
    Class for a generic Asset.

    Attributes:
        name (str): Display name for the asset
        string (str): If a custom asset, the encoded string goes here
        uuid (str): Unique Identifier for the asset
        assetName (str): Name with no whitespaces
        position (Quad): Quad for the position of the asset
        rotation (Quad):  Quad for the rotation of the asset
        scale (Quad):  Quad for scale of the asset
        mCenter (Quad):  Quad for the Mesh Center of the asset
        mExtent (Quad):  Quad for the Mesh Extents (from mCenter) of the asset
    """

    def __init__(
        self,
        object
    ):
        """
        The constructor for Asset class.

        A dictionary of properties is passed in. From this dictionary only 2
        atributes are mandotory:
            Name - Display name for an asset
            String - String that contains encoded asset data

        Everything else is generated automatically.

        Parameters:
            object (dict): A dictionary of atributes for the asset.
        """

        self.name = object["Name"]
        self.string = object["String"]

        keys = object.keys()

        if "UUID" in keys:
            self.uuid = object["UUID"]
        else:
            self.uuid = str(UUID.uuid4()).lower()

        if "AssetName" in keys:
            self.assetName = object["AssetName"]
        else:
            self.assetName = "_".join(object["Name"].split())

        self.position = Quad(
            object["Position"]["x"],
            object["Position"]["y"],
            object["Position"]["z"],
            object["Position"]["w"]
        ) if "Position" in keys else Quad(0, 0, 0, 0)

        self.rotation = Quad(
            object["Rotation"]["x"],
            object["Rotation"]["y"],
            object["Rotation"]["z"],
            object["Rotation"]["w"]
        ) if "Rotation" in keys else Quad(0, 0, 0, 0)

        self.scale = Quad(
            object["Scale"]["x"],
            object["Scale"]["y"],
            object["Scale"]["z"],
            object["Scale"]["w"]
        ) if "Scale" in keys else Quad(0, 0, 0, 0)

        self.mCenter = Quad(
            object["mCenter"]["x"],
            object["mCenter"]["y"],
            object["mCenter"]["z"],
            object["mCenter"]["w"]
        ) if "mCenter" in keys else Quad(0, 0, 0, 0)

        self.mExtent = Quad(
            object["mExtent"]["x"],
            object["mExtent"]["y"],
            object["mExtent"]["z"],
            object["mExtent"]["w"]
        ) if "mExtent" in keys else Quad(0, 0, 0, 0)

# Miscellaneous
    def __str__(self):
        """
        Function to convert the object to a string.

        Returns:
            str: object as a string.
        """

        output = f"""
        UUID: {self.uuid}
        Name: {self.name}
        Asset Name: {self.assetName}
        String: {self.string}
        Position:   {self.position}
        Rotation:   {self.rotation}
        Scale:      {self.scale}
        mCenter:    {self.mCenter}
        mExtent:    {self.mExtent}
        """.replace("    ", "").strip()

        return output

# SQL operations
    def SqlValues(self):
        """
        Function to convert the object to a SQL expression.

        Returns:
            str: An SQL expression for inserting values into a specific table.
        """

        output = f"""
        INSERT INTO {TABLE_NAME}
            VALUES(
                "{self.uuid}",
                "{self.__class__.__name__}",
                "{self.name}",
                "{self.assetName}",
                "{self.string}",
                {self.position.SqlValues()},
                {self.rotation.SqlValues()},
                {self.scale.SqlValues()},
                {self.mCenter.SqlValues()},
                {self.mExtent.SqlValues()}
        );""".replace("    ", "").strip()

        return output

    def SqlCreateTable() -> str:
        """
        Function to return an SQL expression for table creation.

        Returns:
            str: An SQL expression for creating table for Assets.
        """

        output = f"""
        CREATE TABLE {TABLE_NAME} (
        UUID tinytext PRIMARY KEY,
        Type tinytext NOT NULL,
        Name tinytext NOT NULL,
        AssetName tinytext NOT NULL,
        String text NULL,
        {Quad.SqlCreateTable("Position")},
        {Quad.SqlCreateTable("Rotation")},
        {Quad.SqlCreateTable("Scale")},
        {Quad.SqlCreateTable("mCenter")},
        {Quad.SqlCreateTable("mExtent")}
        );""".replace("    ", "").strip()

        return output

    def SqlDropTable():
        """
        Function to return an SQL expression for dropping asset table.

        Returns:
            str: An SQL expression for creating table for assets.
        """

        return f""" DROP TABLE IF EXISTS {TABLE_NAME}; """

    def SqlGetAsset(uuid):
        """
        Function to return an SQL expression for dropping asset table.

        Parameters:
            uuid (str): UUID of the asset to be fetched from database.

        Returns:
            str: An SQL expression for get asset from specific table.
        """

        return f""" SELECT * FROM {TABLE_NAME} WHERE UUID = '{uuid}'; """
