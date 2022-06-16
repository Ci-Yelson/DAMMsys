#### 0.触发器测试

```sql
# Postgresql 触发器语法：
CREATE [ CONSTRAINT ] TRIGGER name 
{ BEFORE | AFTER | INSTEAD OF } { event [ OR ... ]}
ON table_name
[ FROM referenced_table_name ]
{ NOT DEFERRABLE | [ DEFEREABLE ] { IINITIALLY IMMEDIATE | INITIALLY DEFERED} }
FOR [ EACH ] { ROW | STATEMENT }
[ WHEN { condition }]
EXECUTE PROCEDURE function_name ( arguments )
```

```sql
# 先定义函数
CREATE OR REPLEASE FUNCTION tfunc()
returns trigger as $$
begin
    UPDATE test2 as a 
    SET a.count = b.count + 1
    from test2 as b
    where a.id = b.id and a.id = 1;
    return old;
end;
$$
language plpgsql;

# 创建触发器
CREATE TRIGGER example_trigger AFTER INSERT 
ON test1 
FOR EACH ROW 
EXECUTE PROCEDURE tfunc();
```





#### 1.客户——add_order()，提交维修委托后更新车辆状态【“空闲”->“正在维修”】。

```sql
# 定义函数
CREATE OR REPLACE FUNCTION "my_root"."add_order_tfunc"()
  RETURNS "pg_catalog"."trigger" AS $BODY$BEGIN
	-- Routine body goes here...
	UPDATE dammapp_customercar as a 
	SET a.status = 2
	where a.vin = NEW.vin_id;
	RETURN NEW;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  
# 创建触发器
CREATE TRIGGER add_order_trigger AFTER INSERT 
ON dammapp_maintenanceorder 
FOR EACH ROW 
EXECUTE PROCEDURE add_order_tfunc();
```



#### 2.业务员——finish_order()，完成委托后更新车辆状态【“正在维修”->“空闲”】。

```sql
# 定义函数
CREATE OR REPLACE FUNCTION "my_root"."finish_order_tfunc"()
  RETURNS "pg_catalog"."trigger" AS $BODY$BEGIN
	-- Routine body goes here...
	UPDATE dammapp_customercar as a 
	SET a.status = 1
	where a.vin = NEW.vin_id;
	RETURN NEW;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  
# 创建触发器
CREATE TRIGGER finish_order_trigger AFTER UPDATE 
ON dammapp_maintenanceorder 
FOR EACH ROW 
WHEN ((OLD.status<>3) and (NEW.status=3))
EXECUTE PROCEDURE finish_order_tfunc();
```



#### 3.维修员——start_workorder()，开始维修后更新维修员状态【“空闲”->“工作中”】。

```sql
# 定义函数
CREATE OR REPLACE FUNCTION "my_root"."start_workorder_tfunc"()
  RETURNS "pg_catalog"."trigger" AS $BODY$BEGIN
	-- Routine body goes here...
	UPDATE dammapp_maintenanceman as a 
	SET a.status = 2
	where a.mid = NEW.mid_id;
	RETURN NEW;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  
# 创建触发器
CREATE TRIGGER start_workorder_trigger AFTER UPDATE 
ON dammapp_maintenanceworkorder 
FOR EACH ROW 
WHEN ((OLD.status<>2) and (NEW.status=2))
EXECUTE PROCEDURE start_workorder_tfunc();
```



#### 4.维修员——finish_workorder()，完成派工单后更新委托单费用【“总费用”累加】和维修员状态【“工作中”->“空闲”】。

1. 更新委托单费用

```sql
# 定义函数
CREATE OR REPLACE FUNCTION "my_root"."finish_workorder_tfunc1"()
  RETURNS "pg_catalog"."trigger" AS $BODY$BEGIN
	-- Routine body goes here...
	UPDATE dammapp_maintenanceorder as a 
	SET a."cost" = a."cost" + NEW."totalPartsCost" + NEW."artificialCost"
	where a."orderId" = NEW."orderId_id";
	RETURN NEW;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  
# 创建触发器
CREATE TRIGGER finish_workorder_trigger1 AFTER UPDATE 
ON dammapp_maintenanceworkorder 
FOR EACH ROW 
WHEN ((OLD.status<>3) and (NEW.status=3))
EXECUTE PROCEDURE finish_workorder_tfunc1();
```

2. 更新维修员状态

```sql
# 定义函数
CREATE OR REPLACE FUNCTION "my_root"."finish_workorder_tfunc2"()
  RETURNS "pg_catalog"."trigger" AS $BODY$BEGIN
	-- Routine body goes here...
	UPDATE dammapp_maintenanceman as a 
	SET a.status = 1
	where a.mid = NEW.mid_id;
	RETURN NEW;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  
# 创建触发器
CREATE TRIGGER finish_workorder_trigger2 AFTER UPDATE 
ON dammapp_maintenanceworkorder 
FOR EACH ROW 
WHEN ((OLD.status<>3) and (NEW.status=3))
EXECUTE PROCEDURE finish_workorder_tfunc2();
```



#### 5.维修员——add_usepart()，添加使用零件后更新派工单费用【“总材料费”加上当前零件花费】。

```sql
# 定义函数
CREATE OR REPLACE FUNCTION "my_root"."add_usepart_tfunc"()
  RETURNS "pg_catalog"."trigger" AS $BODY$BEGIN
	-- Routine body goes here...
	UPDATE dammapp_maintenanceworkorder as a 
	SET a."totalPartsCost" = a."totalPartsCost" + NEW."partCost"
	where a."workOrderId" = NEW."workOrderId_id";
	RETURN NEW;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  
# 创建触发器
CREATE TRIGGER add_usepart_trigger AFTER INSERT 
ON dammapp_useparts 
FOR EACH ROW 
EXECUTE PROCEDURE add_usepart_tfunc();
```



#### 6.维修员——del_usepart()，删除使用零件后更新派工单费用【“总材料费”减去当前零件花费】。

```sql
# 定义函数
CREATE OR REPLACE FUNCTION "my_root"."del_usepart_tfunc"()
  RETURNS "pg_catalog"."trigger" AS $BODY$BEGIN
	-- Routine body goes here...
	UPDATE dammapp_maintenanceworkorder as a 
	SET a."totalPartsCost" = a."totalPartsCost" - OLD."partCost"
	where a."workOrderId" = OLD."workOrderId_id";
	RETURN OLD;
END$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  
# 创建触发器
CREATE TRIGGER del_usepart_trigger AFTER DELETE 
ON dammapp_useparts 
FOR EACH ROW 
EXECUTE PROCEDURE del_usepart_tfunc();
```



