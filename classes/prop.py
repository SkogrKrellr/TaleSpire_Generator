from classes.config import *
from classes.asset import Asset

class Prop(Asset):
    
    def __init__(self, object) -> None:
        Asset.__init__(self, object)

    def Sql(self) -> str:
        return super().Sql(config.get('tableName', 'props'))

    def tableCreationSql() -> str:
        return Asset.tableCreationSql(config.get('tableName', 'props'))

    def dropTableSql() -> str:
        return Asset.dropTableSql(config.get('tableName', 'props'))