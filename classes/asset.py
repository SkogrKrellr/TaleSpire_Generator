from abc import abstractmethod, abstractproperty
from classes.quad import Quad

class Asset:

    @abstractmethod
    def __init__(
        self,
        object
    ) -> None:
        self.id = 0
        self.uuid = object["Id"]
        self.name = object["Name"]
        self.assetName =  object["Assets"][0]["LoaderData"]["AssetName"]
        self.position = Quad(
            object["Assets"][0]["Position"]["x"],
            object["Assets"][0]["Position"]["y"],
            object["Assets"][0]["Position"]["z"],
            0
        )
        self.rotation = Quad(
            object["Assets"][0]["Rotation"]["x"],
            object["Assets"][0]["Rotation"]["y"],
            object["Assets"][0]["Rotation"]["z"],
            object["Assets"][0]["Rotation"]["w"]
        )
        self.scale = Quad(
            object["Assets"][0]["Scale"]["x"],
            object["Assets"][0]["Scale"]["y"],
            object["Assets"][0]["Scale"]["z"],
            0
        )
        self.mCenter = Quad(
            object["ColliderBoundsBound"]["m_Center"]["x"],
            object["ColliderBoundsBound"]["m_Center"]["y"],
            object["ColliderBoundsBound"]["m_Center"]["z"],
            0
        )
        self.mExtent = Quad(
            object["ColliderBoundsBound"]["m_Extent"]["x"],
            object["ColliderBoundsBound"]["m_Extent"]["y"],
            object["ColliderBoundsBound"]["m_Extent"]["z"],
            0
        )

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

    def SqlValues() -> str:
        return f"""
            UUID,
            Name,
            AssetName,
            {Quad.SqlValues("Position")},
            {Quad.SqlValues("Rotation")},
            {Quad.SqlValues("Scale")},
            {Quad.SqlValues("mCenter")},
            {Quad.SqlValues("mExtent")}
        """.strip()

    def Sql(self, tableName) -> str:
        return f"""
            INSERT INTO {tableName} 
            ({Asset.SqlValues()})
            VALUES(
                "{self.uuid}", 
                "{self.name}", 
                "{self.assetName}", 
                {self.position.Sql()}, 
                {self.rotation.Sql()},
                {self.scale.Sql()},
                {self.mCenter.Sql()},
                {self.mExtent.Sql()}
            );
        """.strip()

    def tableCreationSql(tableName) -> str:
        return f"""
            CREATE TABLE {tableName} (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            UUID tinytext NOT NULL,
            Name tinytext NOT NULL,
            AssetName tinytext NOT NULL,
            {Quad.tableCreationSql("Position")},
            {Quad.tableCreationSql("Rotation")},
            {Quad.tableCreationSql("Scale")},
            {Quad.tableCreationSql("mCenter")},
            {Quad.tableCreationSql("mExtent")});
        """.strip()

    def dropTableSql(tableName) -> str:
        return f""" DROP TABLE IF EXISTS {tableName}; """.strip()