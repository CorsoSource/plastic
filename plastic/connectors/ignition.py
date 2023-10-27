

from plastic.recordset import RecordSet
from plastic.connectors.base import PlasticORM_Connection_Base
from plastic.core import PlasticORM_Base


META_QUERIES = {
	'ignition': {},
}

ENGINES = [
	'base', 'mysql', 'postgres', 'sqlite'
]

def autopopulate_metaqueries(META_QUERIES=META_QUERIES, ENGINES=ENGINES):
	for engine in ENGINES:
		try:
			META_QUERIES.update(
				plastic.metaqueries.getDict()[engine].META_QUERIES
			)
		except Exception as error:
			raise error

autopopulate_metaqueries()




def isIgnition():
	try:
		_ = getattr(system, 'db')
		return True
	except:
		return False


def assert_can_read_db():
	try:
		assert system.util.getConnectionMode() >= 2, 'Change communication mode to at least Read mode!'
	except AssertionError:
		raise
	except:
		pass # only designers and vision clients have to worry about this

def assert_can_readwrite_db():
	try:
		assert system.util.getConnectionMode() == 3, 'Change communication mode to at Read/Write mode!'
	except AssertionError:
		raise
	except:
		pass # only designers and vision clients have to worry about this
	


class Ignition_Connector(PlasticORM_Connection_Base):
	__meta_queries__ = META_QUERIES
	
	_engine = None
	_param_token = '?'
	
	
	def __init__(self, dbName):
		self.dbName = dbName
		self._engine = system.db.getConnectionInfo(self.dbName).getValueAt(0,'DBType').lower()
		self.tx = None
		

	def __enter__(self):
		if self.tx == None:
			self.tx = system.db.beginTransaction(self.dbName, 8)
		return self
	

	def __exit__(self, *args):
		if self.tx:
			system.db.commitTransaction(self.tx)
			system.db.closeTransaction(self.tx)
			self.tx = None
			

	def _execute_query(self, query, values):
		assert_can_read_db()
		if self.tx:
			return RecordSet(initialData=system.db.runPrepQuery(query, values, self.dbName, self.tx))
		else:
			return RecordSet(initialData=system.db.runPrepQuery(query, values, self.dbName))
	

	def _execute_insert(self, insertQuery, insertValues):
		assert_can_readwrite_db()
		if self.tx:
			return system.db.runPrepUpdate(insertQuery, insertValues, self.dbName, self.tx, getKey=1)
		else:
			return system.db.runPrepUpdate(insertQuery, insertValues, self.dbName, getKey=1)


	def _execute_update(self, updateQuery, updateValues):
		assert_can_readwrite_db()
		if self.tx:
			system.db.runPrepUpdate(updateQuery, updateValues, self.dbName, self.tx, getKey=0)
		else:
			system.db.runPrepUpdate(updateQuery, updateValues, self.dbName, getKey=0)
	
	def _execute_create(self, createQuery):
		assert_can_readwrite_db()
		if self.tx:
			system.db.runUpdateQuery(createQuery, self.dbName, self.tx, getKey=0)
		else:
			system.db.runUpdateQuery(createQuery, self.dbName, getKey=0)


class PlasticIgnition(PlasticORM_Base):
	_connectionType = Ignition_Connector
	
	_dbInfo = None

	pass



def connect_table(db, schema, table, 
				  column_def=None, 
				  column_defaults=None,
				  autocommit=False, auto_create_table=False):
	return type(table, (PlasticIgnition,), {
			'_dbInfo': db,
			'_schema': schema,
			'_table': table,
			'_column_def': column_def or {},
			'_column_defaults': column_defaults or {},
			'_autocommit': autocommit,
			'_auto_create_table': auto_create_table,
		})
