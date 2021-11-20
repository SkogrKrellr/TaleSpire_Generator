from abc import abstractclassmethod, abstractmethod, abstractproperty
from classes.quad import Quad
from classes.config import config as Config

TABLE_NAME = DATABASE_NAME = Config.get('tableName', 'assets')

class Asset:

    @abstractmethod
    def __init__(
        self,
        object
        ):
        self.uuid = object["UUID"]
        self.name = object["Name"]
        self.assetName =  object["AssetName"]
        self.position = Quad(
            object["Position"]["x"],
            object["Position"]["y"],
            object["Position"]["z"],
            object["Position"]["w"]
        )
        self.rotation = Quad(
            object["Rotation"]["x"],
            object["Rotation"]["y"],
            object["Rotation"]["z"],
            object["Rotation"]["w"]
        )
        self.scale = Quad(
            object["Scale"]["x"],
            object["Scale"]["y"],
            object["Scale"]["z"],
            object["Scale"]["w"]
        )
        self.mCenter = Quad(
            object["mCenter"]["x"],
            object["mCenter"]["y"],
            object["mCenter"]["z"],
            object["mCenter"]["w"]
        )
        self.mExtent = Quad(
            object["mExtent"]["x"],
            object["mExtent"]["y"],
            object["mExtent"]["z"],
            object["mExtent"]["w"]
        )

# Miscellaneous

    def __str__(self) -> str:
        return f"""
            UUID: {self.uuid}
            Name: {self.name}
            Asset Name: {self.assetName}
            Position:   {self.position}
            Rotation:   {self.rotation}
            Scale:      {self.scale}
            mCenter:    {self.mCenter}
            mExtent:    {self.mExtent}
        """.strip()

# SQL operations
    def SqlValues(self) -> str:
        return f"""
            INSERT INTO {TABLE_NAME} 
            VALUES(
                "{self.uuid}",
                "{self.__class__.__name__}", 
                "{self.name}", 
                "{self.assetName}", 
                {self.position.SqlValues()}, 
                {self.rotation.SqlValues()},
                {self.scale.SqlValues()},
                {self.mCenter.SqlValues()},
                {self.mExtent.SqlValues()}
            );
        """.strip()
    
    def SqlCreateTable() -> str:
        return f"""
            CREATE TABLE {TABLE_NAME} (
            UUID tinytext PRIMARY KEY,
            Type tinytext NOT NULL,
            Name tinytext NOT NULL,
            AssetName tinytext NOT NULL,
            {Quad.SqlCreateTable("Position")},
            {Quad.SqlCreateTable("Rotation")},
            {Quad.SqlCreateTable("Scale")},
            {Quad.SqlCreateTable("mCenter")},
            {Quad.SqlCreateTable("mExtent")});
        """.strip()
    
    def SqlDropTable() -> str:
        return f""" DROP TABLE IF EXISTS {TABLE_NAME}; """.strip()
    
    def SqlGetAsset(uuid) -> str:
        return f""" SELECT * FROM {TABLE_NAME} WHERE UUID = '{uuid}'; """.strip()