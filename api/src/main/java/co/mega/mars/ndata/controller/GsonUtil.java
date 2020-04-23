package co.mega.mars.ndata.controller;

import com.google.common.base.Strings;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.util.StringUtils;

import java.math.BigDecimal;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

public class GsonUtil {
    private static final Logger logger = LogManager.getLogger(GsonUtil.class);

    private static final Gson gson = new Gson();

    public static Gson instance() {
        return gson;
    }

    public static void addElement(JsonObject obj, String key, String element) {
        if (StringUtils.isEmpty(element))
            obj.addProperty(key, "");
        else
            obj.add(key, gson.fromJson(element, JsonElement.class));
    }

    public static String getAsString(JsonObject jsonObject, String key) {
        return getAsString(jsonObject, key, "");
    }

    public static String getAsString(JsonObject jsonObject, String key, String defaultValue) {
        if (jsonObject == null || jsonObject.get(key) == null)
            return defaultValue;

        JsonElement item = jsonObject.get(key);
        if (item == null || item.isJsonNull())
            return defaultValue;
        return item.isJsonPrimitive() ? item.getAsString() : instance().toJson(item);
    }

    public static String getAsStringNotEmpty(JsonObject jsonObject, String key) throws Exception {
        String value = getAsString(jsonObject, key);
        if (Strings.isNullOrEmpty(value))
            throw new IllegalArgumentException(key + " not empty");
        return value;
    }

    public static int getAsIntNotEmpty(JsonObject jsonObject, String key) throws Exception {
        String value = getAsString(jsonObject, key);
        if (Strings.isNullOrEmpty(value))
            throw new IllegalArgumentException(key + " not empty");

        return Integer.parseInt(value);
    }

    public static JsonElement getJsonElement(JsonElement jsonElement, String parents) {
        if (jsonElement == null || jsonElement.isJsonNull())
            return null;
        if (StringUtils.isEmpty(parents))
            return jsonElement;

        for (String str : parents.split(",")) {
            if(jsonElement == null || jsonElement.isJsonNull() || !jsonElement.isJsonObject())
                return null;
            jsonElement = jsonElement.getAsJsonObject().get(str);
        }
        return jsonElement == null || jsonElement.isJsonNull() ? null : jsonElement;
    }

    public static JsonArray getJsonArray(String items) {
        JsonArray array = new JsonArray();
        if (StringUtils.isEmpty(items))
            return array;

        for (String item : items.split(","))
            array.add(item);
        return array;
    }

    public static int getAsInt(JsonObject jsonObject, String key) {
        return getAsInt(jsonObject, key, 0);
    }

    public static int getAsInt(JsonObject jsonObject, String key, int defaultValule) {
        if (jsonObject == null || jsonObject.get(key) == null || jsonObject.get(key).isJsonNull())
            return defaultValule;

        String value = getAsString(jsonObject, key, Integer.toString(defaultValule));
        try {
            return Strings.isNullOrEmpty(value) ? defaultValule : Integer.parseInt(value);
        } catch (Exception e) {
            return defaultValule;
        }
    }

    /**
     * 浅拷贝
     */
    public static JsonObject shallowCopy(JsonObject item) {
        if (item == null)
            return item;

        JsonObject copyItem = new JsonObject();
        item.entrySet().forEach(v -> copyItem.add(v.getKey(), v.getValue()));
        return copyItem;
    }

    public static JsonObject convertFromResultSet(ResultSet rs) throws Exception {
        JsonObject rst = new JsonObject();

        ResultSetMetaData meta = rs.getMetaData();
        for (int i=1; i<=meta.getColumnCount(); i++) {
            String columnName = meta.getColumnName(i);
            Class clazz = Class.forName(meta.getColumnClassName(i));

            if (clazz == Integer.class || clazz == Boolean.class) { // 在这里, 我们将boolean转化成int用
                rst.addProperty(columnName, rs.getInt(columnName));
            }
            else if (clazz == Long.class) {
                rst.addProperty(columnName, rs.getLong(columnName));
            }
            else if (clazz == BigDecimal.class) {
                BigDecimal bigDecimal = rs.getBigDecimal(columnName);
                rst.addProperty(columnName, bigDecimal == null ? 0 : bigDecimal.longValue());
            }
            else if (clazz == String.class) {
                String str = rs.getString(columnName);
                rst.addProperty(columnName, str == null ? "" : str);
            }
            else if (clazz == Timestamp.class) {
                Timestamp timestamp = rs.getTimestamp(columnName);
                rst.addProperty(columnName, timestamp == null ? null : timestamp.getTime());
            }
            else {
                throw new IllegalArgumentException("column type(" +clazz.toString() + ") can not parse");
            }
        }

        return rst;
    }

    public static List<JsonObject> getQueryResult(JdbcTemplate jdbcTemplate, String sql) throws Exception {
        List<JsonObject> rst = new ArrayList<>();
        jdbcTemplate.query(sql, new RowCallbackHandler() {
            @Override
            public void processRow(ResultSet rs) throws SQLException {
                try {
                    rst.add(GsonUtil.convertFromResultSet(rs));
                } catch (Exception e) {logger.error(sql + " error", e);}
            }
        });
        return  rst;
    }

    public static JsonArray getQueryResultWithJsonArray(JdbcTemplate jdbcTemplate, String sql) throws Exception {
        List<JsonObject> list = getQueryResult(jdbcTemplate, sql);
        JsonArray array = new JsonArray(list.size());
        list.forEach(v -> array.add(v));
        return array;
    }

    public static List<JsonObject> getQueryResult(JdbcTemplate jdbcTemplate, String sql, Object... parmas) throws Exception {
        List<JsonObject> rst = new ArrayList<>();
        jdbcTemplate.query(sql, parmas, new RowCallbackHandler() {
            @Override
            public void processRow(ResultSet rs) throws SQLException {
                try {
                    rst.add(GsonUtil.convertFromResultSet(rs));
                } catch (Exception e) {logger.error(sql + " error", e);}
            }
        });
        return  rst;
    }

    public static JsonArray getQueryResultWithJsonArray(JdbcTemplate jdbcTemplate, String sql, Object... parmas) throws Exception {
        List<JsonObject> list = getQueryResult(jdbcTemplate, sql, parmas);
        JsonArray array = new JsonArray(list.size());
        list.forEach(v -> array.add(v));
        return array;
    }

    public static void main(String[] args) {
        Date dt = new Date();
        dt.setTime(1579514677000l);
        System.out.println(dt);
    }
}
