import string
from MySQLdb import (
    connect,
    OperationalError,
)


class MissingObjectError(Exception):
    pass


class NotUniqueObject(Exception):
    pass


class WrongArgumentsException(Exception):
    pass


class AvlanSQLDao:

    def _after_save_hook(self, an_object):
        id_name = self._get_id_name(an_object.__class__)
        if not an_object.__dict__[id_name]:
            an_object.__dict__[id_name] = self.__conn.insert_id()

    def __init__(self, host, port, username, password, database=None, keepalive=False, autocommit=False, logger=None):

        # self.__logger = logger

        self.__host = host
        self.__port = port
        self.__username = username
        self.__password = password
        self.__database = database
        self.__autocommit = autocommit
        self.__keepalive = keepalive

        if keepalive:
            self.__conn = self.__create_connection()

    def __create_connection(self):
        if self.__database is None:
            return connect(
                host=self.__host,
                port=self.__port,
                user=self.__username,
                passwd=self.__password,
            )
        else:
            return connect(
                host=self.__host,
                port=self.__port,
                user=self.__username,
                passwd=self.__password,
                db=self.__database,
            )

    def autocommit(function):
        def wrap(self, *args, **kwargs):
            return_value = function(self, *args, **kwargs)
            if self.__autocommit:
                self.commit()
            return return_value
        return wrap

    def keepalive(function):
        def wrap(self, *args, **kwargs):
            if not self.__keepalive:
                self.__conn = self.__create_connection()
                return_value = function(self, *args, **kwargs)
                self.__conn.close()
            else:
                return_value = function(self, *args, **kwargs)
            return return_value
        return wrap

    @keepalive
    @autocommit
    def raw_execute(self, sql_query):
        cursor = self.__conn.cursor()
        try:
            cursor.execute(sql_query)
        except OperationalError, msg:
            print "Command skipped: ", msg
        finally:
            cursor.close()

    @keepalive
    def list_sql(self, sql_query, clazz, arg_list=()):
            # self.__logger.log_list("list_sql()", arg_list)
            # self.__logger.log_sql(sql_query)

            cursor = self.__conn.cursor()
            cursor.execute(
                sql_query,
                arg_list,
            )
            result = []
            for row_data in cursor.fetchall():
                obj = clazz()
                self._update_object_from_cursor(
                    row_data,
                    cursor,
                    obj,
                )
                result.append(obj)
            cursor.close()

            return result

    @keepalive
    def list_where(self, where_clause, clazz, arg_list=()):

        # self.__logger.log_class("list_where()", clazz, arg_list)
        table_name = self._get_table_name(clazz)

        obj = clazz()

        sql_from = self._get_table_from(clazz)
        select = self._get_table_select_clause(obj)

        sql_query = "{0:s} FROM {1:s} T{2:s} WHERE {3:s}".format(
            select,
            table_name,
            sql_from,
            where_clause,
        )

        if select.lower().find("sum") >= 0 or select.lower().find("count") >= 0:
            group_by_list = []
            for name in obj.__dict__.keys():
                # attributes starting with "_" are virtual (do not exist in db)
                if name[0] != "_":
                    group_by_list.append("T." + name)
            sql_query += " GROUP BY %s" % (string.join(group_by_list, ", "))

        order_by = self._get_table_order_by(clazz)
        if order_by:
            sql_query += " ORDER BY " + order_by

        # self.__logger.log_sql(sql_query)

        cursor = self.__conn.cursor()
        cursor.execute(
            sql_query,
            arg_list,
        )
        result = []
        for row_data in cursor.fetchall():
            obj = clazz()
            self._update_object_from_cursor(
                row_data,
                cursor,
                obj,
            )
            result.append(obj)
        cursor.close()

        return result

    @keepalive
    def list(self, example_object, first_result=0, max_results=100000):

        # self.__logger.log("list()", example_object)
        clazz = example_object.__class__
        table_name = self._get_table_name(clazz)

        value_list = []
        name_list = []
        for name, value in example_object.__dict__.items():
            if value is not None:
                name_list.append(" AND T." + name + " = %s")
                value_list.append(value)

        sql_from = self._get_table_from(clazz)
        select = self._get_table_select_clause(example_object)

        if name_list:
            sql_query = "{0:s} FROM {1:s} T{2:s} WHERE TRUE {3:s}".format(
                select,
                table_name,
                sql_from,
                string.join(
                    name_list,
                    "",
                ),
            )
        else:
            sql_query = "{0:s} FROM {1:s} T{2:s}".format(
                select,
                table_name,
                sql_from,
            )

        if select.lower().find("sum(") >= 0 or select.lower().find("count(") >= 0:
            group_by_list = []
            for name, value in example_object.__dict__.items():
                # attributes starting with "_" are virtual (do not exist in db)
                if name[0] != "_":
                    group_by_list.append("T." + name)
            sql_query += " GROUP BY %s" % (string.join(group_by_list, ", "))

        order_by = self._get_table_order_by(clazz)
        if order_by:
            sql_query += " ORDER BY " + order_by

        sql_query += " LIMIT %d OFFSET %d" % (max_results, first_result)

        # self.__logger.log_sql(sql_query)

        cursor = self.__conn.cursor()
        cursor.execute(
            sql_query,
            value_list,
        )
        result = []
        for row_data in cursor.fetchall():
            obj = clazz()
            self._update_object_from_cursor(
                row_data,
                cursor,
                obj,
            )
            result.append(obj)
        cursor.close()

        return result

    @staticmethod
    def _update_object_from_cursor(row_data, cursor, obj):

        lower_to_attribute_name = {}
        for name in obj.__dict__.keys():
            lower_to_attribute_name[name.lower()] = name

        for n in range(0, len(row_data)):
            name = cursor.description[n][0].lower()
            value = row_data[n]
            if name in lower_to_attribute_name:
                obj.__dict__[lower_to_attribute_name[name]] = value

    @keepalive
    @autocommit
    def delete(self, example_object):

        # self.__logger.log("delete()", example_object)
        table_name = self._get_table_name(example_object.__class__)

        value_list = []
        name_list = []
        for name, value in example_object.__dict__.items():
            if value is not None:
                name_list.append(" AND " + name + " = %s")
                value_list.append(value)

        if name_list:
            sql_query = "DELETE FROM {0:s} WHERE TRUE {1:s}".format(table_name, string.join(name_list, " "))
        else:
            raise WrongArgumentsException("to delete all objects use delete_all(class)")

        # self.__logger.log_sql(sql_query)
        # self.__logger.log_update_sql(sql_query, value_list)

        c = self.__conn.cursor()
        c.execute(sql_query, value_list)
        c.close()

    @keepalive
    @autocommit
    def delete_all(self, clazz):

        # self.__logger.log_class("delete_all()", clazz, None)
        table_name = self._get_table_name(clazz)
        sql_query = "DELETE FROM {0:s}".format(table_name)

        # self.__logger.log_sql(sql_query)
        # self.__logger.log_update_sql(sql_query, ())

        c = self.__conn.cursor()
        c.execute(sql_query)
        c.close()

    @keepalive
    @autocommit
    def load(self, clazz, object_id):
        # Get one entry using unique key marked as "TABLE_ID"

        # self.__logger.log_class("load()", clazz, object_id)
        table_name = self._get_table_name(clazz)
        object_id_name = self._get_id_name(clazz)

        obj = clazz()

        select_clause = self._get_table_select_clause(obj)
        sql_query = "%s FROM %s T%s WHERE T.%s = %%s" % (
            select_clause,
            table_name,
            self._get_table_from(clazz),
            object_id_name,
        )

        if select_clause.lower().find("sum(") >= 0 or select_clause.lower().find("count(") >= 0:
            group_by_list = []
            for name in obj.__dict__.keys():
                # attributes starting with "_" are virtual (do not exist in db)
                if name[0] != "_":
                    group_by_list.append("T." + name)
            sql_query += " GROUP BY %s" % (string.join(group_by_list, ", "))

        # self.__logger.log_sql(sql_query)

        cursor = self.__conn.cursor()
        cursor.execute(
            sql_query,
            [object_id],
        )
        row_data = cursor.fetchone()
        if not row_data:
            raise MissingObjectError("not found: " + clazz.__name__ + "@" + str(object_id))
        self._update_object_from_cursor(
            row_data,
            cursor,
            obj,
        )
        cursor.close()

        return obj

    @keepalive
    @autocommit
    def update(self, an_object, ignore_none=True):

        # self.__logger.log("update()", an_object)
        table_name = self._get_table_name(an_object.__class__)
        id_name = self._get_id_name(an_object.__class__)
        assert an_object.__dict__[id_name], \
            "object must have id field set before update(): " \
            + an_object

        value_list = []
        name_list = []
        for name, value in an_object.__dict__.items():
            # attributes starting with "_" are virtual (do not exist in db)
            if name[0] != "_" and name != id_name:
                if (not ignore_none) or value is not None:
                    name_list.append(name + " = %s")
                    value_list.append(value)

        sql_query = "UPDATE {0:s} SET {1:s} WHERE {2:s} = %s".format(table_name,
                                                                     string.join(name_list, ","),
                                                                     id_name)
        value_list.append(an_object.__dict__[id_name])

        # self.__logger.log_sql(sql_query)
        # self.__logger.log_sql(repr(value_list))
        # self.__logger.log_update_sql(sql_query, value_list)

        c = self.__conn.cursor()
        c.execute(sql_query, value_list)
        c.close()

    @keepalive
    @autocommit
    def save(self, an_object, ignore_none=True):

        # self.__logger.log("save()", an_object)
        clazz = an_object.__class__
        table_name = self._get_table_name(clazz)
        id_name = self._get_id_name(clazz)

        value_list = []
        name_list = []
        percent_list = []
        for name, value in an_object.__dict__.items():
            # attributes starting with "_" are virtual (do not exist in db)
            if name[0] != "_" and (name != id_name or value):
                if (not ignore_none) or value is not None:
                    name_list.append(name)
                    percent_list.append("%s")
                    value_list.append(value)

        sql_query = "INSERT INTO {0:s}({1:s}) VALUES({2:s})".format(table_name,
                                                                    string.join(name_list, ","),
                                                                    string.join(percent_list, ","))

        # self.__logger.log_sql(sql_query)
        # self.__logger.log_update_sql(sql_query, value_list)

        c = self.__conn.cursor()
        c.execute(sql_query, value_list)
        c.close()

        if not an_object.__dict__[id_name]:
            an_object.__dict__[id_name] = self.__conn.insert_id()

    def commit(self):

        self.__conn.commit()

    def rollback(self):

        self.__conn.rollback()

    @staticmethod
    def _get_table_name(clazz):

        if "SQL_TABLE" in clazz.__dict__:
            return clazz.__dict__["SQL_TABLE"]
        else:
            return clazz.__name__

    @staticmethod
    def _get_id_name(clazz):

        if "TABLE_ID" in clazz.__dict__:
            return clazz.__dict__["TABLE_ID"]
        else:
            return "id"

    @staticmethod
    def _get_table_from(clazz):

        if "SQL_FROM" in clazz.__dict__:
            return " " + clazz.__dict__["SQL_FROM"]
        else:
            return ""

    @staticmethod
    def _get_table_order_by(clazz):

        if "SQL_ORDER_BY" in clazz.__dict__:
            return " " + clazz.__dict__["SQL_ORDER_BY"]
        else:
            return None

    @staticmethod
    def _get_table_select_clause(obj):

        clazz = obj.__class__

        names = []
        for name in obj.__dict__.keys():
            # attributes starting with "_" are virtual (do not exist in db)
            if name[0] != "_":
                names.append("T." + name)

        sql = "SELECT %s" % string.join(names, ", ")
        if "SQL_SELECT" in clazz.__dict__:
            sql += ", " + clazz.__dict__["SQL_SELECT"]

        return sql
