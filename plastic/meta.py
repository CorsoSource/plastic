

from shared.data.plastic.connectors.base import PlasticORM_Connection_Base
from shared.data.plastic.column import PlasticColumn


from weakref import WeakSet



class MetaPlasticORM(type):
	"""Metaclass that allows new PlasticORM classes to autoconfigure themselves.

	When a new PlasticORM class is _created_ (not instantiated!), this will
	  be run. On __init__ the new PlasticORM class will first 
	"""
	def __new__(cls, clsname, bases, attributes): 
		# Placeholder.       
		return super(MetaPlasticORM,cls).__new__(cls, clsname, bases, attributes)
	
	
	def __init__(cls, clsname, bases, attributes):
		"""Initializes the basic attributes for the class itself.
		Auto-configuration is kicked off here.
		"""
		# Do a null setup for the base classes.
		# This allows Plastic to defer some of its configuration until the
		#   database specific classes are defined.
		if clsname.startswith('Plastic') or cls._connectionType==PlasticORM_Connection_Base:
			cls._table = ''

		# Derived classes get initialized, though.
		# Thus we can be sure to configure _before_ creating the derived classes
		else:
			# Critically, the connection definition is deferred until here
			if not cls._connection:
				cls._connection = cls._connectionType(cls._dbInfo)
			cls._table = cls._table or clsname
			cls._table = cls._table.lower()
			cls._verify_columns()
			
		cls._pending = None
		
		# each class gets its own group of instances, of course
		cls._instances = WeakSet()
		
		# grab the defaults set, if any
		column_defaults = getattr(cls, '_column_defaults', {})
		
		# remove since it's only for setup - use Table.column.default = new_value otherwise
		if hasattr(cls, '_column_defaults'):
			delattr(cls, '_column_defaults')
		
		# Add the column names themselves as convenience attributes.
		# These are of type PlasticColumn and allow some additional abstractions.
		# NOTE: columns are not validated! They are assumed to not include
		#   spaces or odd/illegal characters.
		for ix,column in enumerate(cls._columns):
			meta_column = PlasticColumn(cls, column)
			meta_column.default = column_defaults.get(column)
			setattr(cls, column, meta_column)

		# Continue and carry out the normal class definition process   
		return super(MetaPlasticORM,cls).__init__(clsname, bases, attributes)   
	
	def __iter__(cls):
		"""
		Returns all rows, unfiltered, from the table.
		"""
		with cls._connection as plasticDB:
			# Build the query string (as defined by the engine configured)
			recordsQuery = "select %s\nfrom %s" 
			recordsQuery %= (
				','.join(cls._columns),
				cls._fullyQualifiedTableName
				)
			if cls._primary_key_cols:
				recordsQuery += "\norder by %s"
				recordsQuery %= (','.join(cls._primary_key_cols),)
			
			records = plasticDB.query(recordsQuery)
		
		objects = []
		for record in records:
			initDict = record._asdict()
			initDict['bypass_validation'] = True
			objects.append(cls(**initDict))
		
		for object in objects:
			yield object

	@property
	def _fullyQualifiedTableName(self):
		"""Helper function for getting the table name"""
		if self._schema:
			return '%s.%s' % (self._schema, self._table,)
		else:
			return '%s' % (self._table,)

	def _verify_columns(cls):
		"""Auto-configure the class definition. 

		As instances are created, they all follow the schema that is retrieved,
		  so this only needs to be done once, so we perform it on class definition.
		"""
		# ensure the configuration is valid
		with cls._connection as plasticDB:
			if not plasticDB.tableExists(cls._schema, cls._table) and cls._auto_create_table:
				cls._createTable()
			
			assert plasticDB.tableExists(cls._schema, cls._table), "Table may not exist or %r.%r is ambiguous" % (cls._schema, cls._table,)
		
		# Auto-configure the key columns, if needed        
		if cls._autoconfigure or not (cls._primary_key_cols and cls._primary_key_auto):
			with cls._connection as plasticDB:
				# collect the PKs from the engine
				pkCols = plasticDB.primaryKeys(cls._schema, cls._table)
				if pkCols:
					cls._primary_key_cols, cls._primary_key_auto = zip(*(r._tuple for r in pkCols))
		
		# Auto-configure the columns, if needed
		if cls._autoconfigure or not cls._columns:
			with cls._connection as plasticDB:
				# collect the columns from the engine
				columns = plasticDB.columnConfig(cls._schema, cls._table)
				if columns:
					cls._columns, cls._not_nullable_cols = zip(*[r._tuple for r in columns])
					# change to column names
					cls._not_nullable_cols = tuple(col 
											   for col,nullable 
											   in zip(cls._columns, cls._not_nullable_cols)
											   if not nullable
											  )
					cls._values = [None]*len(cls._columns)
				else:
					cls._columns = tuple()
					cls._not_nullable_cols = tuple()
					cls._values = []
				
				# TODO: add column default configuration from database
				#       unless already set (don't override?)
				#cls._column_defaults = ...
