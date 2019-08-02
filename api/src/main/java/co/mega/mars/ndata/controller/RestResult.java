package co.mega.mars.ndata.controller;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import org.springframework.util.StringUtils;

public class RestResult {
    private String state = "fail";
    private Object data;
    private String message;
    private Integer pageSize;
    private Integer pageIndex;
    private Integer totalCount;

    public void setSuccess() {
        this.state = "success";
    }

    public void setFail() {
        this.state = "fail";
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public void setData(Object data) {
        this.data = data;
    }

    public String getState() {
        return state;
    }

    public Object getData() {
        return data;
    }

    public String getMessage() {
        return message;
    }

    public Integer getPageSize() {
        return pageSize;
    }

    public void setPageSize(Integer pageSize) {
        this.pageSize = pageSize;
    }

    public Integer getPageIndex() {
        return pageIndex;
    }

    public void setPageIndex(Integer pageIndex) {
        this.pageIndex = pageIndex;
    }

    public Integer getTotalCount() {
        return totalCount;
    }

    public void setTotalCount(Integer totalCount) {
        this.totalCount = totalCount;
    }

    public static String getFailResult() {
        return getFailResult(null, null);
    }

    public static String getFailResult(Object data) {
        return getFailResult(null, data);
    }

    public static String getFailResult(String message, Object data) {
        RestResult restResult = new RestResult();
        restResult.setFail();
        restResult.setMessage(StringUtils.isEmpty(message) ? "操作失败,请重试或联系系统管理员" : message);
        restResult.setData(data);

        return new Gson().toJson(restResult);
    }

    public static String getSuccessResult() {
        return getSuccessResult(null, null);
    }

    public static String getSuccessResult(Object data) {
        return getSuccessResult(null, data);
    }

    public static String getSuccessResult(String message, Object data) {
        RestResult restResult = new RestResult();
        restResult.setSuccess();
        restResult.setMessage(StringUtils.isEmpty(message) ? "操作成功" : message);
        restResult.setData(data);

        return new Gson().toJson(restResult);
    }

    public static String getSuccessResultWithPage(Object data, int pageSize, int pageIndex, int totalCount) {
        RestResult restResult = new RestResult();
        restResult.setSuccess();
        restResult.setMessage("操作成功");
        restResult.setData(data);
        restResult.setPageSize(pageSize);
        restResult.setPageIndex(pageIndex);
        restResult.setTotalCount(totalCount);

        return new Gson().toJson(restResult);
    }

    public static JsonObject pageResult(int total, int pageIndex, int pageSize, JsonArray array) {
        JsonObject rst = new JsonObject();
        rst.addProperty("total", total);
        rst.add("data", array);
        rst.addProperty("page_index", pageIndex);
        rst.addProperty("page_size", pageSize);

        return rst;
    }
}
