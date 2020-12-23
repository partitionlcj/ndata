package co.mega.mars.ndata.controller;

import com.google.common.base.Strings;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowCallbackHandler;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.Pipeline;

import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.*;

@Controller
public class ReportController {

    Logger logger = LoggerFactory.getLogger(ReportController.class);

    @Autowired
    @Qualifier("mainSSDB")
    JedisPool pool;
    @Autowired
    @Qualifier("bcpSSDB")
    JedisPool wavPool;

    @Autowired
    JdbcTemplate jdbcTemplate;

    @GetMapping("/api/audio/wakeup_wav")
    public void downloadWakeupWav(@RequestParam("requestId") String rid, HttpServletResponse response) throws Exception {
        try(Jedis dr = pool.getResource()) {
            String asrId = "WAKEUP_"+rid;
            byte[] data = dr.get((asrId).getBytes());

            response.setContentType("audio/x-wav");
            response.setHeader("Content-Disposition", "attachment; filename=\"WAKEUP_"+rid+".wav\"");
            if (data != null) {
                response.getOutputStream().write(data);
                response.flushBuffer();
            }
        }
    }

    @GetMapping("/api/audio/download_wav")
    public void downloadWavByRid(@RequestParam("requestId") String rid, HttpServletResponse response) throws Exception {
        try(Jedis dr = pool.getResource()) {
            String asrId = rid;
            byte[] data = dr.get((asrId).getBytes());

            response.setContentType("audio/x-wav");
            response.setHeader("Content-Disposition", "attachment; filename=\""+rid+".wav\"");
            if (data != null) {
                response.getOutputStream().write(data);
                response.flushBuffer();
            }
        }
    }

    @GetMapping("/api/ssdb/wav")
    public void downloadWav(@RequestParam("key") String key, HttpServletResponse response) throws Exception {
        Jedis r = wavPool.getResource();
        byte[] data = r.get(key.getBytes());
        response.setContentType("audio/x-wav");
        response.setHeader("Content-Disposition", "attachment; filename=\""+key+"\"");
        if( data != null ){
            response.getOutputStream().write(data);
            response.flushBuffer();
        }
        r.close();
    }


