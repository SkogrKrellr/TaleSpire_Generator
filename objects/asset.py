import uuid as UUID
from objects.quad import Quad
from objects.config import config as Config
from converter.conversionManager import ConversionManager

TABLE_NAME = DATABASE_NAME = Config.get('tableName', 'assets')

class Asset:

    def __init__(
        self,
        object
        ):

        self.name = object["Name"]
        self.string = object["String"]
        
        keys = object.keys()

        self.uuid = object["UUID"] if "UUID" in keys else str(UUID.uuid4()).lower()
        self.assetName =  object["AssetName"] if "AssetName" in keys else "_".join(object["Name"].split())

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
    def __str__(self) -> str:
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
        """.strip()

        return output

# SQL operations
    def SqlValues(self) -> str:
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
        );""".strip()

        return output
    
    def SqlCreateTable() -> str:
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
        );""".strip()

        return output
    
    def SqlDropTable() -> str:
        return f""" DROP TABLE IF EXISTS {TABLE_NAME}; """
    
    def SqlGetAsset(uuid) -> str:
        return f""" SELECT * FROM {TABLE_NAME} WHERE UUID = '{uuid}'; """
