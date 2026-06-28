from database.DB_connect import DBConnect
from model.arco import Arco
from model.categoria import Categoria
from model.product import Product


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last


    @staticmethod
    def getCategorie():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct c.*
                    from categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(Categoria(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllNodes(id_cat):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct p.*
            from products p 
            where p.category_id =%s"""

        cursor.execute(query,(id_cat,))

        for row in cursor:
            results.append(Product(**row))

        cursor.close()
        conn.close()
        return results


    @staticmethod
    def getAllEdges(d_min,d_max,id_cat,idMap):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
        select t1.product_id as p1,t2.product_id as p2,t1.vendite  +t2.vendite as peso
        from(
        select p.product_id ,sum(oi.quantity) as vendite
        from orders o ,order_items oi ,products p 
        where o.order_id =oi.order_id and oi.product_id =p.product_id and o.order_date between %s
        and %s and p.category_id =%s
        group by p.product_id 
        )t1,
        (
        select p.product_id ,sum(oi.quantity) as vendite
        from orders o ,order_items oi ,products p 
        where o.order_id =oi.order_id and oi.product_id =p.product_id and o.order_date between %s 
        and %s and p.category_id =%s
        group by p.product_id ) t2
        where t1.vendite <=t2.vendite  and t1.product_id <>t2.product_id 
        group by t1.product_id ,t2.product_id
        """

        cursor.execute(query,(d_min,d_max,id_cat,d_min,d_max,id_cat))

        for row in cursor:
            results.append(Arco(idMap[row["p1"]],idMap[row["p2"]],row["peso"]))

        cursor.close()
        conn.close()
        return results