    @RequestMapping( value = "/api/ssdb/get", method = RequestMethod.GET, produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity getSsdbData(@RequestParam(defaultValue = "") String keys) throws Exception {
        Jedis ssdb = pool.getResource();

        if(Strings.isNullOrEmpty(keys)){
            return new ResponseEntity<Object>(RestResult.getFailResult("keys为空"), HttpStatus.OK);
        }

        String[] keyArr = keys.split(",");
        List<String> vals = ssdb.mget(keyArr);

        Gson g = new Gson();
        Map<String,Object> data = new HashMap<>();
        for(int i = 0 ; i < vals.size(); i++){
            String json = vals.get(i);
            if (Strings.isNullOrEmpty(json))
                continue;
            Object obj = json.startsWith("[") ? g.fromJson(json, JsonArray.class) : g.fromJson(json, JsonObject.class);
            data.put(keyArr[i], obj);
        }
        ssdb.close();
        return new ResponseEntity<Object>(RestResult.getSuccessResult(data), HttpStatus.OK);
    }

    @PostMapping("/api/common/lowQuality")
    public ResponseEntity  markLowQuality(@RequestBody String json) throws Exception {
        Gson g = new Gson();
        JsonObject p = g.fromJson(json, JsonObject.class);
        String rid = p.get("request_id").getAsString();
        String type = p.get("type").getAsString();
        int lowQualityType = -1;
        if( "cut".equals(type)){
            lowQualityType = 1001;
        }
        else {
            lowQualityType = 9999;
        }
        jdbcTemplate.update("update debug_query set badcase=? where request_id=?", new Object[]{lowQualityType,rid});
        logger.info("set low quality wav {} {}", rid, type);
        return new ResponseEntity<Object>(RestResult.getSuccessResult(p), HttpStatus.OK);
    }

    @PostMapping("/api/common/badcase")
    public ResponseEntity  addBadCase(@RequestBody String json) throws Exception {
        Gson g = new Gson();
        JsonObject p = g.fromJson(json, JsonObject.class);
        String rid = p.get("request_id").getAsString();

        try(CloseableHttpClient client = HttpClients.createDefault()){
            String url = String.format("http://ais.i-tetris.com:9890/api/nlu/asr/badcase");
            HttpPost httpPost = new HttpPost(url);
            StringEntity entity = new StringEntity(json,"utf-8");
            httpPost.setEntity(entity);
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");
            httpPost.setHeader("Cookie", "mars_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJubHVfYXBwIiwidWlkIjoxMDAwLCJvcmciOiJtZWdhIiwiaWF0IjoxNTkzNDAxNTY3LCJleHAiOjE2MjQ5Mzc1Njd9.Jb2HcRys719D6UuY0R2Sgl7XYQy3fZRrfp-cgjU7sX0");

            CloseableHttpResponse response = client.execute(httpPost);
            if (response.getStatusLine().getStatusCode() == 200) {
                jdbcTemplate.update("update debug_query set badcase=1 where request_id=?", new Object[]{rid});
                return new ResponseEntity<Object>(RestResult.getSuccessResult(p), HttpStatus.OK);

            } else {
                return new ResponseEntity<Object>(RestResult.getFailResult("failed to add badcase,"+response.getEntity().toString(),p), HttpStatus.OK);
            }
        }
    }

    public static void main(String[] args) {
        try(CloseableHttpClient client = HttpClients.createDefault()){
            String url = String.format("http://ais.i-tetris.com:9890/api/nlu/asr/badcase");
            HttpPost httpPost = new HttpPost(url);
            StringEntity entity = new StringEntity("{'request_id':'aaa','text':'test','asr_text':'test_asr','type':1000,'weight':1}");
            httpPost.setEntity(entity);
            httpPost.setHeader("Accept", "application/json");
            httpPost.setHeader("Content-type", "application/json");
            httpPost.setHeader("", "mars_token=eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJubHVfYXBwIiwidWlkIjoxMDAwLCJvcmciOiJtZWdhIiwiaWF0IjoxNTkzNDAxNTY3LCJleHAiOjE2MjQ5Mzc1Njd9.Jb2HcRys719D6UuY0R2Sgl7XYQy3fZRrfp-cgjU7sX0");

            CloseableHttpResponse response = client.execute(httpPost);
            if (response.getStatusLine().getStatusCode() == 200) {
                System.out.println("success");
            } else {
                System.out.println("failed:"+response.getEntity().toString());
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @PostMapping("/api/common/read_page_ssdb")
    public ResponseEntity  commonReadPageSsdb(@RequestBody String json) throws Exception {
        Gson g = new Gson();
        JsonObject params = g.fromJson(json, JsonObject.class);
        String key = params.get("key").getAsString();
        int pageIndex = params.get("page_index").getAsInt();
        int pageSize = params.get("page_size").getAsInt();

        Jedis jedis = pool.getResource();

        String content = jedis.get(key);
        JsonArray array = g.fromJson(content, JsonArray.class);

        List<String> keyList = new ArrayList<>(pageSize);

        int beginIndex = pageIndex * pageSize - pageSize;
        int endIndex = beginIndex + pageSize;
        logger.info("begin index : {}", beginIndex);
        logger.info("end index : {}", endIndex);
        for (int i=beginIndex; i<endIndex && i<array.size(); i++) {
            keyList.add("context.{" + array.get(i).getAsString() + "}");
        }

        JsonArray rst = new JsonArray();

        Pipeline pipeline = jedis.pipelined();
        for (String contextKey : keyList) {
            logger.info("context key : {}", contextKey);
            pipeline.get(contextKey);
        }
        List<Object> contextList = pipeline.syncAndReturnAll();
        logger.info("context list : {}", contextList);
        // 如果json解析失败, 返回值包含session_id的json object
        for (int i=0; i<contextList.size(); i++) {
            String sessionId = array.get(i).getAsString();
            try {
                JsonObject item = g.fromJson(contextList.get(i).toString(), JsonObject.class);
                rst.add(item);
            } catch (Exception e) {
                logger.error("parse json object error : {}", sessionId, e);

                JsonObject item = new JsonObject();
                item.addProperty("session_id", sessionId);
                rst.add(item);
            }
        }

        JsonObject rstItem = RestResult.pageResult(array.size(), pageIndex, pageSize, rst);
        return new ResponseEntity<Object>(RestResult.getSuccessResult(rstItem), HttpStatus.OK);
    }

    private static final String[] JSON_COLUMNS = {"input","output","nlp_result","model_results","rule_da_result","nlu_result","server_state"};
    @GetMapping("/api/debug/getReqInfo")
    public ResponseEntity<Object> getReqInfo(@RequestParam("rid")String rid){
        Map r = jdbcTemplate.queryForMap("select * from dialogue.request_info where id=?", new Object[]{rid});
        JsonArray jr = new JsonArray();
        Arrays.stream(JSON_COLUMNS).forEach((c)->convert2Json(c,r ,jr));
        return new ResponseEntity<Object>(GsonUtil.instance().toJson(jr), HttpStatus.OK);
    }

    @GetMapping("/api/debug/getVosReqInfo")
    public ResponseEntity<Object> getVosReqInfo(@RequestParam("rid")String rid){
        Map r = jdbcTemplate.queryForMap("select * from dialogue.vos_request_info where request_id=?", new Object[]{rid});
        JsonArray jr = new JsonArray();
        convertStr("request_id",r ,jr);
        convertStr("vehicle_id",r ,jr);
        convertStr("env",r ,jr);
        convert2Json("log_data",r ,jr);
        convertLong("start_time",r ,jr);
        convertLong("end_time",r ,jr);
        convertLong("update_time",r ,jr);
        return new ResponseEntity<Object>(GsonUtil.instance().toJson(jr), HttpStatus.OK);
    }

    private void convertLong(String k, Map m, JsonArray jr){
        Long v = (Long) m.get(k);
        if( v == null || "null".equals(v))return;

        JsonObject big = new JsonObject();
        big.addProperty(k,v);
        jr.add(big);
    }

    private void convertStr(String k, Map m, JsonArray jr){
        String v = (String) m.get(k);
        if( v == null || "null".equals(v))return;

        JsonObject big = new JsonObject();
        big.addProperty(k,v);
        jr.add(big);
    }

    private void convert2Json(String k, Map m, JsonArray jr){
        String v = (String) m.get(k);
        if( v == null || "null".equals(v))return;
        try {
            JsonObject o = GsonUtil.instance().fromJson(v, JsonObject.class);
            JsonObject big = new JsonObject();
            big.add(k,o);
            jr.add(big);
        }catch (Exception ex){
            logger.error("failed to convert {} to json object ", v,ex);
        }
    }

    @GetMapping("/api/debug/output")
    public ResponseEntity<Object> getOutput(@RequestParam("rid")String rid){
        String output = jdbcTemplate.queryForObject("select output from debug_query where request_id=?", new Object[]{rid}, String.class);
        return new ResponseEntity<Object>(RestResult.getSuccessResult(output), HttpStatus.OK);
    }

    @PostMapping("/api/sp/com/batch_comment")
    public ResponseEntity<String> getComment(){
        return ResponseEntity.ok("{}");
    }

    @PostMapping("/api/common/report")
    public ResponseEntity commonReport(@RequestBody String json) throws Exception {
        return new ResponseEntity<Object>(RestResult.getSuccessResult(getReport(json)), HttpStatus.OK);
    }

    public JsonElement getReport(String json) throws Exception {
        logger.info("json:{}", json);
        boolean custom = false;
        Gson g = new Gson();
        JsonObject queryParam = g.fromJson(json, JsonObject.class);

        String reportName = queryParam.get("report_name").getAsString();
        JsonObject reportMetaData = GsonUtil.getQueryResult(jdbcTemplate, "select * from report_meta_data where report_name=?", new Object[]{reportName}).get(0);
        JsonArray reportTitle = g.fromJson(reportMetaData.get("report_title").getAsString(), JsonArray.class);

        String reportSql = reportMetaData.get("report_sql").getAsString();

        String where = null;
        if( queryParam.get("customQuery") != null){
            String query = queryParam.get("customQuery").getAsString().trim();
            if( query.length() > 0 && ! "undefined".equals(query) ){
                int start = reportSql.indexOf("from");
                int end = reportSql.indexOf("where");
                where = " "+reportSql.substring(start,end) +" where " + query;
                custom = true;
            }
        }

        String reportParams = reportMetaData.remove("report_params").getAsString();
        JsonArray reportParamArray = reportParams.length() == 0 ? new JsonArray() : g.fromJson(reportParams, JsonArray.class);

        Object[] params = new Object[reportParamArray.size()];
        for (int i=0; i<reportParamArray.size(); i++) {
            JsonObject item = reportParamArray.get(i).getAsJsonObject();
            int index = item.get("index").getAsInt();
            String name = item.get("name").getAsString();
            String value = queryParam.get(name) == null || queryParam.get(name).isJsonNull() ? item.get("default").getAsString() : queryParam.get(name).getAsString();

            params[index - 1] = value;
        }
        if( custom){
            params = new Object[0];
        }
        logger.info("params:{}", Arrays.toString(params));

        if( custom ){
            reportSql = reportSql.substring(0, reportSql.indexOf("from")) + where;
        }

        where =  reportSql.substring(reportSql.indexOf("from"));

        int total = 0;
        if (GsonUtil.getAsInt(queryParam, "pageIndex", 0) == 0 && GsonUtil.getAsInt(queryParam, "pageSize", 0) == 0) {
            total = 1;
        }
        else if (params.length == 0 || custom) {
            total = jdbcTemplate.queryForObject("select count(*) " + where, Integer.class);
        }
        else
            total = jdbcTemplate.queryForObject("select count(*) " + where, params, Integer.class);

        if (total == 0) {
            return getReportResult(total, reportTitle, new JsonArray());
        }

        // 拼接排序SQL
        String sortPartition = GsonUtil.getAsString(reportMetaData, "report_order");
        if (! Strings.isNullOrEmpty(sortPartition)) {
            reportSql += " " + sortPartition;
        }

        JsonArray dataArray = new JsonArray();
        if (GsonUtil.getAsInt(queryParam, "pageIndex", 0) > 0 && GsonUtil.getAsInt(queryParam, "pageSize", 0) > 0) {
            params = Arrays.copyOf(params, params.length + 2);
            params[params.length - 2] = queryParam.get("pageIndex").getAsInt() * queryParam.get("pageSize").getAsInt() - queryParam.get("pageSize").getAsInt();
            params[params.length - 1] = queryParam.get("pageSize").getAsInt();
            reportSql += " limit ?, ?";
        }

        jdbcTemplate.query(reportSql, params, new RowCallbackHandler() {
            @Override
            public void processRow(ResultSet rs) throws SQLException {
                try {
                    JsonObject item = GsonUtil.convertFromResultSet(rs);

                    JsonArray array = new JsonArray();
                    ResultSetMetaData meta = rs.getMetaData();
                    for (int i=1; i<=meta.getColumnCount(); i++)
                        array.add(item.remove(meta.getColumnName(i)));
                    dataArray.add(array);
                } catch (Exception e) {logger.error("error", e);}
            }
        });

        return getReportResult(total, reportTitle, dataArray);
    }

    private JsonObject getReportResult(int total, JsonArray title, JsonArray data) throws Exception {
        JsonObject rst = new JsonObject();
        rst.addProperty("total", total);
        rst.add("title", title);
        rst.add("data", data);
        return rst;
    }
}
